import argparse
import json
import time
from pathlib import Path

import requests

ARXIV_API = "http://export.arxiv.org/api/query"


def fetch_arxiv(start=0, max_results=200, search_query="cat:cs.AI"):
    params = {
        "search_query": search_query,
        "start": start,
        "max_results": max_results,
    }
    resp = requests.get(ARXIV_API, params=params, timeout=30)
    resp.raise_for_status()
    return resp.text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="cat:cs.AI")
    parser.add_argument("--batches", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=200)
    parser.add_argument("--sleep", type=float, default=2.0)
    args = parser.parse_args()

    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    batch_count = args.batches
    batch_size = args.batch_size

    for i in range(batch_count):
        xml_text = fetch_arxiv(
            start=i * batch_size, max_results=batch_size, search_query=args.query
        )
        out_file = out_dir / f"arxiv_{i}.xml"
        out_file.write_text(xml_text, encoding="utf-8")
        time.sleep(args.sleep)

    manifest = {
        "batches": batch_count,
        "query": args.query,
        "batch_size": batch_size,
    }
    Path("data/raw/manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
