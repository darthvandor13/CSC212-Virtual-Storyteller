##! @file chatgpt_webhook.py
##! @brief  Flask webhook that turns a single keyword into a children’s story
##!         using the OpenAI ChatCompletion API, with enhanced error handling.
##!
##! This refactored version wraps the Flask instance and OpenAI logic in small,
##! documented helper functions for Doxygen API reference generation.
##! Runtime behaviour aims for robustness, especially in handling API calls
##! and providing informative error feedback.
##! Run `python chatgpt_webhook.py` for a local server on port 5000.
##!
##! @author   Calvin Vandor
##! @date     2025-05-10
##! @version  1.1
##! @copyright MIT License
##!
##! ### Environment variables
##! * **AI_STORYTELLER_TEST_KEY_CV** – Your OpenAI API key (secret).
##!
##! ### Example (curl)
##! ```bash
##! curl -X POST http://localhost:5000/generate_story \
##!      -H "Content-Type: application/json" \
##!      -d '{"word": "dragon"}'
##! ```
##! returns (on success): `{ "story": "Once upon a time there was a friendly dragon..." }`
##! or (on error): `{ "story": "Error: ..." }`

from __future__ import annotations # For postponed evaluation of type hints

import os
import requests
from flask import Flask, jsonify, request
from typing import Dict, Any, Optional # Changed str | None to Optional[str]

__all__ = ["create_app", "generate_story"]


# --- Configuration & Global Setup ---

## @var _OPENAI_API_URL
# @brief OpenAI ChatCompletion API endpoint. (Internal constant)
_OPENAI_API_URL: str = "https://api.openai.com/v1/chat/completions"

## @var _REQUEST_TIMEOUT
# @brief Default timeout in seconds for requests to the OpenAI API. (Internal constant)
_REQUEST_TIMEOUT: int = 30 # seconds

# Early warning if the primary API key environment variable is not set
if not os.getenv("AI_STORYTELLER_TEST_KEY_CV"):
    print("⚠️ WARNING: Environment variable AI_STORYTELLER_TEST_KEY_CV is not set. "
          "OpenAI calls will fail unless an API key is provided directly to generate_story().")

# --- Helper Functions ---

def _openai_headers(api_key: str) -> Dict[str, str]:
    """
    Constructs the required HTTP headers for an OpenAI API request.

    @param api_key The OpenAI API secret key.
    @return A dictionary containing the authorization and content-type headers.
    """
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def generate_story(keyword: str, *, api_key: Optional[str] = None, model: str = "gpt-4o-mini") -> str:
    """
    Calls the OpenAI ChatCompletion API to generate a short children’s story based on a keyword.

    This function handles API key retrieval (favoring a passed key, then an environment variable),
    constructs the prompt, makes the HTTP request, and processes the response, including
    comprehensive error handling.

    @param keyword The topic or noun for the story (e.g., "robot", "adventure").
    @param api_key Optional override for the OpenAI API key. If None, uses AI_STORYTELLER_TEST_KEY_CV env var.
    @param model The OpenAI ChatCompletion model to use (default: "gpt-4o-mini").
    @return The generated story text as a string, or an error message string if generation fails.
    """
    effective_api_key = api_key or os.getenv("AI_STORYTELLER_TEST_KEY_CV")

    if not effective_api_key:
        print("❌ Error in generate_story: OpenAI API key is not configured or provided.")
        return "Error: API key not set. Please configure the AI_STORYTELLER_TEST_KEY_CV environment variable."

    request_body: Dict[str, Any] = {
        "model": model,
        "messages": [
            {
                "role": "system", # Using system role for broader instruction
                "content": "You are a creative storyteller for children."
            },
            {
                "role": "user",
                "content": f"Tell a short, imaginative children's story about {keyword}. Keep it under 5 paragraphs."
            }
        ],
        # "max_tokens": 250, # Optional: to control length further
        # "temperature": 0.7 # Optional: to control creativity
    }

    print(f"ℹ️ Sending prompt to OpenAI (model: {model}): '... about {keyword}'")

    try:
        resp = requests.post(
            _OPENAI_API_URL,
            headers=_openai_headers(effective_api_key),
            json=request_body,
            timeout=_REQUEST_TIMEOUT
        )

        if resp.status_code == 200:
            try:
                data = resp.json()
                # Standard OpenAI chat completion response structure
                story_content = data["choices"][0]["message"]["content"].strip()
                print(f"✅ OpenAI story generated successfully for '{keyword}'.")
                return story_content
            except (ValueError, KeyError, IndexError) as e:
                # Error parsing valid JSON response or unexpected structure
                print(f"❌ Error parsing successful OpenAI response: {e}\nResponse text: {resp.text[:500]}")
                return "Error: Received an unexpected or malformed response from the story generation service."
        else:
            # OpenAI API returned a non-200 status code (e.g., 401, 429, 500)
            error_details = resp.text[:500] # Log first 500 chars of error body
            print(f"❌ OpenAI API Error. Status: {resp.status_code}, Response: {error_details}")
            return f"Error {resp.status_code}: The story generation service reported an issue. Please check server logs for details."

    except requests.exceptions.Timeout:
        print(f"❌ OpenAI request timed out after {_REQUEST_TIMEOUT} seconds for URL: {_OPENAI_API_URL}")
        return "Error: The story generation service took too long to respond. Please try again later."
    except requests.exceptions.ConnectionError as e:
        print(f"❌ OpenAI connection error: {e}")
        return "Error: Could not connect to
