import asyncio
from fastmcp.client import Client


async def main():
    client = Client("http://localhost:8005/mcp/")

    async with client:
        # add note
        res1 = await client.call_tool("add_note", {
            "id": "1",
            "text": "hello mcp"
        })
        print("ADD:", res1)

        # search
        res2 = await client.call_tool("search_notes", {
            "query": "hello",
            "k": 3
        })
        print("SEARCH:", res2)


if __name__ == "__main__":
    asyncio.run(main())