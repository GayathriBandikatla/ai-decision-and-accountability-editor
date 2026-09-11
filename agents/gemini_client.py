"""Shared Gemini call with an ordered model fallback chain."""

import logging
import google.generativeai as genai

from config.settings import settings

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.gemini_api_key)


def model_chain() -> list:
    chain = [settings.gemini_model]
    for name in settings.gemini_fallback_models.split(","):
        name = name.strip()
        if name and name not in chain:
            chain.append(name)
    return chain


def generate_json_text(prompt: str) -> str:
    """Try each model in order; return the first successful response text with ``` fences stripped."""
    last_error = None
    for model_name in model_chain():
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt, generation_config={"temperature": 0})
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.strip()
            logger.info(f"Gemini response from {model_name}")
            return text
        except Exception as e:
            last_error = e
            logger.warning(f"Model {model_name} failed: {str(e).splitlines()[0][:160]}")
    logger.error("All Gemini models in the fallback chain failed")
    raise last_error
