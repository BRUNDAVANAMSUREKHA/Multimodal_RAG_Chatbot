import time
from google import genai
from google.genai import types
from app.core.milvus_db import search_data


def retrieve_documents(query, api_key, doc_id):
    client = genai.Client(api_key=api_key)

    for attempt in range(3):
        try:
            response = client.models.embed_content(
                model="gemini-embedding-001",
                contents=types.Content(
                    parts=[types.Part(text=query)]
                )
            )
            query_vector = response.embeddings[0].values
            docs = search_data(query_vector, doc_id=doc_id)
            return docs

        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                print(f"[retriever] Rate limit, waiting 65s (attempt {attempt + 1})...")
                time.sleep(65)
                continue
            raise e

    return []
