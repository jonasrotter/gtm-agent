"""Quick script to run CODE category tests."""
import asyncio
import httpx
import time

CODE_TESTS = [
    {"name": "code_python_blob", "query": "Write Python code to upload a file to Azure Blob Storage using the SDK"},
    {"name": "code_bicep_webapp", "query": "Generate Bicep code to deploy an Azure App Service with a SQL Database"},
    {"name": "code_cli_commands", "query": "Give me the Azure CLI commands to create a storage account with private endpoint"},
    {"name": "code_terraform_aks", "query": "Create Terraform code to deploy an AKS cluster with managed identity"},
]


async def run_code_tests():
    print("=" * 60)
    print("Running CODE Tests")
    print("=" * 60)
    
    results = []
    
    for test in CODE_TESTS:
        print(f"\n{'='*60}")
        print(f"Test: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        print("-" * 60)
        
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=600.0) as client:
                response = await client.post(
                    "http://localhost:8000/agent/query",
                    json={"content": test["query"]}  # API expects 'content' not 'query'
                )
                duration = time.time() - start
                
                if response.status_code == 200:
                    data = response.json()
                    score = data.get("score")
                    iterations = data.get("iterations", 0)
                    agents = data.get("agents_used", [])
                    resp_text = str(data.get("response", ""))[:200]
                    
                    print(f"  Duration: {duration:.1f}s")
                    print(f"  Iterations: {iterations}")
                    print(f"  Score: {score}")
                    print(f"  Agents: {agents}")
                    print(f"  Response: {resp_text}...")
                    print("  ✅ PASSED")
                    results.append({"name": test["name"], "status": "PASSED", "score": score, "duration": duration})
                else:
                    print(f"  Duration: {duration:.1f}s")
                    print(f"  ❌ FAILED: HTTP {response.status_code}")
                    print(f"  Error: {response.text[:300]}")
                    results.append({"name": test["name"], "status": "FAILED", "error": response.status_code, "duration": duration})
        except Exception as e:
            duration = time.time() - start
            print(f"  Duration: {duration:.1f}s")
            print(f"  ❌ ERROR: {str(e)[:200]}")
            results.append({"name": test["name"], "status": "ERROR", "error": str(e)[:100], "duration": duration})
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    passed = sum(1 for r in results if r["status"] == "PASSED")
    print(f"Passed: {passed}/{len(results)}")
    for r in results:
        status_icon = "✅" if r["status"] == "PASSED" else "❌"
        print(f"  {status_icon} {r['name']}: {r['status']} ({r['duration']:.1f}s)")


if __name__ == "__main__":
    asyncio.run(run_code_tests())
