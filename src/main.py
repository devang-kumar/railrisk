import json
import os

from pipeline import RailRiskPipeline


def load_dataset() -> list[dict]:
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'freight_dataset.json')
    with open(path, 'r') as f:
        return json.load(f)


def main():
    dataset = load_dataset()
    pipeline = RailRiskPipeline()

    # Pick diverse cases including the new dynamic out-of-distribution ones
    test_ids = {"FRT-1001", "FRT-1007", "FRT-2001", "FRT-2004"}
    test_cases = [s for s in dataset if s["id"] in test_ids]

    print("====================================================")
    print("  RailRisk AI - Pipeline Test Suite")
    print("====================================================\n")

    reports = pipeline.run_batch(test_cases)
    for report in reports:
        print(report.format_report())

    print("All pipeline tests completed successfully.")


if __name__ == "__main__":
    main()
