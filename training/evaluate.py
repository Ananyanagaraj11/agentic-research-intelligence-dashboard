import json
from pathlib import Path


def main():
    report_path = Path("artifacts/report.json")
    if not report_path.exists():
        raise FileNotFoundError("Missing artifacts/report.json. Train first.")

    report = json.loads(report_path.read_text(encoding="utf-8"))
    summary = {
        "macro_f1": report["macro avg"]["f1-score"],
        "weighted_f1": report["weighted avg"]["f1-score"],
        "accuracy": report["accuracy"],
    }
    Path("artifacts/summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
