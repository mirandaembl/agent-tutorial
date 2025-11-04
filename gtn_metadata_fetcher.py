#!/usr/bin/env python3
"""
Simple script to fetch training material metadata from the Galaxy Training Network API.
API Documentation: https://training.galaxyproject.org/training-material/api/

Note: The GTN API is marked as UNSTABLE and subject to change without warning.
"""

import requests
import json
import sys
from typing import Dict, List, Any

class GTNMetadataFetcher:
    def __init__(self):
        self.base_url = "https://training.galaxyproject.org/training-material/api"

    def fetch_topics(self) -> List[Dict[str, Any]]:
        """Fetch all available topics."""
        url = f"{self.base_url}/topics.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_contributors(self) -> Dict[str, Any]:
        """Fetch all contributors."""
        url = f"{self.base_url}/contributors.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_topic_details(self, topic_id: str) -> Dict[str, Any]:
        """Fetch detailed information for a specific topic."""
        url = f"{self.base_url}/topics/{topic_id}.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_tutorial(self, topic_id: str, tutorial_id: str, material_type: str = "tutorial") -> Dict[str, Any]:
        """Fetch specific tutorial material."""
        url = f"{self.base_url}/topics/{topic_id}/tutorials/{tutorial_id}/{material_type}.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_top_tools(self) -> Dict[str, Any]:
        """Fetch tutorials organized by tool."""
        url = f"{self.base_url}/top-tools.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

def main():
    fetcher = GTNMetadataFetcher()

    try:
        print("Fetching Galaxy Training Network metadata...")
        print("=" * 50)

        # Fetch all topics
        print("\n📚 Fetching all topics...")
        topics = fetcher.fetch_topics()
        topics = [v for k, v in topics.items()]  # Convert dict to list
        print(f"Found {len(topics)} topics:")
        for topic in topics[:5]:  # Show first 5 topics
            print(f"  • {topic.get('name', 'N/A')} ({topic.get('title', 'N/A')})")
        if len(topics) > 5:
            print(f"  ... and {len(topics) - 5} more")

        # Fetch contributors
        print("\n👥 Fetching contributors...")
        contributors = fetcher.fetch_contributors()
        print(f"Found {len(contributors)} contributors")

        # Fetch top tools
        print("\n🔧 Fetching top tools...")
        top_tools = fetcher.fetch_top_tools()
        print(f"Found {len(top_tools)} tools with tutorials")

        # Example: Get details for first topic
        if topics:
            first_topic = topics[0]
            topic_id = first_topic.get('name')
            if topic_id:
                print(f"\n🔍 Fetching details for topic: {topic_id}")
                topic_details = fetcher.fetch_topic_details(topic_id)
                tutorials = topic_details.get('materials', [])
                print(f"  Topic has {len(tutorials)} tutorials")

                # Show first tutorial details
                if tutorials:
                    tutorial = tutorials[0]
                    print(f"  First tutorial: {tutorial.get('title', 'N/A')}")
                    print(f"  Duration: {tutorial.get('time_estimation', 'N/A')}")
                    print(f"  Hands-on: {'Yes' if tutorial.get('hands_on') else 'No'}")

        print(f"\n✅ Successfully fetched GTN metadata!")
        print("\nTo save data to files, modify the script to write JSON output.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()