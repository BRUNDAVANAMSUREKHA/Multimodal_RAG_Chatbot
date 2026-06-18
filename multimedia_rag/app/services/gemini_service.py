import time
from google import genai


def ask_gemini(context, question, api_key):
    client = genai.Client(api_key=api_key)

    no_context = context.strip().startswith("[No relevant chunks")

    if no_context:
        prompt = f"""You are a helpful assistant. The user uploaded a document but no relevant chunks were found for their query.
Answer from your general knowledge if you can, and briefly mention it wasn't found in their document.

User asks: "{question}"

ANSWER:"""
    else:
        prompt = f"""You are a smart assistant helping a user understand a document they uploaded.

Here is the relevant content retrieved from their document:

---
DOCUMENT CONTEXT:
{context}
---

The user asks: "{question}"

Respond naturally and helpfully:
- Give clear definitions, explanations, or examples as needed.
- Use bullet points only when listing multiple things, otherwise use paragraphs.
- Do not say "Based on the document..." — just answer directly.
- Only say the topic isn't covered if the context is completely unrelated.
ANSWER:"""

    models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash"]

    for model_name in models_to_try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                text = response.text
                if text is None:
                    return "I wasn't able to generate a response. Please try rephrasing."
                return text.strip()

            except Exception as e:
                err = str(e)
                if "503" in err or "UNAVAILABLE" in err:
                    wait = 10 * (attempt + 1)
                    print(f"[gemini] Model {model_name} busy, retrying in {wait}s...")
                    time.sleep(wait)
                    continue
                elif "429" in err or "RESOURCE_EXHAUSTED" in err:
                    return "Rate limit reached. Please wait a minute and try again."
                elif "404" in err or "not found" in err.lower():
                    print(f"[gemini] Model {model_name} not found, trying next...")
                    break
                else:
                    raise e
        else:
            continue
        continue

    return "Model is temporarily unavailable. Please try again in a moment."