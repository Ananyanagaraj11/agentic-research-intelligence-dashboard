# Agentic Research Intelligence Dashboard

End-to-end project from dataset ingestion to model training, evaluation, and an interactive dashboard.

## Live demo
- https://frontend-two-gilt-97.vercel.app
- The demo uses fallback metrics unless the API is deployed.

## What this project includes
- Large-scale dataset ingestion from arXiv
- Training pipeline for multi-class paper classification
- Evaluation and error analysis
- FastAPI backend with agentic insights
- Interactive, animated dashboard (React + Vite)

## Repo structure
```
backend/        FastAPI API + agentic services
training/       Data prep, training, evaluation
frontend/       Dashboard UI
data/           Raw and processed datasets (local)
```

## Quick start (local)
1. Create a Python venv and install requirements:
   - `python -m venv .venv`
   - `.\.venv\Scripts\activate`
   - `pip install -r backend/requirements.txt`
   - `pip install -r training/requirements.txt`
2. Run the API:
   - `uvicorn backend.app.main:app --reload`
3. Run the UI:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

## Next milestones
- Add arXiv dataset ingestion (`training/ingest_arxiv.py`)
- Preprocess XML into JSONL (`training/preprocess_arxiv.py`)
- Analyze dataset semantics (`training/analyze_dataset.py`)
- Train classifier (`training/train_classifier.py`)
- Train transformer classifier (`training/train_transformer.py`)
- Evaluate (`training/evaluate.py`)
- Connect UI to live API endpoints
