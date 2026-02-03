"""
Main Evaluation Runner for GTM-Agent Tool Evaluation.

This module orchestrates the evaluation process:
1. Parses task definitions from evaluation.xml
2. Runs tasks against the API or directly against agents
3. Calculates scores using the scorers module
4. Generates comprehensive reports

Usage:
    # Run from command line
    python -m tests.evaluation.evaluation
    
    # Or programmatically
    from tests.evaluation import EvaluationRunner
    
    runner = EvaluationRunner()
    report = await runner.run_evaluation("tests/evaluation/evaluation.xml")
    print(report.to_markdown())
"""

import asyncio
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx

from tests.evaluation.models import (
    CategoryMetrics,
    EvaluationConfig,
    EvaluationReport,
    EvaluationResult,
    ExpectedRouting,
    TaskDefinition,
    TaskExpectations,
    TaskScores,
    TokenUsage,
    ToolInvocation,
    ToolMetrics,
)
from tests.evaluation.scorers import (
    calculate_task_scores,
    score_citations,
    score_code_quality,
    score_efficiency,
    score_keywords,
    score_performance,
    score_routing,
    score_tool_selection,
    score_waf_reference,
)


class EvaluationRunner:
    """
    Main orchestrator for running tool evaluations.
    
    Supports two evaluation modes:
    - API mode: Sends requests to the HTTP API endpoint
    - Direct mode: Runs against agent classes directly (faster, more metrics)
    
    Example:
        runner = EvaluationRunner(config=EvaluationConfig(mode="api"))
        report = await runner.run_evaluation("evaluation.xml")
        print(report.to_markdown())
    """
    
    def __init__(self, config: EvaluationConfig | None = None):
        """
        Initialize the evaluation runner.
        
        Args:
            config: Evaluation configuration. Uses defaults if not provided.
        """
        self.config = config or EvaluationConfig()
        self._http_client: httpx.AsyncClient | None = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self._http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.config.timeout_seconds)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None
    
    def parse_evaluation_file(self, file_path: str | Path) -> tuple[EvaluationConfig, list[TaskDefinition]]:
        """
        Parse an XML evaluation file.
        
        Args:
            file_path: Path to the evaluation.xml file
            
        Returns:
            Tuple of (config, tasks) parsed from the file
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Evaluation file not found: {file_path}")
        
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Parse config if present
        config = self.config
        config_elem = root.find("config")
        if config_elem is not None:
            timeout = config_elem.find("timeout_seconds")
            if timeout is not None and timeout.text:
                config = config.model_copy(
                    update={"timeout_seconds": float(timeout.text)}
                )
        
        # Parse tasks
        tasks: list[TaskDefinition] = []
        for task_elem in root.findall(".//task"):
            task = self._parse_task_element(task_elem)
            if task:
                tasks.append(task)
        
        return config, tasks
    
    def _parse_task_element(self, task_elem: ET.Element) -> TaskDefinition | None:
        """Parse a single task element from XML."""
        task_id = task_elem.get("id", "")
        category = task_elem.get("category", "")
        
        prompt_elem = task_elem.find("prompt")
        if prompt_elem is None or not prompt_elem.text:
            return None
        
        description_elem = task_elem.find("description")
        description = description_elem.text if description_elem is not None else None
        
        # Parse expected outcomes
        expected_elem = task_elem.find("expected")
        expected = TaskExpectations()
        
        if expected_elem is not None:
            # Routing
            routing_elem = expected_elem.find("routing")
            if routing_elem is not None and routing_elem.text:
                try:
                    expected.routing = ExpectedRouting(routing_elem.text.strip())
                except ValueError:
                    pass
            
            # Tools
            tools_elem = expected_elem.find("tools")
            if tools_elem is not None and tools_elem.text:
                expected.tools = [t.strip() for t in tools_elem.text.split(",")]
            
            # Keywords
            keywords_elem = expected_elem.find("keywords")
            if keywords_elem is not None and keywords_elem.text:
                expected.keywords = [k.strip() for k in keywords_elem.text.split(",")]
            
            # Boolean flags
            for flag in ["has_citations", "has_waf_reference", "has_code_block"]:
                elem = expected_elem.find(flag)
                if elem is not None and elem.text:
                    setattr(expected, flag, elem.text.lower() == "true")
            
            # Code patterns
            patterns_elem = expected_elem.find("code_patterns")
            if patterns_elem is not None and patterns_elem.text:
                expected.code_patterns = [p.strip() for p in patterns_elem.text.split(",")]
            
            # Numeric constraints
            for num_field in ["min_steps", "max_steps", "max_tool_calls"]:
                elem = expected_elem.find(num_field)
                if elem is not None and elem.text:
                    setattr(expected, num_field, int(elem.text))
            
            # Duration
            duration_elem = expected_elem.find("max_duration_seconds")
            if duration_elem is not None and duration_elem.text:
                expected.max_duration_seconds = float(duration_elem.text)
        
        return TaskDefinition(
            id=task_id,
            category=category,
            prompt=prompt_elem.text.strip(),
            expected=expected,
            description=description,
        )
    
    async def run_task_via_api(self, task: TaskDefinition) -> EvaluationResult:
        """
        Run a single task via the HTTP API.
        
        Args:
            task: The task definition to evaluate
            
        Returns:
            EvaluationResult with all metrics
        """
        if not self._http_client:
            self._http_client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.config.timeout_seconds)
            )
        
        start_time = time.perf_counter()
        result = EvaluationResult(task=task)
        
        try:
            response = await self._http_client.post(
                f"{self.config.base_url}/agent/query",
                json={"content": task.prompt},
            )
            
            duration = time.perf_counter() - start_time
            result.duration_seconds = duration
            
            if response.status_code == 200:
                data = response.json()
                result.success = True
                result.response_text = data.get("content", "")
                result.response_preview = result.response_text[:500] + "..." if len(result.response_text) > 500 else result.response_text
                
                # Extract metadata from response
                result.actual_routing = data.get("classification", {}).get("category")
                result.iterations_used = data.get("iterations", 0)
                result.verification_score = data.get("verification_score")
                
                # Extract agents/tools used
                steps = data.get("execution_steps", [])
                result.steps_executed = len(steps)
                result.actual_tools = list(set(
                    step.get("tool") for step in steps if step.get("tool")
                ))
                
                # Convert steps to tool invocations for metrics
                for step in steps:
                    if step.get("tool"):
                        result.tool_invocations.append(ToolInvocation(
                            tool_name=step.get("tool", "unknown"),
                            arguments={"query": step.get("query", "")},
                            result=step.get("result", "")[:500] if step.get("result") else None,
                            duration_seconds=step.get("duration", 0),
                        ))
                
                # Token usage if available
                usage = data.get("usage")
                if usage:
                    result.token_usage = TokenUsage(
                        input_tokens=usage.get("input_tokens", 0),
                        output_tokens=usage.get("output_tokens", 0),
                        total_tokens=usage.get("total_tokens", 0),
                    )
            else:
                result.success = False
                result.error = f"HTTP {response.status_code}: {response.text[:200]}"
                
        except httpx.TimeoutException:
            result.success = False
            result.error = f"Timeout after {self.config.timeout_seconds}s"
            result.duration_seconds = time.perf_counter() - start_time
        except Exception as e:
            result.success = False
            result.error = f"{type(e).__name__}: {str(e)}"
            result.duration_seconds = time.perf_counter() - start_time
        
        # Calculate scores
        result.scores = self._calculate_scores(result)
        
        return result
    
    def _calculate_scores(self, result: EvaluationResult) -> TaskScores:
        """Calculate all scores for an evaluation result."""
        task = result.task
        expected = task.expected
        
        scores = TaskScores(
            routing_score=score_routing(
                expected.routing.value if expected.routing else None,
                result.actual_routing,
            ),
            tool_selection_score=score_tool_selection(
                expected.tools,
                result.actual_tools,
            ),
            keyword_coverage_score=score_keywords(
                result.response_text,
                expected.keywords,
            ),
            citation_score=score_citations(
                result.response_text,
                expected.has_citations,
            ),
            code_quality_score=score_code_quality(
                result.response_text,
                expected.has_code_block,
                expected.code_patterns,
            ),
            performance_score=score_performance(
                result.duration_seconds,
                expected.max_duration_seconds,
            ),
            efficiency_score=score_efficiency(
                len(result.tool_invocations),
                expected.max_tool_calls,
            ),
        )
        
        return scores
    
    async def run_evaluation(
        self,
        eval_path: str | Path,
        task_filter: list[str] | None = None,
    ) -> EvaluationReport:
        """
        Run the full evaluation suite.
        
        Args:
            eval_path: Path to evaluation.xml file
            task_filter: Optional list of task IDs to run (runs all if None)
            
        Returns:
            Complete EvaluationReport with all results and metrics
        """
        print(f"🚀 Starting Evaluation from {eval_path}")
        
        # Parse evaluation file
        config, tasks = self.parse_evaluation_file(eval_path)
        self.config = config
        
        # Filter tasks if specified
        if task_filter:
            tasks = [t for t in tasks if t.id in task_filter]
        
        print(f"📋 Loaded {len(tasks)} evaluation tasks")
        
        # Run all tasks
        results: list[EvaluationResult] = []
        
        async with self:
            for i, task in enumerate(tasks):
                print(f"\n[{i + 1}/{len(tasks)}] Running: {task.id}")
                print(f"    Prompt: {task.prompt[:60]}...")
                
                if self.config.mode == "api":
                    result = await self.run_task_via_api(task)
                else:
                    # Direct mode - would require agent imports
                    result = await self.run_task_via_api(task)  # Fallback to API
                
                results.append(result)
                
                status = "✅ PASSED" if result.passed else "❌ FAILED"
                print(f"    {status} (score: {result.scores.overall_score:.2f}, duration: {result.duration_seconds:.1f}s)")
                
                if result.error:
                    print(f"    Error: {result.error}")
        
        # Generate report
        report = self._generate_report(eval_path, results)
        
        print(f"\n{'=' * 60}")
        print(f"📊 Evaluation Complete")
        print(f"{'=' * 60}")
        print(f"Total: {report.total_tasks} | Passed: {report.passed_tasks} | Failed: {report.failed_tasks}")
        print(f"Pass Rate: {report.pass_rate * 100:.1f}%")
        print(f"Overall Accuracy: {report.overall_accuracy * 100:.1f}%")
        
        return report
    
    def _generate_report(
        self,
        eval_path: str | Path,
        results: list[EvaluationResult],
    ) -> EvaluationReport:
        """Generate a complete evaluation report from results."""
        report = EvaluationReport(
            config=self.config,
            evaluation_file=str(eval_path),
            results=results,
            total_tasks=len(results),
            passed_tasks=sum(1 for r in results if r.passed),
            failed_tasks=sum(1 for r in results if not r.passed),
        )
        
        if not results:
            return report
        
        # Calculate aggregate scores
        successful_results = [r for r in results if r.success]
        
        if successful_results:
            report.overall_accuracy = sum(r.scores.overall_score for r in successful_results) / len(successful_results)
            report.routing_accuracy = sum(r.scores.routing_score for r in successful_results) / len(successful_results)
            report.tool_selection_accuracy = sum(r.scores.tool_selection_score for r in successful_results) / len(successful_results)
            report.avg_keyword_coverage = sum(r.scores.keyword_coverage_score for r in successful_results) / len(successful_results)
            report.avg_performance_score = sum(r.scores.performance_score for r in successful_results) / len(successful_results)
        
        # Aggregate token usage
        for result in results:
            report.total_token_usage += result.token_usage
        
        # Calculate tool metrics
        tool_data: dict[str, ToolMetrics] = {}
        for result in results:
            for inv in result.tool_invocations:
                if inv.tool_name not in tool_data:
                    tool_data[inv.tool_name] = ToolMetrics(tool_name=inv.tool_name)
                
                metrics = tool_data[inv.tool_name]
                metrics.call_count += 1
                metrics.total_duration_seconds += inv.duration_seconds
                if inv.error:
                    metrics.error_count += 1
                else:
                    metrics.success_count += 1
        
        report.tool_metrics = list(tool_data.values())
        
        # Calculate category metrics
        category_data: dict[str, list[EvaluationResult]] = {}
        for result in results:
            category = result.task.category
            if category not in category_data:
                category_data[category] = []
            category_data[category].append(result)
        
        for category, cat_results in category_data.items():
            successful = [r for r in cat_results if r.success]
            report.category_metrics.append(CategoryMetrics(
                category=category,
                task_count=len(cat_results),
                passed_count=sum(1 for r in cat_results if r.passed),
                avg_score=sum(r.scores.overall_score for r in successful) / len(successful) if successful else 0,
                avg_duration_seconds=sum(r.duration_seconds for r in successful) / len(successful) if successful else 0,
                avg_tool_calls=sum(len(r.tool_invocations) for r in successful) / len(successful) if successful else 0,
            ))
        
        # Generate recommendations based on results
        report.recommendations = self._generate_recommendations(report)
        
        return report
    
    def _generate_recommendations(self, report: EvaluationReport) -> list[str]:
        """Generate improvement recommendations based on evaluation results."""
        recommendations: list[str] = []
        
        if report.routing_accuracy < 0.9:
            recommendations.append(
                f"Routing accuracy is {report.routing_accuracy * 100:.1f}% (target: 90%). "
                "Consider reviewing classifier patterns for misclassified queries."
            )
        
        if report.tool_selection_accuracy < 0.85:
            recommendations.append(
                f"Tool selection accuracy is {report.tool_selection_accuracy * 100:.1f}% (target: 85%). "
                "Review planner prompts to improve tool selection logic."
            )
        
        if report.avg_keyword_coverage < 0.75:
            recommendations.append(
                f"Average keyword coverage is {report.avg_keyword_coverage * 100:.1f}% (target: 75%). "
                "Responses may be missing key information. Check sub-agent prompts."
            )
        
        if report.avg_performance_score < 0.8:
            recommendations.append(
                f"Performance score is {report.avg_performance_score * 100:.1f}% (target: 80%). "
                "Consider optimizing slow tools or reducing unnecessary iterations."
            )
        
        # Check for tools with high error rates
        for tool in report.tool_metrics:
            if tool.success_rate < 0.9 and tool.call_count >= 3:
                recommendations.append(
                    f"Tool '{tool.tool_name}' has {tool.success_rate * 100:.1f}% success rate. "
                    "Investigate error causes."
                )
        
        # Check for underperforming categories
        for cat in report.category_metrics:
            pass_rate = cat.passed_count / cat.task_count if cat.task_count > 0 else 0
            if pass_rate < 0.7:
                recommendations.append(
                    f"Category '{cat.category}' has {pass_rate * 100:.1f}% pass rate. "
                    "Review failed tasks for common issues."
                )
        
        return recommendations
    
    def generate_markdown_report(self, report: EvaluationReport) -> str:
        """
        Generate a markdown-formatted report.
        
        Args:
            report: The evaluation report to format
            
        Returns:
            Markdown string of the report
        """
        lines = [
            "# GTM-Agent Tool Evaluation Report",
            "",
            "## Summary",
            "",
            f"- **Date**: {report.timestamp.isoformat()}",
            f"- **Evaluation File**: {report.evaluation_file}",
            f"- **Mode**: {report.config.mode}",
            "",
            "### Results Overview",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Tasks | {report.total_tasks} |",
            f"| Passed | {report.passed_tasks} |",
            f"| Failed | {report.failed_tasks} |",
            f"| Pass Rate | {report.pass_rate * 100:.1f}% |",
            "",
            "### Dimension Scores",
            "",
            "| Dimension | Score | Target | Status |",
            "|-----------|-------|--------|--------|",
            f"| Routing Accuracy | {report.routing_accuracy * 100:.1f}% | 90% | {'✅' if report.routing_accuracy >= 0.9 else '❌'} |",
            f"| Tool Selection | {report.tool_selection_accuracy * 100:.1f}% | 85% | {'✅' if report.tool_selection_accuracy >= 0.85 else '❌'} |",
            f"| Keyword Coverage | {report.avg_keyword_coverage * 100:.1f}% | 75% | {'✅' if report.avg_keyword_coverage >= 0.75 else '❌'} |",
            f"| Performance | {report.avg_performance_score * 100:.1f}% | 80% | {'✅' if report.avg_performance_score >= 0.8 else '❌'} |",
            "",
            "### Token Usage",
            "",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| Input Tokens | {report.total_token_usage.input_tokens:,} |",
            f"| Output Tokens | {report.total_token_usage.output_tokens:,} |",
            f"| Total Tokens | {report.total_token_usage.total_tokens:,} |",
            "",
        ]
        
        # Tool metrics
        if report.tool_metrics:
            lines.extend([
                "## Tool Call Analysis",
                "",
                "| Tool | Calls | Avg Duration | Success Rate |",
                "|------|-------|--------------|--------------|",
            ])
            for tool in sorted(report.tool_metrics, key=lambda t: t.call_count, reverse=True):
                lines.append(
                    f"| {tool.tool_name} | {tool.call_count} | "
                    f"{tool.avg_duration_seconds:.2f}s | {tool.success_rate * 100:.1f}% |"
                )
            lines.append("")
        
        # Category metrics
        if report.category_metrics:
            lines.extend([
                "## Per-Category Results",
                "",
                "| Category | Tasks | Passed | Avg Score | Avg Duration |",
                "|----------|-------|--------|-----------|--------------|",
            ])
            for cat in sorted(report.category_metrics, key=lambda c: c.category):
                pass_rate = cat.passed_count / cat.task_count if cat.task_count > 0 else 0
                lines.append(
                    f"| {cat.category} | {cat.task_count} | "
                    f"{cat.passed_count} ({pass_rate * 100:.0f}%) | "
                    f"{cat.avg_score:.2f} | {cat.avg_duration_seconds:.1f}s |"
                )
            lines.append("")
        
        # Recommendations
        if report.recommendations:
            lines.extend([
                "## Recommendations",
                "",
            ])
            for i, rec in enumerate(report.recommendations, 1):
                lines.append(f"{i}. {rec}")
            lines.append("")
        
        # Detailed results
        lines.extend([
            "## Detailed Task Results",
            "",
        ])
        
        for result in report.results:
            status = "✅ PASSED" if result.passed else "❌ FAILED"
            lines.extend([
                f"### {result.task.id}: {status}",
                "",
                f"**Prompt**: {result.task.prompt}",
                "",
                f"| Metric | Value |",
                f"|--------|-------|",
                f"| Duration | {result.duration_seconds:.2f}s |",
                f"| Overall Score | {result.scores.overall_score:.2f} |",
                f"| Routing Score | {result.scores.routing_score:.2f} |",
                f"| Tool Selection | {result.scores.tool_selection_score:.2f} |",
                f"| Tools Used | {', '.join(result.actual_tools) or 'None'} |",
                "",
            ])
            
            if result.error:
                lines.append(f"**Error**: {result.error}")
                lines.append("")
            
            if result.response_preview:
                lines.extend([
                    "<details>",
                    "<summary>Response Preview</summary>",
                    "",
                    "```",
                    result.response_preview,
                    "```",
                    "",
                    "</details>",
                    "",
                ])
            
            lines.append("---")
            lines.append("")
        
        return "\n".join(lines)
    
    async def save_report(
        self,
        report: EvaluationReport,
        output_dir: str | Path = "tests/evaluation/reports",
    ) -> Path:
        """
        Save the evaluation report to a file.
        
        Args:
            report: The report to save
            output_dir: Directory to save the report
            
        Returns:
            Path to the saved report file
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = report.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = f"evaluation_report_{timestamp}.md"
        filepath = output_dir / filename
        
        markdown = self.generate_markdown_report(report)
        filepath.write_text(markdown, encoding="utf-8")
        
        print(f"\n📄 Report saved to: {filepath}")
        
        return filepath


async def main():
    """Main entry point for running evaluations from command line."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run GTM-Agent Tool Evaluation")
    parser.add_argument(
        "--eval-file",
        default="tests/evaluation/evaluation.xml",
        help="Path to evaluation XML file",
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="Base URL for the API",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=300,
        help="Timeout in seconds per task",
    )
    parser.add_argument(
        "--tasks",
        nargs="*",
        help="Specific task IDs to run (runs all if not specified)",
    )
    parser.add_argument(
        "--save-report",
        action="store_true",
        help="Save the report to a file",
    )
    
    args = parser.parse_args()
    
    config = EvaluationConfig(
        base_url=args.base_url,
        timeout_seconds=args.timeout,
    )
    
    runner = EvaluationRunner(config=config)
    report = await runner.run_evaluation(args.eval_file, task_filter=args.tasks)
    
    # Print markdown report
    print("\n" + "=" * 60)
    print(runner.generate_markdown_report(report))
    
    if args.save_report:
        await runner.save_report(report)
    
    # Return non-zero exit code if pass rate is below threshold
    if report.pass_rate < 0.7:
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
