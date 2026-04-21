# Pokemon RAG Assistant

This project is a Retrieval-Augmented Generation (RAG) system built for a Pokemon knowledge dataset. It loads text documents from `RAGDocs`, chunks them, creates embeddings, stores them in a FAISS vector index, retrieves relevant chunks for a user question, and generates an answer using retrieved context.

The project also includes a Streamlit interface, evaluation script, and unit tests.

## Project Structure

```text
.
+-- RAGDocs/                 # Text dataset
+-- rag/                     # RAG pipeline code
|   +-- preprocess.py         # Load, clean, and chunk documents
|   +-- build_faiss_index.py  # Build FAISS index
|   +-- search_faiss.py       # Retrieve top-k chunks
|   +-- generate_answer.py    # Generate context-grounded answers
|   +-- evaluate.py           # Run evaluation questions
|   +-- *_model.py            # Model loading helpers
+-- tests/                   # Unit tests
+-- vector_store/            # Generated FAISS index and chunk metadata
+-- app.py                   # Streamlit app
+-- requirements.txt         # Python dependencies
+-- README.md
```

## 1. Clone The Project

```powershell
git clone <your-github-repo-url>
cd CodyBarkerAssingment4
```

If the folder name is different after cloning, `cd` into that project folder.

## 2. Create A Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The first time you run the embedding or generation step, Hugging Face may download the models:

```text
sentence-transformers/all-MiniLM-L6-v2
Qwen/Qwen2.5-0.5B-Instruct
```

After the first download, the project loads the models locally from cache.

## 4. Check Preprocessing

From the project root:

```powershell
python -m rag.preprocess
```

Or from inside the `rag` folder:

```powershell
python preprocess.py
```

This loads all `.txt` files from `RAGDocs`, cleans the text, splits it into chunks, and prints sample chunks.

## 5. Build The FAISS Index

From the project root:

```powershell
python -m rag.build_faiss_index
```

Or from inside the `rag` folder:

```powershell
python build_faiss_index.py
```

This creates:

```text
vector_store/pokemon_rag.index
vector_store/chunks.json
```

## 6. Test Retrieval

From the project root:

```powershell
python -m rag.search_faiss "What happens when a Pokemon is burned?" --top-k 3
```

Or from inside the `rag` folder:

```powershell
python search_faiss.py "What happens when a Pokemon is burned?" --top-k 3
```

This prints the retrieved chunks, source filenames, chunk numbers, and similarity scores.

## 7. Generate An Answer

From the project root:

```powershell
python -m rag.generate_answer "What happens when a Pokemon is burned?"
```

Or from inside the `rag` folder:

```powershell
python generate_answer.py "What happens when a Pokemon is burned?"
```

This retrieves context from FAISS and generates an answer using only the retrieved context.

## 8. Run Evaluation

From the project root:

```powershell
python -m rag.evaluate
```

Or from inside the `rag` folder:

```powershell
python evaluate.py
```

The evaluation script runs 5 test questions and prints:

```text
Question
Retrieved chunks
Expected answer
Final answer
Accuracy
```

## 9. Run The Streamlit App

From the project root:

```powershell
streamlit run app.py
```

The app lets users:

- Enter a Pokemon question
- View the final generated answer
- View retrieved evidence chunks
- See source files, chunk numbers, and similarity scores
- Adjust retrieval settings in the sidebar

## 10. Run Unit Tests

```powershell
python -m unittest discover -s tests
```

## Notes For Submission

Recommended files/folders to submit or commit:

```text
RAGDocs/
rag/
tests/
app.py
requirements.txt
README.md
.gitignore
```

Optional:

```text
vector_store/
```

The vector store can be regenerated using:

```powershell
python -m rag.build_faiss_index
```

Do not commit:

```text
.venv/
.env
__pycache__/
```
