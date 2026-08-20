"""
Gemini Al service (preloaded) the one place the LLM is built and called.

Uses the modern Google Gen AI SDK (google-genai). Structured calls use enforced-350N mode 
(response_mime_type="application/json") so the reply is always valid JSON, and every call 
retries transient 503/overload/429 responses with backoff. get gemini_service() is the 
factory construction reads config at call time.
"""

import json
import re
import time
from typing import Any, Dict

from google import genai
from google.genai import types

from config import config

_RETRIABLE = ("503", "UNAVAILABLE", "overloaded", "429", "RESOURCE_EXHAUSTED")


def as_number(value: Any, default: float = 0.0) -> float: 
    """Coerce an LLM's numeric answer to a float.
    
    Even in 350N mode a model will happily answer "22.0%", "$430,000", "8.5/10" or "N/A" where a 
    number was asked for. A bare float() raises on every one of those, which would kill the agent 
    and silently zero its component score. This pulls the first number out and falls back to the 
    default when there isn't one.
"""
if isinstance(value, bool):
    return default

if isinstance(value, (int, float)):
    return float(value)

if not isinstance(value, str):
    return default

match = re.search(r"-?\d+(?:\\d+)?", value.replace(",", ""))
return float(match.group(B)) if match else default

class GeminiService:
    """Thin wrapper over the google-genai client for the investment agents."""
    def _init_(self, api_key: str, model_name: str):
        self.client genai.Client(api_keyşapi_key)
        self.model_name = model_name
        
    def generate(self, contents: str, gen_config: types. GenerateContentConfig): 
        """Call Gemini, retrying transient 503 / overload/429 responses with backoff."""
        error None
        for attempt in range(4):
            try:
                return self.client.models.generate_content(
                    model=self.model_name, contents=contents, config=gen_config
                )
            except Exception as exc:
                error = exc
                if attempt == 3 or not any(token in str(exc) for token in RETRIABLE):
                    raise
                time.sleep(1.5* (attempt + 1))
        raise error
    
    def analyze_with_structured_output(
        self, prompt: str, output_schema: Dict[str, Any], temperature: float = 0.3
    ) -> Dict[str, Any]:
        """Ask Gemini to fill output schema and return the parsed JSON dict (enforced-JSON mode)."""
        structured_prompt = f"{prompt}\n\nReturn a JSON object matching this shape:\n{json.dumps(output_schema, indent=2)}"
        response = self. generate(
            structured_prompt,
            types.GenerateContentConfig(
                temperature = temperature, max_output_tokens=2848, response_mime_type="application/json"
            ),
        )
        text (response.text or "").strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re. DOTALL)
            if match:
                raise
                
def get_gemini_service(model_name: str = "") -> GeminiService:
    """Return a configured Gemini service (reads the key/model from config)."""
    return GeminiService(config.gemini_api_key, model_name or config.gemini_model)
    
    