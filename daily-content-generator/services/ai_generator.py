import os
import datetime
import google.generativeai as genai
from typing import Dict, Any
import time
import json
import logging
from google.generativeai import types
from google.generativeai.client import Client

from ..config import settings

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
try:
    genai.configure(api_key=settings.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    logging.info("Successfully initialized Google Generative AI client and model.")
except Exception as e:
    logging.error(f"Error initializing Google Generative AI: {e}")
    raise

def generate_personalized_content(user_name: str, birth_details: Dict[str, Any], preferences: Dict[str, Any], retries=3, delay=5) -> Dict[str, Any]:
    """Generate personalized daily content using Google's Generative AI."""
    logging.info(f"Generating content for {user_name}...")
    
    # Construct a more structured prompt
    prompt = f"""
    Generate a personalized astrological reading for {user_name} for today, {datetime.date.today()}.
    
    **User's Birth Details:**
    - Date: {birth_details.get('date')}
    - Time: {birth_details.get('time')}
    - Location: {birth_details.get('location')}
    
    **User's Preferences:**
    - Focus Areas: {', '.join(preferences.get('focus_areas', ['General', 'Career', 'Love']))}
    
    **Instructions:**
    Please provide a JSON object with the following keys:
    - "daily_overview": A brief, engaging summary for the day.
    - "focus_areas": A dictionary with keys for each focus area (e.g., "Career", "Love", "Health") and a paragraph for each.
    - "planetary_influences": A description of the key planetary influences for the day.
    - "advice": A short, actionable piece of advice.
    
    Example JSON output:
    {{
      "daily_overview": "Today is a day of potential breakthroughs...",
      "focus_areas": {{
        "Career": "Your hard work may be noticed by superiors...",
        "Love": "Communication is key in your relationships today...",
        "Health": "Focus on mindfulness and light exercise."
      }},
      "planetary_influences": "The Moon in Taurus brings a grounding energy...",
      "advice": "Take a moment to appreciate the small joys today."
    }}
    """
    
    generation_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
    )

    for attempt in range(retries):
        try:
            response = model.generate_content(
                contents=prompt,
                generation_config=generation_config
            )
            
            # Clean and parse the JSON response
            cleaned_response = response.text.strip().replace('`', '').replace('json', '')
            parsed_content = json.loads(cleaned_response)
            
            # Structure the final content
            content = {
                'date': str(datetime.date.today()),
                'generated_for': user_name,
                'reading': parsed_content
            }
            return content
            
        except (json.JSONDecodeError, Exception) as e:
            logging.error(f"Error generating content on attempt {attempt + 1} for user {user_name}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                logging.error(f"Failed to generate content for user {user_name} after multiple retries.")
                raise Exception("Failed to generate content after multiple retries.")
    return None
