"""Debug script for the failing code_python_blob test."""
import asyncio
import httpx

async def test():
    query = "Write Python code to upload a file to Azure Blob Storage using the azure-storage-blob SDK"
    
    async with httpx.AsyncClient(timeout=120) as client:
        print(f"Testing: {query}")
        print("-" * 60)
        
        try:
            response = await client.post(
                "http://localhost:8000/agent/query",
                json={"content": query}
            )
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:2000]}")
            
        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test())
