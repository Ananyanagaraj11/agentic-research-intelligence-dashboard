import argparse
import json
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def iter_entries(xml_text):
    root = ET.fromstring(xml_text)
    for entry in root.findall("atom:entry", ATOM_NS):
        yield entry


def extract_text(entry):
    title_node = entry.find("atom:title", ATOM_NS)
    summary_node = entry.find("atom:summary", ATOM_NS)
    title = (title_node.text or "").strip()
    summary = (summary_node.text or "").strip()
    return title, summary


def extract_label(entry):
    categories = entry.findall("atom:category", ATOM_NS)
    if not categories:
        return "unknown"
    term = categories[0].attrib.get("term", "unknown")
    return term


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-label-count", type=int, default=2)
    args = parser.parse_args()

    raw_dir = Path("data/raw")
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)

    xml_files = sorted(raw_dir.glob("arxiv_*.xml"))
    if not xml_files:
        raise FileNotFoundError("No XML files found in data/raw. Run ingest first.")

    records = []
    label_counts = Counter()

    for xml_file in xml_files:
        xml_text = xml_file.read_text(encoding="utf-8")
        for entry in iter_entries(xml_text):
            title, summary = extract_text(entry)
            label = extract_label(entry)
            if not title or not summary or label == "unknown":
                continue
            text = f"{title}\n{summary}"
            records.append({"text": text, "label": label})
            label_counts[label] += 1

    kept_labels = {
        label for label, count in label_counts.items() if count >= args.min_label_count
    }

    out_path = out_dir / "papers.jsonl"
    kept_counts = Counter()
    with out_path.open("w", encoding="utf-8") as out_file:
        for record in records:
            if record["label"] not in kept_labels:
                continue
            out_file.write(json.dumps(record) + "\n")
            kept_counts[record["label"]] += 1

    stats_path = out_dir / "label_stats.json"
    stats_path.write_text(json.dumps(kept_counts, indent=2), encoding="utf-8")

    dropped = sum(label_counts.values()) - sum(kept_counts.values())
    print(f"Saved {sum(kept_counts.values())} records; dropped {dropped}.")


if __name__ == "__main__":
    main()
