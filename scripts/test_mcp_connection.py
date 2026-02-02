"""Test MCPStreamableHTTPTool connection to Microsoft Learn MCP."""
import asyncio
from agent_framework import MCPStreamableHTTPTool

async def test_mcp_connection():
    """Test direct connection to Microsoft Learn MCP."""
    print("Creating MCPStreamableHTTPTool...")
    
    mcp = MCPStreamableHTTPTool(
        name="microsoft_learn",
        url="https://learn.microsoft.com/api/mcp",
        timeout=30.0,
        sse_read_timeout=30.0,
    )
    
    print(f"MCP tool created: {mcp.name}")
    print(f"URL: {mcp.url}")
    
    try:
        print("\nEntering async context...")
        async with mcp:
            print("✅ MCP context entered successfully!")
            print(f"is_connected: {mcp.is_connected}")
            
            # Check functions (tools)
            if hasattr(mcp, 'functions') and mcp.functions:
                print(f"\n✅ {len(mcp.functions)} tools loaded from MCP:")
                for func in mcp.functions:
                    name = getattr(func, 'name', 'unknown')
                    desc = getattr(func, 'description', '')[:80] if hasattr(func, 'description') else ''
                    print(f"  - {name}: {desc}...")
                
                # Try to call a tool directly
                print("\n--- Testing tool call ---")
                search_tool = mcp.functions[0]  # microsoft_docs_search
                print(f"Calling {search_tool.name}...")
                try:
                    result = await search_tool(query="Azure Blob Storage")
                    print(f"Result type: {type(result)}")
                    if isinstance(result, list):
                        for item in result[:2]:
                            print(f"  Item type: {type(item)}")
                            if hasattr(item, 'text'):
                                print(f"  Text (first 300 chars): {item.text[:300]}...")
                            elif hasattr(item, 'content'):
                                print(f"  Content: {item.content[:300]}...")
                    else:
                        print(f"Result: {str(result)[:500]}")
                except Exception as e:
                    print(f"❌ Tool call failed: {type(e).__name__}: {e}")
            else:
                print("\n❌ No functions/tools found")
                
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}")
        print(f"Message: {e}")
        
        # Check if it's a connection issue
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_connection())
