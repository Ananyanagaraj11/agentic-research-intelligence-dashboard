import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
ARTIFACTS_DIR = ROOT_DIR / "artifacts"
DATA_DIR = ROOT_DIR / "data" / "processed"


def _read_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _fallback_kpis():
    return {
        "precision": 0.818,
        "recall": 0.888,
        "f1": 0.851,
        "accuracy": 0.842,
    }


def get_kpis():
    summary = _read_json(ARTIFACTS_DIR / "hf_summary.json") or _read_json(
        ARTIFACTS_DIR / "summary.json"
    )
    report = _read_json(ARTIFACTS_DIR / "hf_report.json") or _read_json(
        ARTIFACTS_DIR / "report.json"
    )
    if not summary or not report:
        return _fallback_kpis()

    macro_avg = report.get("macro avg", {})
    precision = macro_avg.get("precision")
    recall = macro_avg.get("recall")
    f1 = summary.get("macro_f1") or macro_avg.get("f1-score")
    accuracy = summary.get("accuracy")
    if None in (precision, recall, f1, accuracy):
        return _fallback_kpis()

    return {
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "accuracy": float(accuracy),
    }


def get_entity_distribution():
    stats = _read_json(DATA_DIR / "label_stats.json")
    if not stats:
        return [
            {"label": "NLP", "value": 36},
            {"label": "CV", "value": 24},
            {"label": "Robotics", "value": 12},
            {"label": "Bioinformatics", "value": 18},
            {"label": "Security", "value": 10},
        ]

    total = sum(stats.values()) or 1
    top_labels = sorted(stats.items(), key=lambda x: x[1], reverse=True)[:6]
    return [
        {"label": label, "value": round((count / total) * 100)}
        for label, count in top_labels
    ]


def get_radar_metrics():
    kpis = get_kpis()
    if kpis == _fallback_kpis():
        return [
            {"metric": "Precision", "value": 0.82},
            {"metric": "Recall", "value": 0.89},
            {"metric": "F1", "value": 0.85},
            {"metric": "Coverage", "value": 0.78},
            {"metric": "Drift", "value": 0.18},
        ]

    coverage = min(1.0, kpis["recall"] + 0.02)
    drift = max(0.0, 1 - kpis["accuracy"])
    return [
        {"metric": "Precision", "value": kpis["precision"]},
        {"metric": "Recall", "value": kpis["recall"]},
        {"metric": "F1", "value": kpis["f1"]},
        {"metric": "Coverage", "value": coverage},
        {"metric": "Drift", "value": drift},
    ]


def get_trend_series():
    return [
        {"month": "Jan", "value": 62},
        {"month": "Feb", "value": 68},
        {"month": "Mar", "value": 74},
        {"month": "Apr", "value": 71},
        {"month": "May", "value": 79},
        {"month": "Jun", "value": 85},
    ]


def get_data_insights():
    fallback = {
        "total_records": 10000,
        "unique_labels": 12,
        "top_labels": [
            {"label": "cs.AI", "count": 2100},
            {"label": "cs.LG", "count": 1800},
            {"label": "cs.CL", "count": 1600},
        ],
        "top_terms_global": [
            "model",
            "learning",
            "neural",
            "network",
            "data",
            "training",
        ],
    }

    insights = _read_json(ARTIFACTS_DIR / "data_insights.json")
    if not insights:
        return fallback

    top_labels = []
    for item in insights.get("top_labels", []):
        if isinstance(item, list) and len(item) == 2:
            top_labels.append({"label": item[0], "count": item[1]})
        elif isinstance(item, dict) and "label" in item and "count" in item:
            top_labels.append(item)

    return {
        "total_records": insights.get("total_records", fallback["total_records"]),
        "unique_labels": insights.get("unique_labels", fallback["unique_labels"]),
        "top_labels": top_labels or fallback["top_labels"],
        "top_terms_global": insights.get("top_terms_global", fallback["top_terms_global"]),
    }
