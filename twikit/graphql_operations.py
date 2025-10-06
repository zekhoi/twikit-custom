"""
GraphQL Operation Fetcher with Caching

This module fetches GraphQL query IDs dynamically from Twitter's client-web JS bundle
and caches them to avoid hardcoding and frequent updates.
"""

from __future__ import annotations

import re
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client.client import Client

# Cache for GraphQL operations
_operations_cache: dict[str, str] = {}
_cache_timestamp: float = 0
_cache_ttl: int = 3600  # Cache for 1 hour


async def fetch_graphql_operations(client: Client) -> dict[str, str]:
    """
    Fetches GraphQL operation IDs from Twitter's main JavaScript bundle.

    Parameters
    ----------
    client : Client
        The client instance to use for HTTP requests.

    Returns
    -------
    dict[str, str]
        A dictionary mapping operation names to their query IDs.
    """
    global _operations_cache, _cache_timestamp

    # Check if cache is still valid
    current_time = time.time()
    if _operations_cache and (current_time - _cache_timestamp) < _cache_ttl:
        return _operations_cache

    # Fetch the main JS bundle
    url = 'https://abs.twimg.com/responsive-web/client-web/main.967bddca.js'

    try:
        response = await client.get(url)
        js_content = response.text

        # Extract GraphQL operations using regex
        # Pattern matches: queryId:"QUERY_ID",operationName:"OPERATION_NAME"
        pattern = r'queryId:"([a-zA-Z0-9_-]+)",operationName:"([a-zA-Z0-9_]+)"'
        matches = re.findall(pattern, js_content)

        # Build the operations dictionary
        operations = {operation_name: query_id for query_id, operation_name in matches}

        if operations:
            _operations_cache = operations
            _cache_timestamp = current_time
            return operations
        else:
            # If no operations found, return cached version if available
            if _operations_cache:
                return _operations_cache
            raise ValueError("No GraphQL operations found in JavaScript bundle")

    except Exception as e:
        # If fetch fails and we have a cache, return it
        if _operations_cache:
            return _operations_cache
        raise RuntimeError(f"Failed to fetch GraphQL operations: {e}")


async def get_query_id(client: Client, operation_name: str) -> str:
    """
    Gets the query ID for a specific GraphQL operation.

    Parameters
    ----------
    client : Client
        The client instance to use for HTTP requests.
    operation_name : str
        The name of the GraphQL operation.

    Returns
    -------
    str
        The query ID for the operation.

    Raises
    ------
    KeyError
        If the operation name is not found in the fetched operations.
    """
    operations = await fetch_graphql_operations(client)

    if operation_name not in operations:
        raise KeyError(f"GraphQL operation '{operation_name}' not found")

    return operations[operation_name]


def clear_cache() -> None:
    """Clears the GraphQL operations cache."""
    global _operations_cache, _cache_timestamp
    _operations_cache = {}
    _cache_timestamp = 0


def set_cache_ttl(ttl: int) -> None:
    """
    Sets the cache time-to-live in seconds.

    Parameters
    ----------
    ttl : int
        The time-to-live in seconds.
    """
    global _cache_ttl
    _cache_ttl = ttl
