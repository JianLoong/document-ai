import asyncio
from fastmcp import FastMCP

from confluence import get_contents_search_term

# load_dotenv()

mcp = FastMCP("Confluence MCP")


@mcp.tool
def get_all_page_contents_by_search_term(search_term: str) -> str:
    """
    Searches Confluence for pages matching the search term and returns a single string containing the HTML contents of up to 5 pages.

    Args:
        search_term (str): The text to search for in Confluence pages.

    Returns:
        str: Concatenated HTML content of all matching pages, separated by double newlines.
    """

    return get_contents_search_term(search_term)


def main():
    asyncio.run(mcp.run(transport="stdio"))


if __name__ == "__main__":
    main()
