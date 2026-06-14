import json
from agents import (
    DelayDetectionAgent,
    CargoCriticalityAgent,
    EnvironmentalContextAgent,
    ImpactPredictionAgent,
    ActionRecommendationAgent
)
from ml_model import ml_predictor


class RailRiskReport:
    def __init__(self, shipment: dict, ml_prob: float, delay_info: dict,
                 criticality_info: dict, env_info: dict, risk_info: dict,
                 action_info: dict):
        self.shipment_id = shipment.get("id", "N/A")
        self.cargo_type = shipment.get("cargo_type", "N/A")
        self.destination = shipment.get("destination", "N/A")
        self.weather = shipment.get("route_weather", "Unknown")
        self.ml_breakdown_prob = ml_prob
        
        self.delay_hours = delay_info.get("delay_time_hours", 0)
        self.delay_severity = delay_info.get("delay_severity", "None")
        
        self.criticality_level = criticality_info.get("criticality_level", "Low")
        self.criticality_score = criticality_info.get("criticality_score", 0)
        
        self.env_multiplier = env_info.get("environmental_risk_multiplier", 1.0)
        self.env_reasoning = env_info.get("weather_impact_reasoning", "")
        
        self.risk_score = risk_info.get("risk_score", 0)
        self.predicted_impact = risk_info.get("predicted_impact", "Unknown")
        self.risk_reasoning = risk_info.get("risk_reasoning", "")
        self.human_status = risk_info.get("human_status", "Pending")
        
        self.recommended_action = action_info.get("recommended_action", "No action")
        self.recommendation_reason = action_info.get("recommendation_reason", "")

    def format_report(self) -> str:
        sep = "-" * 70
        return (
            f"{sep}\n"
            f"  RAILRISK HYBRID AI/ML REPORT - {self.shipment_id}\n"
            f"{sep}\n"
            f"  [1] SHIPMENT DETAILS\n"
            f"      Cargo       : {self.cargo_type}\n"
            f"      Destination : {self.destination}\n"
            f"      Delay       : {self.delay_hours} h ({self.delay_severity} severity)\n"
            f"      Weather     : {self.weather}\n"
            f"\n"
            f"  [2] ML PREDICTIVE MAINTENANCE\n"
            f"      Breakdown Probability: {self.ml_breakdown_prob}% (Random Forest)\n"
            f"\n"
            f"  [3] LLM INTELLIGENCE\n"
            f"      Criticality : {self.criticality_level} (Score: {self.criticality_score})\n"
            f"      Env. Impact : Multiplier {self.env_multiplier}x - {self.env_reasoning}\n"
            f"      Risk Score  : {self.risk_score} / 100\n"
            f"      Impact      : {self.predicted_impact}\n"
            f"      Reasoning   : {self.risk_reasoning}\n"
            f"      Status      : {self.human_status}\n"
            f"\n"
            f"  [4] AI ACTION RECOMMENDATION\n"
            f"      Action      : {self.recommended_action}\n"
            f"      Reason      : {self.recommendation_reason}\n"
            f"{sep}\n"
        )


class RailRiskPipeline:
    def __init__(self):
        self.delay_agent = DelayDetectionAgent()
        self.criticality_agent = CargoCriticalityAgent()
        self.env_agent = EnvironmentalContextAgent()
        self.impact_agent = ImpactPredictionAgent()
        self.action_agent = ActionRecommendationAgent()

    def run(self, shipment: dict) -> RailRiskReport:
        # Layer 1: ML Breakdown Prediction
        ml_prob = ml_predictor.predict_failure_probability(
            shipment.get("wagon_age_years", 10),
            shipment.get("load_weight_tons", 50),
            shipment.get("days_since_service", 100)
        )
        
        # Layer 2-6: LLM Agents
        delay_info = self.delay_agent.process(shipment)
        criticality_info = self.criticality_agent.process(shipment)
        env_info = self.env_agent.process(shipment)
        
        risk_info = self.impact_agent.process(shipment, delay_info, criticality_info, env_info, ml_prob)
        action_info = self.action_agent.process(shipment, risk_info, ml_prob)
        
        return RailRiskReport(shipment, ml_prob, delay_info, criticality_info, env_info, risk_info, action_info)

    def run_batch(self, shipments: list[dict]) -> list[RailRiskReport]:
        return [self.run(s) for s in shipments]
