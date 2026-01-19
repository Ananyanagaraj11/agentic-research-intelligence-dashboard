import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
import torch
from datasets import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)


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


class WeightedTrainer(Trainer):
    def __init__(self, *args, class_weights=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.get("labels")
        outputs = model(**inputs)
        logits = outputs.get("logits")
        loss_fct = torch.nn.CrossEntropyLoss(weight=self.class_weights)
        loss = loss_fct(logits, labels)
        return (loss, outputs) if return_outputs else loss


def build_label_maps(labels):
    unique = sorted(set(labels))
    label_to_id = {label: i for i, label in enumerate(unique)}
    id_to_label = {i: label for label, i in label_to_id.items()}
    return label_to_id, id_to_label


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="allenai/scibert_scivocab_uncased")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=256)
    args = parser.parse_args()

    samples = load_samples()
    texts = [s["text"] for s in samples]
    labels = [s["label"] for s in samples]
    label_to_id, id_to_label = build_label_maps(labels)
    numeric_labels = [label_to_id[l] for l in labels]

    if not texts:
        raise ValueError("No samples found. Check preprocessing output.")

    min_count = min(Counter(numeric_labels).values())
    stratify_labels = numeric_labels if min_count >= 2 else None
    train_idx, test_idx = train_test_split(
        list(range(len(texts))),
        test_size=0.2,
        random_state=42,
        stratify=stratify_labels,
    )
    dataset = {
        "train": Dataset.from_dict(
            {
                "text": [texts[i] for i in train_idx],
                "label": [numeric_labels[i] for i in train_idx],
            }
        ),
        "test": Dataset.from_dict(
            {
                "text": [texts[i] for i in test_idx],
                "label": [numeric_labels[i] for i in test_idx],
            }
        ),
    }

    tokenizer = AutoTokenizer.from_pretrained(args.model)

    def tokenize(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=args.max_length,
        )

    tokenized = {
        split: dataset[split].map(tokenize, batched=True, remove_columns=["text"])
        for split in dataset
    }
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    counts = Counter(numeric_labels)
    max_count = max(counts.values())
    weights = [max_count / counts[i] for i in range(len(counts))]
    class_weights = torch.tensor(weights, dtype=torch.float)

    model = AutoModelForSequenceClassification.from_pretrained(
        args.model, num_labels=len(label_to_id), id2label=id_to_label, label2id=label_to_id
    )

    args_out = TrainingArguments(
        output_dir="artifacts/hf_model",
        learning_rate=2e-5,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=25,
        load_best_model_at_end=True,
        report_to=[],
    )

    trainer = WeightedTrainer(
        model=model,
        args=args_out,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
        tokenizer=tokenizer,
        data_collator=data_collator,
        class_weights=class_weights.to(model.device),
    )

    trainer.train()
    preds = trainer.predict(tokenized["test"])
    pred_labels = np.argmax(preds.predictions, axis=1)
    test_label_ids = sorted(set(tokenized["test"]["label"]))
    report = classification_report(
        tokenized["test"]["label"],
        pred_labels,
        labels=test_label_ids,
        target_names=[id_to_label[i] for i in test_label_ids],
        output_dict=True,
        zero_division=0,
    )

    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/hf_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    summary = {
        "macro_f1": report["macro avg"]["f1-score"],
        "weighted_f1": report["weighted avg"]["f1-score"],
        "accuracy": report["accuracy"],
    }
    Path("artifacts/hf_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
