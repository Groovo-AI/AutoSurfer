from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from autosurfer.config import Config
from autosurfer.llm.response_schema.browser_actions import NextActions
from langchain_core.utils import get_from_env
import json
import re
from typing import Any, Dict


class GeminiStructuredWrapper:
    """Wrapper to handle Gemini's structured output more reliably"""
    
    def __init__(self, model):
        self.model = model
    
    def invoke(self, messages):
        # Get the raw response from Gemini
        response = self.model.invoke(messages)
        
        # Extract JSON from the response
        content = response.content if hasattr(response, 'content') else str(response)
        
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if not json_match:
            # If no JSON found, try to construct a basic response
            return self._create_fallback_response(content)
        
        try:
            # Parse the JSON
            json_str = json_match.group(0)
            parsed = json.loads(json_str)
            
            # Validate and fix the structure
            fixed_response = self._fix_response_structure(parsed)
            return NextActions(**fixed_response)
            
        except (json.JSONDecodeError, Exception) as e:
            # If parsing fails, create a fallback response
            return self._create_fallback_response(content)
    
    def _fix_response_structure(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Fix common issues in Gemini's response structure"""
        if "actions" not in response:
            return {"actions": []}
        
        fixed_actions = []
        for action_item in response["actions"]:
            if "action" not in action_item:
                continue
                
            action = action_item["action"]
            action_type = action.get("type")
            
            # Fix common field issues
            if action_type == "goto":
                # Ensure url field exists
                if "url" not in action and "summary" in action:
                    # Try to extract URL from summary or use a default
                    summary = action["summary"]
                    if "google" in summary.lower():
                        action["url"] = "https://google.com"
                    elif "instagram" in summary.lower():
                        action["url"] = "https://instagram.com"
                    else:
                        action["url"] = "https://google.com"
                # Remove invalid fields
                action = {"type": "goto", "url": action.get("url", "https://google.com")}
            
            elif action_type == "done":
                # Ensure summary field exists
                if "summary" not in action:
                    action["summary"] = "Task completed"
                action = {"type": "done", "summary": action["summary"]}
            
            # Add other action type fixes as needed
            
            fixed_action_item = {
                "thought": action_item.get("thought", "Performing action"),
                "action": action
            }
            fixed_actions.append(fixed_action_item)
        
        return {"actions": fixed_actions}
    
    def _create_fallback_response(self, content: str) -> NextActions:
        """Create a fallback response when parsing fails"""
        # Try to determine intent from content
        if "google" in content.lower():
            url = "https://google.com"
        elif "instagram" in content.lower():
            url = "https://instagram.com"
        else:
            url = "https://google.com"
        
        return NextActions(actions=[{
            "thought": "Navigating to the requested website",
            "action": {
                "type": "goto",
                "url": url
            }
        }])


def get_llm_client(client):
    if client == "openai":
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        openai_model = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
        )
        return openai_model.with_structured_output(NextActions)
    
    elif client == "gemini":
        if not Config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")

        gemini_model = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0,
            google_api_key=Config.GOOGLE_API_KEY,
        )
        
        # Use our custom wrapper for better handling
        return GeminiStructuredWrapper(gemini_model)
    
    else:
        raise ValueError(f"Unsupported LLM client: {client}")
