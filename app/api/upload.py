import sys
import os
import shutil

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from fastapi import APIRouter, UploadFile, File, Form
from app.services.parser import parse_document
from app.services.chunker import create_chunks
from app.services.embeddings import create_embeddings
from app.core.milvus_db import insert_data, list_docs

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_document(
        file: UploadFile = File(...),
        api_key: str = Form(...)
):
    try:
        doc_id = file.filename

        existing_docs = list_docs()
        if doc_id in existing_docs:
            print(f"[upload] {doc_id} already indexed, skipping")
            return {
                "status": "already_exists",
                "message": f"{file.filename} is already indexed.",
                "doc_id": doc_id
            }

        print(f"STEP 1 -> Saving file: {file.filename}")
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("STEP 2 -> Parsing document")
        text = parse_document(file_path)
        print(f"TEXT LENGTH: {len(text)} characters")

        if not text or len(text.strip()) < 10:
            return {
                "status": "error",
                "message": "No text could be extracted. This may be a scanned/image-only PDF."
            }

        print("STEP 3 -> Chunking")
        chunks = create_chunks(text)
        print(f"TOTAL CHUNKS: {len(chunks)}")

        if len(chunks) > 50:
            chunks = chunks[:50]
            print(f"[upload] Capped to 50 chunks")

        print("STEP 4 -> Creating embeddings")
        embeddings = create_embeddings(chunks, api_key)

        print("STEP 5 -> Inserting into Milvus with doc_id")
        insert_data(doc_id, chunks, embeddings)

        print("UPLOAD SUCCESS")
        return {
            "status": "success",
            "message": f"Document uploaded and indexed. ({len(chunks)} chunks)",
            "doc_id": doc_id
        }

    except Exception as e:
        print("UPLOAD ERROR:", str(e))
        return {"status": "error", "message": str(e)}


@router.get("/docs")
async def get_docs():
    try:
        docs = list_docs()
        return {"docs": docs}
    except Exception as e:
        return {"docs": [], "error": str(e)}


@router.delete("/docs/{doc_id}")
async def remove_doc(doc_id: str):
    try:
        from app.core.milvus_db import delete_doc
        delete_doc(doc_id)
        return {"status": "success", "message": f"Deleted {doc_id}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/reset-collection")
async def reset_collection():
    try:
        from pymilvus import utility, connections
        from app.core import milvus_db
        connections.connect(alias="default", host="localhost", port="19530")
        if utility.has_collection("document_rag"):
            utility.drop_collection("document_rag")
            print("[reset] Dropped collection document_rag")
        milvus_db._collection = None
        milvus_db._get_collection()
        return {"status": "success", "message": "Collection reset. Please re-upload your documents."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
