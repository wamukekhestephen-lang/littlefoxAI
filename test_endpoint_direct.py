#!/usr/bin/env python3
"""Test /ask endpoint generator directly"""
import sys
import logging
from io import StringIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('test')

# Import what we need
from groq_client import groq_response_streaming
from web_search import search_web, fetch_page

def is_browsing_query(text: str) -> bool:
    text = text.lower().strip()
    if text in {"hi", "hello", "hey", "yo", "sup"}:
        return False
    if len(text.split()) <= 2:
        return False
    if text.startswith(("hi ", "hello ", "hey ")):
        return False
    return True

# Test conversational path
user_input = "hey"
logger.info(f"Testing with input: {user_input}")

# Check if it's a browsing query
is_browse = is_browsing_query(user_input)
logger.info(f"is_browsing_query returned: {is_browse}")

if not is_browse:
    logger.info("[GROQ] starting streaming")
    try:
        for i, chunk in enumerate(groq_response_streaming(
            f"Respond naturally and conversationally to: {user_input}"
        )):
            logger.info(f"[GROQ] chunk {i}: {chunk}")
            if i >= 3:  # Just test first few chunks
                break
        logger.info("✓ Conversational path works!")
    except Exception as e:
        logger.error(f"✗ Error in streaming: {e}", exc_info=True)
        sys.exit(1)
else:
    logger.info("Query is a browsing query - skipping this test")

logger.info("\n✓ ALL TESTS PASSED!")
