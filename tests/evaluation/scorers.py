"""
Scoring functions for evaluation metrics.

Each scorer calculates a score between 0.0 and 1.0 for a specific dimension
of the evaluation.
"""

import re
from typing import Any


def score_routing(expected: str | None, actual: str | None) -> float:
    """
    Score routing accuracy.
    
    Args:
        expected: Expected routing category (e.g., "FACTUAL", "HOWTO")
        actual: Actual routing category from classifier
        
    Returns:
        1.0 if exact match, 0.0 otherwise
    """
    if expected is None or actual is None:
        return 1.0  # No routing expectation
    
    # Normalize for comparison
    expected_norm = expected.upper().strip()
    actual_norm = actual.upper().strip()
    
    return 1.0 if expected_norm == actual_norm else 0.0


def score_tool_selection(
    expected_tools: list[str],
    actual_tools: list[str],
    require_all: bool = False,
) -> float:
    """
    Score tool selection accuracy.
    
    Args:
        expected_tools: List of expected tool names
        actual_tools: List of actually used tool names
        require_all: If True, all expected tools must be used.
                    If False, at least one expected tool must be used.
                    
    Returns:
        Score between 0.0 and 1.0
    """
    if not expected_tools:
        return 1.0  # No tool expectations
    
    if not actual_tools:
        return 0.0  # Expected tools but none used
    
    # Normalize tool names
    expected_set = {t.lower().strip() for t in expected_tools}
    actual_set = {t.lower().strip() for t in actual_tools}
    
    if require_all:
        # All expected tools must be present
        matched = len(expected_set & actual_set)
        return matched / len(expected_set)
    else:
        # At least one expected tool must be present
        if expected_set & actual_set:
            # Bonus for using more expected tools
            matched = len(expected_set & actual_set)
            return min(1.0, 0.5 + (matched / len(expected_set)) * 0.5)
        return 0.0


def score_keywords(
    response: str,
    expected_keywords: list[str],
    case_sensitive: bool = False,
) -> float:
    """
    Score keyword coverage in response.
    
    Args:
        response: The response text to search
        expected_keywords: List of keywords that should appear
        case_sensitive: Whether to match case-sensitively
        
    Returns:
        Fraction of keywords found (0.0 to 1.0)
    """
    if not expected_keywords:
        return 1.0  # No keyword expectations
    
    if not response:
        return 0.0
    
    search_text = response if case_sensitive else response.lower()
    
    found = 0
    for keyword in expected_keywords:
        search_keyword = keyword if case_sensitive else keyword.lower()
        if search_keyword in search_text:
            found += 1
    
    return found / len(expected_keywords)


def score_citations(
    response: str,
    requires_citations: bool,
) -> float:
    """
    Score presence and quality of citations.
    
    Args:
        response: The response text to check
        requires_citations: Whether citations are expected
        
    Returns:
        Score based on citation presence and quality
    """
    if not requires_citations:
        return 1.0  # No citation requirement
    
    if not response:
        return 0.0
    
    # Look for URL patterns (Microsoft Learn, Azure docs, etc.)
    url_patterns = [
        r"https?://learn\.microsoft\.com[^\s\)\"\']+",
        r"https?://docs\.microsoft\.com[^\s\)\"\']+",
        r"https?://azure\.microsoft\.com[^\s\)\"\']+",
        r"https?://[^\s\)\"\']*microsoft[^\s\)\"\']+",
    ]
    
    urls_found = []
    for pattern in url_patterns:
        urls_found.extend(re.findall(pattern, response, re.IGNORECASE))
    
    if not urls_found:
        # Check for reference markers like [1], [Source], etc.
        ref_patterns = [
            r"\[\d+\]",
            r"\[Source\]",
            r"\[Reference\]",
            r"Source:",
            r"Reference:",
        ]
        for pattern in ref_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return 0.5  # Partial credit for reference markers
        return 0.0
    
    # Score based on number and quality of citations
    unique_urls = set(urls_found)
    
    if len(unique_urls) >= 3:
        return 1.0
    elif len(unique_urls) == 2:
        return 0.9
    elif len(unique_urls) == 1:
        return 0.7
    
    return 0.5


def score_code_quality(
    response: str,
    has_code_expected: bool,
    code_patterns: list[str] | None = None,
) -> float:
    """
    Score code generation quality.
    
    Args:
        response: The response text containing code
        has_code_expected: Whether code is expected in the response
        code_patterns: Optional list of patterns that should appear in code
        
    Returns:
        Score based on code presence and quality
    """
    if not has_code_expected:
        return 1.0  # No code expectation
    
    if not response:
        return 0.0
    
    # Check for code blocks
    code_block_patterns = [
        r"```[\w]*\n[\s\S]*?```",  # Markdown code blocks
        r"<code>[\s\S]*?</code>",  # HTML code tags
    ]
    
    code_blocks = []
    for pattern in code_block_patterns:
        code_blocks.extend(re.findall(pattern, response))
    
    if not code_blocks:
        # Check for inline code indicators
        if "`" in response or "az " in response.lower():
            score = 0.3  # Partial credit for inline code
        else:
            return 0.0
    else:
        score = 0.6  # Base score for having code blocks
    
    # Check for expected patterns in code
    if code_patterns:
        code_text = " ".join(code_blocks) if code_blocks else response
        patterns_found = sum(
            1 for p in code_patterns 
            if p.lower() in code_text.lower()
        )
        pattern_score = patterns_found / len(code_patterns)
        score += pattern_score * 0.4
    else:
        score += 0.4  # No specific patterns required
    
    return min(1.0, score)


def score_performance(
    actual_duration: float,
    max_duration: float | None,
) -> float:
    """
    Score performance based on execution time.
    
    Args:
        actual_duration: Actual execution duration in seconds
        max_duration: Maximum expected duration in seconds
        
    Returns:
        Score based on how well duration met expectations
    """
    if max_duration is None:
        return 1.0  # No duration expectation
    
    if actual_duration <= max_duration:
        # Bonus for being significantly faster
        ratio = actual_duration / max_duration
        if ratio <= 0.5:
            return 1.0
        elif ratio <= 0.75:
            return 0.95
        else:
            return 0.9
    else:
        # Penalty for being slower
        overage_ratio = actual_duration / max_duration
        if overage_ratio <= 1.25:
            return 0.7
        elif overage_ratio <= 1.5:
            return 0.5
        elif overage_ratio <= 2.0:
            return 0.3
        else:
            return 0.1


def score_efficiency(
    actual_tool_calls: int,
    max_tool_calls: int | None,
    min_tool_calls: int = 1,
) -> float:
    """
    Score efficiency based on number of tool calls.
    
    Args:
        actual_tool_calls: Actual number of tool calls made
        max_tool_calls: Maximum expected tool calls
        min_tool_calls: Minimum expected tool calls (default 1)
        
    Returns:
        Score based on tool call efficiency
    """
    if max_tool_calls is None:
        return 1.0  # No efficiency expectation
    
    if actual_tool_calls == 0:
        return 0.0  # Should have made at least one call
    
    if actual_tool_calls <= max_tool_calls:
        # Good - within budget
        if actual_tool_calls >= min_tool_calls:
            return 1.0
        else:
            return 0.8  # Slightly penalize for too few calls
    else:
        # Over budget
        overage = actual_tool_calls - max_tool_calls
        penalty = overage * 0.15
        return max(0.2, 1.0 - penalty)


def score_waf_reference(
    response: str,
    requires_waf: bool,
) -> float:
    """
    Score Well-Architected Framework reference presence.
    
    Args:
        response: The response text to check
        requires_waf: Whether WAF reference is expected
        
    Returns:
        Score based on WAF pillar mentions
    """
    if not requires_waf:
        return 1.0  # No WAF requirement
    
    if not response:
        return 0.0
    
    # WAF pillars
    pillars = [
        "reliability",
        "security",
        "cost optimization",
        "operational excellence",
        "performance efficiency",
    ]
    
    # Also check for common WAF terms
    waf_terms = [
        "well-architected",
        "waf",
        "azure architecture center",
        "best practice",
    ]
    
    response_lower = response.lower()
    
    # Check for pillar mentions
    pillars_found = sum(1 for p in pillars if p in response_lower)
    
    # Check for WAF terms
    waf_terms_found = sum(1 for t in waf_terms if t in response_lower)
    
    if pillars_found >= 2 or waf_terms_found >= 2:
        return 1.0
    elif pillars_found >= 1 or waf_terms_found >= 1:
        return 0.7
    else:
        return 0.0


def calculate_task_scores(
    result: dict[str, Any],
    task: dict[str, Any],
) -> dict[str, float]:
    """
    Calculate all scores for a task evaluation result.
    
    Args:
        result: Dictionary containing evaluation result data
        task: Dictionary containing task definition and expectations
        
    Returns:
        Dictionary of score names to score values
    """
    expected = task.get("expected", {})
    
    scores = {
        "routing_score": score_routing(
            expected.get("routing"),
            result.get("actual_routing"),
        ),
        "tool_selection_score": score_tool_selection(
            expected.get("tools", []),
            result.get("actual_tools", []),
        ),
        "keyword_coverage_score": score_keywords(
            result.get("response_text", ""),
            expected.get("keywords", []),
        ),
        "citation_score": score_citations(
            result.get("response_text", ""),
            expected.get("has_citations", False),
        ),
        "code_quality_score": score_code_quality(
            result.get("response_text", ""),
            expected.get("has_code_block", False),
            expected.get("code_patterns"),
        ),
        "performance_score": score_performance(
            result.get("duration_seconds", 0),
            expected.get("max_duration_seconds"),
        ),
        "efficiency_score": score_efficiency(
            len(result.get("tool_invocations", [])),
            expected.get("max_tool_calls"),
        ),
    }
    
    # Add WAF score if applicable
    if expected.get("has_waf_reference"):
        scores["waf_reference_score"] = score_waf_reference(
            result.get("response_text", ""),
            True,
        )
    
    return scores
