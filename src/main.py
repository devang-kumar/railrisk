import json
import os
from agents import (
    DelayDetectionAgent,
    CargoCriticalityAgent,
    ImpactPredictionAgent,
    ActionRecommendationAgent
)

def main():
    # Load the dataset
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'freight_dataset.json')
    with open(data_path, 'r') as f:
        dataset = json.load(f)
        
    # Initialize agents
    delay_agent = DelayDetectionAgent()
    criticality_agent = CargoCriticalityAgent()
    impact_agent = ImpactPredictionAgent()
    action_agent = ActionRecommendationAgent()
    
    print("--- RailRisk AI: Disruption Risk Intelligence System ---\n")
    
    # Process each shipment
    for shipment in dataset:
        print(f"Processing Shipment: {shipment['id']} | Cargo: {shipment['cargo_type']} | Destination: {shipment['destination']}")
        
        # 1. Delay Detection
        delay_info = delay_agent.process(shipment)
        print(f"  [1] Delay Detection   : {delay_info['delay_time_hours']} hours ({delay_info['delay_severity']} severity)")
        
        # 2. Cargo Criticality
        crit_info = criticality_agent.process(shipment)
        print(f"  [2] Cargo Criticality : {crit_info['criticality_level']} (Score: {crit_info['criticality_score']})")
        
        # 3. Impact Prediction
        risk_info = impact_agent.process(shipment, delay_info, crit_info)
        print(f"  [3] Risk & Impact     : Risk Score {risk_info['risk_score']} | Impact: {risk_info['predicted_impact']}")
        
        # 4. Action Recommendation
        action_info = action_agent.process(shipment, risk_info)
        print(f"  [4] Action Recomm.    : {action_info['recommended_action']}")
        print("-" * 80)

if __name__ == "__main__":
    main()
