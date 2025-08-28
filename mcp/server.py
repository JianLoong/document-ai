import asyncio
import html
import http
import json
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
import urllib3

load_dotenv()

mcp = FastMCP("Confluence MCP")


def _get_confluence_conn_and_headers():
    """
    Establishes an HTTPS connection to the Confluence API using environment variables for configuration.
    Returns a tuple of (HTTPSConnection, headers dict) for making authenticated API requests.
    - base_url: Set by the CONFLUENCE_BASE_URL environment variable (default: 'jianloongliew.atlassian.net').
    - api_key: Set by the CONFLUENCE_API_KEY environment variable (must be provided).
    The headers include Basic authentication and content-type for JSON.
    """
    base_url = os.getenv("CONFLUENCE_BASE_URL", "jianloongliew.atlassian.net")
    api_key = os.getenv("CONFLUENCE_API_KEY")
    conn = http.client.HTTPSConnection(base_url)
    headers = {
        "authorization": f"Basic {api_key}",
        "content-type": "application/json",
    }
    return conn, headers


def get_all_page_contents_by_search_term(search_term):
    """
    Searches Confluence for pages matching the given search term using the CQL API.
    For each result (up to the specified limit), fetches the full HTML content of the page.

    Args:
        search_term (str): The text to search for in Confluence pages. Special characters are HTML-escaped and the query is URL-encoded.

    Returns:
        list of tuples: Each tuple contains (page_id, title, html_content) for a matching page.
    """
    import urllib.parse
    import html

    escaped_search_term = html.escape(search_term)
    cql_query = f'text ~ "{escaped_search_term}"'
    encoded_cql = urllib.parse.quote(cql_query, safe="")
    conn, headers = _get_confluence_conn_and_headers()
    conn.request(
        "GET",
        f"/wiki/rest/api/content/search?cql={encoded_cql}&limit={10}",
        headers=headers,
    )
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data.decode("utf-8"))
    results = result.get("results", [])
    page_contents = []
    for page in results:
        page_id = page.get("id")
        title = page.get("title")
        if not page_id:
            continue
        conn.request(
            "GET",
            f"/wiki/rest/api/content/{page_id}?expand=body.storage",
            headers=headers,
        )
        res = conn.getresponse()
        data = res.read()
        page_result = json.loads(data.decode("utf-8"))
        html_content = page_result.get("body", {}).get("storage", {}).get("value", "")
        page_contents.append((page_id, title, html_content))
    return page_contents


def get_first_page_content_by_search_term(search_term):
    """
    Searches Confluence for the first page matching the given search term using the CQL API.
    Fetches and returns the full HTML content of the first matching page.

    Args:
        search_term (str): The text to search for in Confluence pages. Special characters are HTML-escaped and the query is URL-encoded.

    Returns:
        str: The HTML content of the first matching page, or an empty string if no results are found.
    """
    escaped_search_term = html.escape(search_term)
    cql_query = f'text ~ "{escaped_search_term}"'
    encoded_cql = urllib3.parse.quote(cql_query, safe="")
    conn, headers = _get_confluence_conn_and_headers()
    conn.request(
        "GET",
        f"/wiki/rest/api/content/search?cql={encoded_cql}&limit=1",
        headers=headers,
    )
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data.decode("utf-8"))
    results = result.get("results", [])
    if not results:
        return ""
    page_id = results[0].get("id")
    if not page_id:
        return ""
    # Fetch the page content
    conn.request(
        "GET", f"/wiki/rest/api/content/{page_id}?expand=body.storage", headers=headers
    )
    res = conn.getresponse()
    data = res.read()
    page_result = json.loads(data.decode("utf-8"))
    return page_result.get("body", {}).get("storage", {}).get("value", "")


def get_confluence_page_content(page_id):
    """
    Fetches the HTML content of a Confluence page by its page ID.

    Args:
        page_id (str): The unique identifier of the Confluence page.

    Returns:
        str: The HTML content of the page, or an empty string if not found.
    """
    conn, headers = _get_confluence_conn_and_headers()
    conn.request(
        "GET", f"/wiki/rest/api/content/{page_id}?expand=body.storage", headers=headers
    )
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data.decode("utf-8"))
    return result.get("body", {}).get("storage", {}).get("value", "")


@mcp.tool
def get_contents_search_term(search_term: str) -> str:
    """
    Searches Confluence for pages matching the search term and returns a single string containing the HTML contents of up to 5 pages.

    Args:
        search_term (str): The text to search for in Confluence pages.

    Returns:
        str: Concatenated HTML content of all matching pages, separated by double newlines.
    """
    results = ""
    pages = get_all_page_contents_by_search_term(search_term)
    for pid, title, html in pages:
        content = get_confluence_page_content(pid)
        results += content + "\n\n"
    return results.strip()


def main():
    asyncio.run(mcp.run(transport="stdio"))


if __name__ == "__main__":
    main()
