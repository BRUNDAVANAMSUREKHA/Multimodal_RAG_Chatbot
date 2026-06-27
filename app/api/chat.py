from fastapi import APIRouter, Form
from app.services.retriever import retrieve_documents
from app.services.gemini_service import ask_gemini

router = APIRouter()


@router.post("/chat")
async def chat(
        query: str = Form(...),
        api_key: str = Form(...),
        doc_id: str = Form(...)
):
    try:
        print(f"[chat] USER QUERY: {query} | DOC: {doc_id}")

        docs = retrieve_documents(query, api_key, doc_id)

        print(f"[chat] RETRIEVED DOCS: {len(docs)}")

        if not docs:
            answer = ask_gemini(
                context="[No relevant chunks were retrieved from the document for this query.]",
                question=query,
                api_key=api_key
            )
            return {"answer": answer}

        context = "\n\n".join(docs)
        answer = ask_gemini(context, query, api_key)
        return {"answer": answer}

    except Exception as e:
        print(f"[chat] ERROR: {e}")
        return {"answer": f"Error: {str(e)}"}