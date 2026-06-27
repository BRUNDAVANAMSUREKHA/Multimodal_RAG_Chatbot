import time
from google import genai
from google.genai import types


def create_embeddings(chunks, api_key):
    client = genai.Client(api_key=api_key)

    embeddings = []

    # Free tier = 100 requests/min; process 80 per minute to stay safe
    BATCH_SIZE = 80
    WAIT_BETWEEN_BATCHES = 65  # seconds

    for i, chunk in enumerate(chunks):

        # Wait before each batch after the first
        if i > 0 and i % BATCH_SIZE == 0:
            print(f"[embeddings] Batch limit reached at chunk {i}, waiting {WAIT_BETWEEN_BATCHES}s...")
            time.sleep(WAIT_BETWEEN_BATCHES)

        for attempt in range(3):
            try:
                response = client.models.embed_content(
                    model="gemini-embedding-001",
                    contents=types.Content(
                        parts=[types.Part(text=chunk)]
                    )
                )
                embeddings.append(response.embeddings[0].values)
                break

            except Exception as e:
                err = str(e)
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    wait = 60 * (attempt + 1)
                    print(f"[embeddings] Rate limit hit at chunk {i}, waiting {wait}s...")
                    time.sleep(wait)
                    continue
                else:
                    raise e

    print(f"[embeddings] Done: {len(embeddings)} embeddings created")
    return embeddings