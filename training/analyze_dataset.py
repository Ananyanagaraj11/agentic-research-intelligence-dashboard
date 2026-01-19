import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_+-]{2,}")


def load_samples():
    data_path = Path("data/processed/papers.jsonl")
    if not data_path.exists():
        raise FileNotFoundError(
            "Missing data/processed/papers.jsonl. Run preprocessing first."
        )
    samples = []
    with data_path.open("r", encoding="utf-8") as f:
        for line in f:
            samples.append(json.loads(line))
    return samples


def tokenize(text):
    tokens = TOKEN_RE.findall(text.lower())
    return [t for t in tokens if t not in ENGLISH_STOP_WORDS]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top-terms", type=int, default=12)
    parser.add_argument("--max-per-label", type=int, default=2000)
    args = parser.parse_args()

    samples = load_samples()
    label_counts = Counter()
    global_counts = Counter()
    label_term_counts = defaultdict(Counter)

    per_label_seen = Counter()
    for sample in samples:
        label = sample["label"]
        label_counts[label] += 1
        if per_label_seen[label] >= args.max_per_label:
            continue
        per_label_seen[label] += 1
        tokens = tokenize(sample["text"])
        global_counts.update(tokens)
        label_term_counts[label].update(tokens)

    top_global = [t for t, _ in global_counts.most_common(args.top_terms)]
    top_by_label = {
        label: [t for t, _ in counts.most_common(args.top_terms)]
        for label, counts in label_term_counts.items()
    }

    insights = {
        "total_records": sum(label_counts.values()),
        "unique_labels": len(label_counts),
        "top_labels": label_counts.most_common(10),
        "top_terms_global": top_global,
        "top_terms_by_label": top_by_label,
    }

    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/data_insights.json").write_text(
        json.dumps(insights, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
