import json
import os

class BaseAgent:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'rules.json')
        with open(config_path, 'r') as f:
            self.rules = json.load(f)

class DelayDetectionAgent(BaseAgent):
    """Detects delays and calculates delay severity dynamically."""
    def process(self, shipment: dict) -> dict:
        delay = shipment.get("delay_time_hours", 0)
        is_delayed = delay > 0
        severity = "None"
        
        # Sort thresholds descending
        thresholds = sorted(self.rules["delay_thresholds"].items(), key=lambda x: x[1], reverse=True)
        for level, thresh in thresholds:
            if delay >= thresh and delay > 0:
                severity = level
                break
                
        return {
            "is_delayed": is_delayed,
            "delay_severity": severity,
            "delay_time_hours": delay
        }

class CargoCriticalityAgent(BaseAgent):
    """Evaluates the criticality of the cargo based on dynamic urgency and dependency weights."""
    def process(self, shipment: dict) -> dict:
        urgency = shipment.get("urgency_level", "Low")
        dependency = shipment.get("dependency_type", "Unknown")
        
        score = 0
        
        # Urgency scoring
        score += self.rules["criticality_weights"]["urgency"].get(urgency, 5)
            
        # Dependency scoring
        score += self.rules["criticality_weights"]["dependency"].get(dependency, self.rules["criticality_weights"]["default_dependency"])
            
        criticality = "Low"
        thresholds = sorted(self.rules["criticality_thresholds"].items(), key=lambda x: x[1], reverse=True)
        for level, thresh in thresholds:
            if score >= thresh:
                criticality = level
                break
                
        return {
            "criticality_score": score,
            "criticality_level": criticality
        }

class ImpactPredictionAgent(BaseAgent):
    """Predicts downstream impact and generates an overall risk score dynamically."""
    def process(self, shipment: dict, delay_info: dict, criticality_info: dict) -> dict:
        delay_hrs = delay_info.get("delay_time_hours", 0)
        crit_score = criticality_info.get("criticality_score", 0)
        
        delay_multiplier = self.rules["risk_calculation"]["delay_multiplier"]
        max_score = self.rules["risk_calculation"]["max_score"]
        
        risk_score = min(max_score, crit_score + (delay_hrs * delay_multiplier))
        
        return {
            "risk_score": round(risk_score, 1),
            "predicted_impact": shipment.get("downstream_impact", "Unknown impact")
        }

class ActionRecommendationAgent(BaseAgent):
    """Recommends action based on dynamic risk thresholds."""
    def process(self, shipment: dict, risk_info: dict) -> dict:
        risk_score = risk_info.get("risk_score", 0)
        
        action = "LOG: Standard delay logging. No immediate action required."
        
        recommendations = sorted(self.rules["action_recommendations"], key=lambda x: x["min_risk_score"], reverse=True)
        for rec in recommendations:
            if risk_score >= rec["min_risk_score"]:
                action = rec["action"]
                break
            
        return {
            "recommended_action": action
        }
