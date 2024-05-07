import dspy
from dspy.retrieve.qdrant_rm import QdrantRM
from qdrant_client import QdrantClient

def setup(docs, ids):
    # Setup Qdrant client in memory
    qdrant_client = QdrantClient(":memory:")

    qdrant_client.add(
        collection_name="support",
        documents=docs,
        ids=ids
        )

    # Init retriever model 
    qdrant_retriever_model = QdrantRM("support", qdrant_client, k=3)
    # Initiate LLama3 Instruct model using Ollama
    ollama_model = dspy.OllamaLocal(model="llama3:instruct",model_type='instruct',
                                    max_tokens=350,
                                    temperature=0.1,
                                    top_p=0.8, frequency_penalty=1.17, top_k=40)

    # Setup retriever and language models in dspy
    dspy.settings.configure(rm=qdrant_retriever_model, lm=ollama_model)
