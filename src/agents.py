import json
import os
from groq import Groq
from dotenv import load_dotenv

from prompts import (
    DELAY_AGENT_PROMPT,
    CRITICALITY_AGENT_PROMPT,
    ENVIRONMENTAL_AGENT_PROMPT,
    IMPACT_AGENT_PROMPT,
    ACTION_AGENT_PROMPT
)

load_dotenv()

class BaseAgent:
    def __init__(self):
        self.client = Groq() # Requires GROQ_API_KEY in environment
        self.model = "llama-3.1-8b-instant"

    def _call_llm(self, system_prompt: str) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return {}

class DelayDetectionAgent(BaseAgent):
    """Detects delays and calculates delay severity dynamically using Groq LLM."""
    def process(self, shipment: dict) -> dict:
        prompt = DELAY_AGENT_PROMPT.format(shipment_details=json.dumps(shipment))
        result = self._call_llm(prompt)
        return {
            "is_delayed": result.get("is_delayed", shipment.get("delay_time_hours", 0) > 0),
            "delay_severity": result.get("delay_severity", "Unknown"),
            "delay_time_hours": result.get("delay_time_hours", shipment.get("delay_time_hours", 0))
        }

class CargoCriticalityAgent(BaseAgent):
    """Evaluates the criticality of the cargo using Groq LLM."""
    def process(self, shipment: dict) -> dict:
        prompt = CRITICALITY_AGENT_PROMPT.format(shipment_details=json.dumps(shipment))
        result = self._call_llm(prompt)
        return {
            "criticality_score": result.get("criticality_score", 0),
            "criticality_level": result.get("criticality_level", "Unknown")
        }

class EnvironmentalContextAgent(BaseAgent):
    """Evaluates the weather impact on the specific cargo using Groq LLM."""
    def process(self, shipment: dict) -> dict:
        prompt = ENVIRONMENTAL_AGENT_PROMPT.format(shipment_details=json.dumps(shipment))
        result = self._call_llm(prompt)
        return {
            "environmental_risk_multiplier": result.get("environmental_risk_multiplier", 1.0),
            "weather_impact_reasoning": result.get("weather_impact_reasoning", "No weather impact.")
        }

class ImpactPredictionAgent(BaseAgent):
    """Predicts downstream impact and risk score using Groq LLM."""
    def process(self, shipment: dict, delay_info: dict, criticality_info: dict, env_info: dict, ml_prob: float) -> dict:
        prompt = IMPACT_AGENT_PROMPT.format(
            shipment_details=json.dumps(shipment),
            delay_info=json.dumps(delay_info),
            criticality_info=json.dumps(criticality_info),
            environmental_info=json.dumps(env_info),
            ml_breakdown_prob=ml_prob
        )
        result = self._call_llm(prompt)
        return {
            "risk_score": result.get("risk_score", 0),
            "predicted_impact": result.get("predicted_impact", "Unknown impact"),
            "risk_reasoning": result.get("risk_reasoning", ""),
            "human_status": result.get("human_status", "Pending")
        }

class ActionRecommendationAgent(BaseAgent):
    """Recommends action using Groq LLM."""
    def process(self, shipment: dict, risk_info: dict, ml_prob: float) -> dict:
        prompt = ACTION_AGENT_PROMPT.format(
            shipment_details=json.dumps(shipment),
            risk_info=json.dumps(risk_info),
            ml_breakdown_prob=ml_prob
        )
        result = self._call_llm(prompt)
        return {
            "recommended_action": result.get("recommended_action", "LOG: No action recommended."),
            "recommendation_reason": result.get("recommendation_reason", "")
        }
