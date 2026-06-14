# RailRisk AI: Full-Stack Hybrid AI & ML Disruption Intelligence

Indian Railways moves thousands of trains and massive freight volumes every day. It knows where every wagon is. But delay dashboards do not always translate cargo details and environmental factors into risk priority.

The gap is not in tracking. The gap is in understanding.

**RailRisk AI makes that connection using state-of-the-art Machine Learning and LLM Agents.**

---

## The Invisible Problem

A delayed train shows up in the system as one word — **"delayed."**

No one asks what was inside.
No one asks what the weather is like on the route.
No one asks if the wagon is 15 years old and likely to break down.
No one asks who was waiting.

During emergency situations like COVID oxygen movement, flood relief, and industrial freight disruptions, even a few hours of delay can create serious downstream risk.

The problem was never just the delay.
**The problem was that no system knew what the delay actually meant.**

---

## What RailRisk AI Does

RailRisk AI is a disruption risk intelligence system for rail freight. It does not replace existing railway systems. It adds a powerful **6-layer intelligence pipeline** that is currently missing.

```
[Layer 1] Machine Learning Predictive Maintenance (Random Forest)
      ↓
[Layer 2] LLM Agent: Delay Severity Detection
      ↓
[Layer 3] LLM Agent: Cargo Criticality Analysis
      ↓
[Layer 4] LLM Agent: Environmental & Weather Context
      ↓
[Layer 5] LLM Agent: Downstream Impact Prediction
      ↓
[Layer 6] LLM Agent: Action Recommendation
      ↓
Beautiful React Frontend Report generated
```

A delayed wagon carrying steel on a clear day — low priority. Monitor.

A delayed wagon carrying **Live Cattle** in an **Extreme Heat Wave** in a 15-year old wagon with a 6% breakdown probability — **Critical. Act now.**

RailRisk AI knows the difference.

---

## How It Works — The 6-Layer Architecture

RailRisk AI abandons traditional `if-else` rules. It runs entirely on a dynamic, hybrid AI/ML pipeline.

1. **Predictive Maintenance (Scikit-Learn ML)**: A highly-tuned Random Forest algorithm (optimized for high recall and precision) evaluates telematics data (`wagon_age`, `load_weight`, `days_since_service`) to predict the statistical probability of a mechanical failure.
2. **Delay Detection (Groq LLM)**: Analyzes if the wagon is delayed and the severity of the delay.
3. **Cargo Criticality (Groq LLM)**: Understands the semantic importance of the cargo. (e.g., Live Organs > Steel Coils).
4. **Environmental Context (Groq LLM)**: Cross-references cargo vulnerabilities with live route weather (e.g., Extreme Heat damages perishables, Snowstorms delay electronics). It generates a dynamic risk multiplier.
5. **Impact Prediction (Groq LLM)**: Predicts the holistic socio-economic damage (e.g., "Hospital will run out of ICU oxygen in 2 hours").
6. **Action Recommendation (Groq LLM)**: Formulates an exact, human-readable directive (e.g., "IMMEDIATE ESCALATION: Reroute via cold chain road transport").

One input. Six layers. One clear report.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Machine Learning** | Python, `scikit-learn`, `pandas`, `numpy` |
| **LLM Inference** | `groq` SDK (`llama-3.1-8b-instant`), `pydantic` |
| **Backend API** | Python + FastAPI + Uvicorn |
| **Frontend UI** | React + Tailwind CSS + Vite |
| **Data Engine** | JSON — simulated telemetry and weather data |

---

## Project Structure

```text
railrisk-ai/
├── Frontend/                 # React UI Dashboard
│   ├── src/components/       # UI Components
│   └── src/routes/           # Dashboard and Wagon Detail pages
├── data/
│   └── freight_dataset.json  # Multi-dimensional dataset
├── src/
│   ├── api.py                # FastAPI Backend
│   ├── ml_model.py           # Random Forest Predictive Maintenance
│   ├── agents.py             # Groq LLM Agent definitions
│   ├── pipeline.py           # 6-Layer Orchestrator
│   └── prompts.py            # AI System Instructions
├── .env                      # API Keys (GROQ_API_KEY, etc.)
└── README.md
```

---

## How to Run Locally

### 1. Prerequisites
You will need a `.env` file in the root directory containing your API keys:
```
GROQ_API_KEY=your_key_here
```

### 2. Start the FastAPI AI Backend
```bash
cd railrisk
pip install -r requirements.txt
uvicorn src.api:app --reload
```
The backend API will be available at `http://localhost:8000`.

### 3. Start the React Frontend Dashboard
In a new terminal:
```bash
cd railrisk/Frontend
npm install
npm run dev
```
The beautiful frontend will be available at `http://localhost:5173`.

---

## API Documentation

**POST** `/api/predict`

```json
{
  "id": "W-08",
  "cargo_type": "Liquid Oxygen",
  "destination": "City Hospital",
  "delay_time_hours": 4.5,
  "urgency_level": "High",
  "dependency_type": "Life Support",
  "wagon_age_years": 12,
  "load_weight_tons": 80,
  "days_since_service": 250,
  "route_weather": "Extreme Heat Wave"
}
```

**Response:**
```json
{
  "shipment_id": "W-08",
  "cargo_type": "Liquid Oxygen",
  "weather": "Extreme Heat Wave",
  "ml_breakdown_prob": 6.0,
  "env_multiplier": 1.2,
  "env_reasoning": "Heat can cause liquid oxygen to expand...",
  "criticality_score": 95,
  "risk_score": 87,
  "human_status": "Recommended for Human Review",
  "recommended_action": "IMMEDIATE ESCALATION: Activate Emergency Cold Chain",
  "recommendation_reason": "..."
}
```

---

## What This System Does Not Claim

RailRisk AI does not claim to predict outcomes with certainty. It is a **risk intelligence tool** — it estimates criticality, flags high-risk delays, and recommends priority actions for human review. Final decisions remain with the authority.

---

## Team RootSignal

**Competition:** FAR AWAY 2026 — India's Biggest International Hackathon
**Theme:** Railways · Logistics & Transit · Agentic & Autonomous Systems

| Member | Role |
|---|---|
| Ekta | Strategy, research, problem framing, content, team alignment |
| Devang | Backend, ML, LLM Agents, risk logic, dataset, API, GitHub |
| Aryan | Frontend, UI/UX, PPT, demo visuals |
| Piyush | Pitch, storytelling, judge Q&A, final presentation |
| Mannu | Coordination, progress tracking, testing, submission |

---

*A delayed wagon carrying steel is an inconvenience.*
*A delayed wagon carrying oxygen is a decision.*
*RailRisk AI makes sure that decision is never missed.*
