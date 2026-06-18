from pymilvus import (
    connections, FieldSchema, CollectionSchema,
    DataType, Collection, utility
)

MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
collection_name = "document_rag"
EMBEDDING_DIM = 3072

_collection = None


def _get_connection():
    try:
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
    except Exception:
        pass


def _create_collection():
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="doc_id", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM)
    ]
    schema = CollectionSchema(fields, description="RAG Collection")
    col = Collection(name=collection_name, schema=schema)
    col.create_index(
        field_name="embedding",
        index_params={
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128}
        }
    )
    print("[milvus] Collection created")
    return col


def _get_collection():
    global _collection
    _get_connection()
    if _collection is None:
        if not utility.has_collection(collection_name):
            _collection = _create_collection()
        else:
            _collection = Collection(collection_name)
        _collection.load()
    return _collection


def insert_data(doc_id, texts, embeddings):
    col = _get_collection()
    doc_ids = [doc_id] * len(texts)
    col.insert([doc_ids, texts, embeddings])
    col.flush()
    print(f"[milvus] Inserted {len(texts)} chunks for doc: {doc_id}")


def search_data(query_embedding, doc_id, top_k=8):
    col = _get_collection()
    search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
    try:
        safe_doc_id = doc_id.replace("\\", "\\\\").replace('"', '\\"')
        expr = f'doc_id == "{safe_doc_id}"'
        print(f"[milvus] search expr: {expr}")

        results = col.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            expr=expr,
            output_fields=["text", "doc_id"]
        )
        retrieved = []
        for hit in results[0]:
            text = hit.entity.get("text")
            print(f"[milvus] hit score={hit.distance:.4f} text_len={len(text) if text else 0}")
            if text and text.strip():
                retrieved.append(text)

        print(f"[milvus] search returned {len(retrieved)} chunks for doc_id='{doc_id}'")

        # Fallback: if doc_id filter returns nothing, try without filter
        if len(retrieved) == 0:
            print("[milvus] No results with doc_id filter, trying global search...")
            results_global = col.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=top_k,
                output_fields=["text", "doc_id"]
            )
            for hit in results_global[0]:
                text = hit.entity.get("text")
                if text and text.strip():
                    retrieved.append(text)
            print(f"[milvus] global search returned {len(retrieved)} chunks")

        return retrieved
    except Exception as e:
        print(f"[milvus] search_data error: {e}")
        return []


def delete_doc(doc_id):
    col = _get_collection()
    safe_doc_id = doc_id.replace("\\", "\\\\").replace('"', '\\"')
    col.delete(expr=f'doc_id == "{safe_doc_id}"')
    col.flush()
    print(f"[milvus] Deleted all chunks for doc: {doc_id}")


def list_docs():
    try:
        col = _get_collection()
        results = col.query(
            expr='doc_id != ""',
            output_fields=["doc_id"],
            limit=1000
        )
        doc_ids = list(set(r["doc_id"] for r in results))
        print(f"[milvus] list_docs found: {doc_ids}")
        return doc_ids
    except Exception as e:
        print(f"[milvus] list_docs error: {e}")
        return []