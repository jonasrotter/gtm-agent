"""
Test script for the PEV Orchestrator Agent.

Run with: python scripts/test_pev_agent.py

Make sure the FastAPI server is running first:
  uvicorn src.api.main:app --port 8000
"""

import asyncio
import json
import time
from dataclasses import dataclass

import httpx


BASE_URL = "http://localhost:8000"


@dataclass
class TestQuestion:
    name: str
    query: str
    expected_tools: list[str]
    description: str


# Test questions to validate the PEV workflow
TEST_QUESTIONS = [
    TestQuestion(
        name="Simple Research",
        query="What is Azure Functions?",
        expected_tools=["researcher"],
        description="Simple 1-step research query",
    ),
    TestQuestion(
        name="Architecture Best Practices",
        query="What are the best practices for Azure Cosmos DB multi-region deployment?",
        expected_tools=["researcher", "architect"],
        description="Research + Architecture guidance",
    ),
    TestQuestion(
        name="Code Generation",
        query="Generate Azure CLI commands to create an Azure Function App with Python runtime",
        expected_tools=["code", "ghcp_coding"],
        description="Code/CLI generation task",
    ),
    TestQuestion(
        name="Complex Multi-Step",
        query="I need to design a serverless architecture for an e-commerce platform. Research the best Azure services, provide architecture recommendations following WAF pillars, and generate the deployment CLI commands.",
        expected_tools=["researcher", "architect", "ghcp_coding"],
        description="Complex query requiring all 3 sub-agents",
    ),
]


async def test_health():
    """Check if the server is healthy."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/agent/health", timeout=5.0)
            if response.status_code == 200:
                print("✅ Server is healthy")
                return True
            else:
                print(f"❌ Server returned {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Server not reachable: {e}")
            return False


async def test_query(question: TestQuestion, session_id: str | None = None):
    """Test a single query and display results."""
    print(f"\n{'='*60}")
    print(f"📝 TEST: {question.name}")
    print(f"   {question.description}")
    print(f"{'='*60}")
    print(f"Query: {question.query[:100]}...")
    print()
    
    async with httpx.AsyncClient() as client:
        start = time.perf_counter()
        
        try:
            response = await client.post(
                f"{BASE_URL}/agent/query",
                json={"content": question.query, "session_id": session_id},
                timeout=180.0,  # 3 minutes for complex queries
            )
            
            elapsed = time.perf_counter() - start
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ SUCCESS ({elapsed:.1f}s)")
                print(f"\n📊 PEV Metrics:")
                print(f"   • Verification Score: {data.get('verification_score', 'N/A')}")
                print(f"   • Iterations Used: {data.get('iterations_used', 'N/A')}")
                print(f"   • Requires Human Review: {data.get('requires_human_review', False)}")
                print(f"   • Plan Summary: {data.get('plan_summary', 'N/A')}")
                print(f"   • Agent(s) Used: {data.get('agent_used', 'N/A')}")
                print(f"   • Processing Time: {data.get('processing_time_ms', 'N/A')}ms")
                print(f"   • Session ID: {data.get('session_id', 'N/A')}")
                
                print(f"\n📄 Response Preview (first 500 chars):")
                content = data.get('content', '')
                print(f"   {content[:500]}...")
                
                return data
            else:
                print(f"❌ FAILED: HTTP {response.status_code}")
                print(f"   {response.text}")
                return None
                
        except httpx.TimeoutException:
            print(f"❌ TIMEOUT after {time.perf_counter() - start:.1f}s")
            return None
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return None


async def run_tests():
    """Run all test questions."""
    print("\n" + "="*60)
    print("🚀 PEV ORCHESTRATOR AGENT TEST SUITE")
    print("="*60)
    
    # Check health first
    if not await test_health():
        print("\n⚠️  Server not running. Start it with:")
        print("   uvicorn src.api.main:app --port 8000")
        return
    
    # Run test questions
    results = []
    for question in TEST_QUESTIONS:
        result = await test_query(question)
        results.append((question.name, result is not None))
        
        # Small delay between tests
        await asyncio.sleep(1)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {name}")
    
    print(f"\n   Total: {passed}/{total} passed")


if __name__ == "__main__":
    asyncio.run(run_tests())
