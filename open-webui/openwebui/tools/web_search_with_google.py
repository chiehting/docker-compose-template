"""
title: Google Search Tool
description: This tool performs Google searches to get real-time information from the internet using the Google Search API
required_open_webui_version: 0.4.0
requirements: google-api-python-client
version: 1.0.0
licence: MIT
"""

from pydantic import BaseModel, Field
from googleapiclient.discovery import build
from typing import List, Dict, Optional


class Tools:
    def __init__(self):
        """Initialize the Tool with valves."""
        self.valves = self.Valves()

    class Valves(BaseModel):
        google_api_key: str = Field("", description="Your Google API key")
        custom_search_engine_id: str = Field(
            "", description="Your Google Custom Search Engine ID"
        )
        max_results: int = Field(
            5, description="Maximum number of search results to return (1-10)"
        )

    async def search(
        self, query: str, num_results: Optional[int] = None, __event_emitter__=None
    ) -> str:
        """
        Perform a Google search and return the results.

        Args:
            query: The search query string
            num_results: Optional number of results to return (defaults to max_results valve)

        Returns:
            A formatted string containing the search results
        """ 
        try:
            # Input validation
            if not self.valves.google_api_key:
                return "Error: Google API key not configured. Please set up the API key in the tool settings."

            if not self.valves.custom_search_engine_id:
                return "Error: Custom Search Engine ID not configured. Please set up the CSE ID in the tool settings."

            # Emit status that search is starting
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "Initiating Google search...",
                            "done": False,
                        },
                    }
                )

            # Build the Google Custom Search API service
            service = build(
                "customsearch", "v1", developerKey=self.valves.google_api_key
            )

            # Set number of results
            n_results = min(
                num_results if num_results is not None else self.valves.max_results,
                10,  # Google API maximum
            )

            # Perform the search
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "Fetching search results...",
                            "done": False,
                        },
                    }
                )

            result = (
                service.cse()
                .list(q=query, cx=self.valves.custom_search_engine_id, num=n_results)
                .execute()
            )

            # Process results
            if "items" not in result:
                return "No results found for the given query."

            # Format results
            formatted_results = "Search Results:\n\n"
            for i, item in enumerate(result["items"], 1):
                formatted_results += f"{i}. {item['title']}\n"
                formatted_results += f"URL: {item['link']}\n"
                if "snippet" in item:
                    formatted_results += f"Description: {item['snippet']}\n"
                formatted_results += "\n"

            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "Search completed successfully",
                            "done": True,
                        },
                    }
                )

            return formatted_results

        except Exception as e:
            error_message = f"An error occurred while performing the search: {str(e)}"
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {"description": error_message, "done": True},
                    }
                )
            return error_message
