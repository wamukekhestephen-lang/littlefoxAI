#!/usr/bin/env python3
import sys
import json
import logging

# Setup logging to see errors
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    # Test imports
    logger.info("Importing modules...")
    from web_search import search_web, fetch_page
    from groq_client import groq_response_streaming
    logger.info("Imports successful")
    
    # Test search_web
    logger.info("Testing search_web...")
    results = search_web("hello", max_results=1)
    logger.info(f"search_web returned: {type(results)} with {len(results) if results else 0} results")
    
    # Test groq_response_streaming
    logger.info("Testing groq_response_streaming...")
    response_iter = groq_response_streaming("Say hello")
    logger.info(f"groq_response_streaming returned: {type(response_iter)}")
    
    # Try to get first chunk
    chunks = []
    for i, chunk in enumerate(response_iter):
        logger.info(f"Got chunk {i}: {chunk}")
        chunks.append(chunk)
        if i >= 2:  # Just test first 3 chunks
            break
    logger.info(f"Got {len(chunks)} chunks total")
    
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
    sys.exit(1)

logger.info("All tests passed!")
