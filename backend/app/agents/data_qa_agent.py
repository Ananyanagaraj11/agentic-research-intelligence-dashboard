def detect_noisy_samples(records):
    # Placeholder heuristics; swap with embedding/LLM checks later.
    noisy = []
    for idx, r in enumerate(records):
        title = r.get("title", "").strip()
        abstract = r.get("abstract", "").strip()
        if len(title) < 8 or len(abstract) < 80:
            noisy.append({"index": idx, "reason": "short_text"})
    return noisy
