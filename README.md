# 🎙️ Agentic Meeting & YouTube Video Assistant

Enterprise-grade agentic pipeline: ingest a YouTube video or audio file →
free open-source Whisper transcription (with automatic Hindi→English
translation) → structured summary/decisions/action-items → an Advanced RAG +
agentic router chat interface, fully observable via LangSmith and evaluated
with `ragas`.

## Architecture

```
YouTube URL / Audio Upload
        │
        ▼
[transcription.py]  yt-dlp download → pydub chunking → faster-whisper
                     (auto language detect; task='translate' if Hindi)
        ▼
[summarizer.py]      Mistral LLM → structured Summary / Decisions / Actions
        ▼
[rag_pipeline.py]    SemanticChunker → HuggingFace embeddings → ChromaDB
        ▼
[agent_graph.py]     LangGraph StateGraph:
                        router (LLM classifier) ─┬─▶ rag_node
                                                  │     (MultiQueryRetriever
                                                  │      → CrossEncoder rerank
                                                  │      → Mistral generate)
                                                  └─▶ general_node
                                                        (direct Mistral, no context)
        ▼
[app.py]             Streamlit chat UI, token streaming, PDF/TXT export

[evaluation.py]      ragas: answer_relevancy, faithfulness, context_precision
LangSmith            traces every LCEL/LangGraph node automatically
```

## Setup

```bash
python -m venv venv && source venv/bin/activate     # or venv\Scripts\activate on Windows
pip install -r requirements.txt
sudo apt-get install -y ffmpeg                       # required by pydub/whisper
cp .env.example .env                                  # then fill in your keys
streamlit run app.py
```

## Required environment variables (`.env`)

```
MISTRAL_API_KEY=your_mistral_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key_here
LANGCHAIN_PROJECT=meeting-assistant

# Optional
COHERE_API_KEY=
USE_COHERE_RERANK=false
WHISPER_MODEL_SIZE=medium
WHISPER_DEVICE=cpu
```

## Running an evaluation

```python
from rag_pipeline import load_vectorstore
from evaluation import evaluate_rag

vs = load_vectorstore("meeting_<your_collection_id>")
questions = ["What did the team decide about the Q3 launch?"]
ground_truths = ["The team decided to delay the launch to October."]

df = evaluate_rag(vs, questions, ground_truths)
print(df)
```

## Notes on scaling this to production

- Swap `Chroma` for a managed vector DB (Pinecone/Weaviate/pgvector) for
  multi-tenant / high-concurrency use — the `rag_pipeline.py` interface is
  designed so this is a localized change.
- `faster-whisper` on CPU with `WHISPER_MODEL_SIZE=medium` is a good
  accuracy/speed tradeoff for free/local use; switch to `large-v3` on GPU
  for higher accuracy, or swap in a hosted transcription API if latency
  matters more than cost.
- The router currently uses `mistral-small-latest` for cheap/fast
  classification — this keeps routing cost near-zero relative to generation.
- Wrap `get_llm()` calls with retry/backoff (e.g. `tenacity`) in front of
  Mistral's free-tier rate limits for production traffic.
