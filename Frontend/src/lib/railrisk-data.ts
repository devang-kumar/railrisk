import { getSampleShipments, predictRisk, type Shipment, type RiskReport } from "./api-client";

export type RiskLevel = "Low" | "Medium" | "High" | "Critical";
export type HumanStatus = "Pending" | "Awaiting Dispatcher Approval" | "Recommended for Human Review";
export type ActionStatus = "Pending" | "Dispatched" | "Resolved" | "Escalated";
export type CargoCategory = "Medical" | "Fuel" | "Food" | "Industrial" | "General";

export interface Wagon {
  id: string;
  trainId: string;
  route: string;
  cargo: string;
  cargoCategory: CargoCategory;
  delayHours: number;
  destination: string;
  receiver: string;
  risk: RiskLevel;
  criticalityScore: number;
  actionStatus: ActionStatus;
  recommendedAction: string;
  reason: string;
  riskReasoning: string;
  recommendationReason: string;
  humanStatus: HumanStatus;
  impact: string;
  backupHours: number;
  escalationStage: number;
}

const cargoCategoryMap: Record<string, CargoCategory> = {
  "Liquid Oxygen": "Medical",
  "Vaccines and Medicine": "Medical",
  "Ventilator Components": "Medical",
  "Insulin & Vaccine Cold Chain": "Medical",
  "Medical Oxygen Cylinders": "Medical",
  "Jet Fuel": "Fuel",
  "Diesel Fuel": "Fuel",
  "Coal": "Fuel",
  "Perishable Food (Produce)": "Food",
  "Grain and Wheat": "Food",
  "Industrial Chemicals": "Industrial",
  "Raw Steel": "Industrial",
  "Consumer Electronics": "General",
  "Apparel and Clothing": "General",
  "Steel Coils": "Industrial",
  "Textiles": "General",
};

const actionStatusMap: Record<string, ActionStatus> = {
  "Awaiting Dispatcher Approval": "Escalated",
  "Recommended for Human Review": "Pending",
  "Pending": "Pending",
};

function mapRiskReportToWagon(report: RiskReport, index: number): Wagon {
  return {
    id: report.shipment_id,
    trainId: `TR-${1000 + index}`,
    route: "Mumbai → Pune",
    cargo: report.cargo_type,
    cargoCategory: cargoCategoryMap[report.cargo_type] || "General",
    delayHours: report.delay_hours,
    destination: report.destination,
    receiver: report.destination,
    risk: mapRiskScoreToLevel(report.risk_score),
    criticalityScore: report.criticality_score,
    actionStatus: actionStatusMap[report.human_status] || "Pending",
    recommendedAction: report.recommended_action,
    reason: report.recommendation_reason || report.risk_reasoning,
    riskReasoning: report.risk_reasoning,
    recommendationReason: report.recommendation_reason,
    humanStatus: report.human_status as HumanStatus,
    impact: report.predicted_impact,
    backupHours: getBackupHours(report.cargo_type, report.delay_hours),
    escalationStage: getEscalationStage(report.risk_score),
  };
}

function mapRiskScoreToLevel(score: number): RiskLevel {
  if (score >= 80) return "Critical";
  if (score >= 50) return "High";
  if (score >= 30) return "Medium";
  return "Low";
}

function getBackupHours(cargoType: string, delayHours: number): number {
  const backupMap: Record<string, number> = {
    "Liquid Oxygen": 3,
    "Vaccines and Medicine": 5,
    "Medical Oxygen Cylinders": 3,
    "Insulin & Vaccine Cold Chain": 5,
    "Ventilator Components": 6,
    "Jet Fuel": 8,
    "Diesel Fuel": 8,
    "Coal": 48,
    "Perishable Food (Produce)": 12,
    "Grain and Wheat": 24,
    "Industrial Chemicals": 12,
    "Raw Steel": 36,
    "Consumer Electronics": 48,
    "Apparel and Clothing": 48,
    "Steel Coils": 36,
    "Textiles": 48,
  };
  const base = backupMap[cargoType] || 24;
  return Math.max(1, base - Math.floor(delayHours / 2));
}

function getEscalationStage(riskScore: number): number {
  if (riskScore >= 80) return 4;
  if (riskScore >= 50) return 3;
  if (riskScore >= 30) return 2;
  return 1;
}

let cachedWagons: Wagon[] | null = null;

export async function fetchWagons(): Promise<Wagon[]> {
  if (cachedWagons) return cachedWagons;
  try {
    const shipments = await getSampleShipments();
    const reports = await Promise.all(shipments.map((s, i) => predictRisk(s)));
    cachedWagons = reports.map((r, i) => mapRiskReportToWagon(r, i));
    return cachedWagons;
  } catch (error) {
    console.error("Failed to fetch from API, using fallback data:", error);
    return getFallbackWagons();
  }
}

function getFallbackWagons(): Wagon[] {
  return [
    {
      id: "W-08", trainId: "TR-2241", route: "Mumbai → Pune", cargo: "Medical Oxygen Cylinders",
      cargoCategory: "Medical", delayHours: 6, destination: "Pune Central", receiver: "City Hospital",
      risk: "Critical", criticalityScore: 94, actionStatus: "Escalated", recommendedAction: "Priority alert + immediate road transfer",
      reason: "Hospital backup oxygen lasts ~3 hours. Delay exceeds backup window — patient risk imminent.",
      riskReasoning: "This shipment has a very high risk score due to High criticality and Minor delay severity.",
      recommendationReason: "Cargo-specific action recommended for Medical Oxygen Cylinders (risk score: 94).",
      humanStatus: "Awaiting Dispatcher Approval", impact: "Emergency oxygen supply to 240-bed hospital may fail within 90 minutes.",
      backupHours: 3, escalationStage: 4,
    },
    {
      id: "W-12", trainId: "TR-1108", route: "Vadodara → Delhi", cargo: "Insulin & Vaccine Cold Chain",
      cargoCategory: "Medical", delayHours: 4, destination: "Delhi NCR", receiver: "AIIMS Logistics",
      risk: "High", criticalityScore: 81, actionStatus: "Dispatched", recommendedAction: "Reroute via refrigerated truck",
      reason: "Cold-chain payload — temperature integrity drops after 5 hours of stoppage.",
      riskReasoning: "Risk score is elevated due to High cargo and Minor delay severity.",
      recommendationReason: "Cargo-specific action recommended for Insulin & Vaccine Cold Chain (risk score: 81).",
      humanStatus: "Recommended for Human Review", impact: "Vaccine batch worth ₹1.2Cr at risk of spoilage.",
      backupHours: 5, escalationStage: 3,
    },
    {
      id: "W-03", trainId: "TR-9920", route: "Visakhapatnam → Hyderabad", cargo: "Diesel Fuel",
      cargoCategory: "Fuel", delayHours: 5, destination: "Hyderabad Depot", receiver: "State Power Grid",
      risk: "High", criticalityScore: 76, actionStatus: "Pending", recommendedAction: "Notify backup depot, prepare tanker convoy",
      reason: "Power grid reserves cover 8 hours; further delay triggers brownout risk.",
      riskReasoning: "Risk score is elevated due to High cargo and Minor delay severity.",
      recommendationReason: "Cargo-specific action recommended for Diesel Fuel (risk score: 76).",
      humanStatus: "Recommended for Human Review", impact: "Possible 2-hour power disruption to industrial sector.",
      backupHours: 8, escalationStage: 2,
    },
    {
      id: "W-21", trainId: "TR-3045", route: "Ludhiana → Jaipur", cargo: "Perishable Produce",
      cargoCategory: "Food", delayHours: 3, destination: "Jaipur Wholesale", receiver: "Regional Distributor",
      risk: "Medium", criticalityScore: 52, actionStatus: "Pending", recommendedAction: "Monitor — alert vendor of revised ETA",
      reason: "Produce shelf-life acceptable up to 12 hours additional.",
      riskReasoning: "Moderate risk level due to Medium cargo and Minor delay.",
      recommendationReason: "Cargo-specific action recommended for Perishable Produce (risk score: 52).",
      humanStatus: "Recommended for Human Review", impact: "Minor market disruption; alternative supply available.",
      backupHours: 12, escalationStage: 2,
    },
    {
      id: "W-17", trainId: "TR-7712", route: "Chennai → Bengaluru", cargo: "Steel Coils",
      cargoCategory: "Industrial", delayHours: 2, destination: "Bengaluru Yard", receiver: "Automotive Plant",
      risk: "Low", criticalityScore: 24, actionStatus: "Pending", recommendedAction: "Standard monitoring",
      reason: "Buffer inventory at plant exceeds 36 hours.",
      riskReasoning: "Low risk - Low cargo and None delay severity.",
      recommendationReason: "Generic action recommended (risk score: 24).",
      humanStatus: "Pending", impact: "No operational impact expected.",
      backupHours: 36, escalationStage: 1,
    },
    {
      id: "W-29", trainId: "TR-5563", route: "Kolkata → Patna", cargo: "Ventilator Components",
      cargoCategory: "Medical", delayHours: 5, destination: "Patna Med Hub", receiver: "District Hospital Network",
      risk: "High", criticalityScore: 78, actionStatus: "Dispatched", recommendedAction: "Air freight critical SKUs",
      reason: "Scheduled ICU installation tomorrow at 3 facilities.",
      riskReasoning: "Risk score is elevated due to High cargo and Minor delay severity.",
      recommendationReason: "Cargo-specific action recommended for Ventilator Components (risk score: 78).",
      humanStatus: "Recommended for Human Review", impact: "ICU capacity expansion delayed for 60 patients.",
      backupHours: 6, escalationStage: 3,
    },
    {
      id: "W-34", trainId: "TR-4480", route: "Surat → Ahmedabad", cargo: "Textiles",
      cargoCategory: "General", delayHours: 1, destination: "Ahmedabad", receiver: "Export Warehouse",
      risk: "Low", criticalityScore: 12, actionStatus: "Pending", recommendedAction: "No action required",
      reason: "Within tolerance.",
      riskReasoning: "Low risk - Low cargo and None delay severity.",
      recommendationReason: "Generic action recommended (risk score: 12).",
      humanStatus: "Pending", impact: "None.",
      backupHours: 48, escalationStage: 1,
    },
  ];
}

// Synchronous getter for compatibility
export const wagons: Wagon[] = getFallbackWagons();

export function getWagon(id: string) {
  return wagons.find((w) => w.id.toLowerCase() === id.toLowerCase());
}

export const riskColor: Record<RiskLevel, string> = {
  Low: "text-emerald-400",
  Medium: "text-yellow-400",
  High: "text-[#ff6b00]",
  Critical: "text-[#ff1e1e]",
};

export const riskDot: Record<RiskLevel, string> = {
  Low: "bg-emerald-400",
  Medium: "bg-yellow-400",
  High: "bg-[#ff6b00]",
  Critical: "bg-[#ff1e1e]",
};
