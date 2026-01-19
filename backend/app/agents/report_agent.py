def generate_weekly_report(kpis, trends):
    # Minimal agentic stub: turns metrics into a narrative summary.
    return {
        "title": "Weekly Research Intelligence Report",
        "highlights": [
            f"F1 reached {kpis['f1']:.2%} with recall at {kpis['recall']:.2%}.",
            f"Trend momentum peaked at {max(t['value'] for t in trends)}.",
            "Top growth domains: NLP and Bioinformatics.",
        ],
    }
