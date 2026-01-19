import json
from pathlib import Path

from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report


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


def main():
    samples = load_samples()
    texts = [s["text"] for s in samples]
    labels = [s["label"] for s in samples]

    if not texts:
        raise ValueError("No samples found. Check preprocessing output.")

    label_counts = Counter(labels)
    min_count = min(label_counts.values())
    stratify_labels = labels if min_count >= 2 else None

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=stratify_labels
    )

    model = Pipeline(
        [
            ("tfidf", TfidfVectorizer(max_features=50000, ngram_range=(1, 2))),
            ("clf", LogisticRegression(max_iter=200)),
        ]
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    report = classification_report(y_test, preds, output_dict=True)

    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
