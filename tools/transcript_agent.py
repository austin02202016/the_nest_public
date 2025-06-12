#!/usr/bin/env python3
"""
🎙️ Transcripts Tool – Query and analyze call transcripts

This module provides tools to interact with the transcripts database.
"""

import os
from typing import List, Dict
from dotenv import load_dotenv
from agno.tools import tool
import logging
from supabase import create_client, Client

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL", ""),
    os.getenv("SUPABASE_KEY", "")
)

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_AI_API_KEY", "")

def _get_transcripts_by_company(company: str) -> List[Dict]:
    """
    Get all transcripts associated with a specific company.
    
    Args:
        company (str): The company name
        
    Returns:
        List[Dict]: List of transcripts with their metadata
    """
    try:
        # First, find all rows for the specified company by iterating through the company_domain column
        response = supabase.table("transcripts") \
            .select("*") \
            .ilike("company_domain", f"%{company.lower()}%") \
            .order("created_at", desc=True) \
            .execute()
        
        # Extract the IDs of the found transcripts
        transcript_ids = [transcript['id'] for transcript in response.data]
        
        # Retrieve the transcripts by ID
        transcripts = []
        for transcript_id in transcript_ids:
            transcript_response = supabase.table("transcripts") \
                .select("*") \
                .eq("id", transcript_id) \
                .execute()
            if transcript_response.data:
                transcripts.extend(transcript_response.data)
        
        return transcripts
    except Exception as e:
        logger.error(f"Error fetching transcripts: {str(e)}")
        return []

@tool(name="get_transcripts", description="Get call transcripts for a specific company")
def get_transcripts(company: str = None) -> str:
    """
    Get call transcripts for a specific company.
    
    Args:
        company (str): The company name
        
    Returns:
        str: Formatted transcript information
    """
    if not company:
        return "Error: Please provide a company name."
    
    transcripts = _get_transcripts_by_company(company)
    
    if not transcripts:
        return f"No call transcripts were found for the company {company}. Please check for partial matches or similar company names."
    
    # Format the response
    result = []
    for transcript in transcripts:
        result.append(f"""
Transcript from {transcript['created_at']}:
Company Domain: {transcript.get('company_domain', 'Unknown')}
POC: {transcript['POC']}

Transcript:
{transcript['transcripts']}
---""")
    
    return "\n".join(result)

# Placeholder for future: get_transcripts_by_id (to be implemented) 