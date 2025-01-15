# Import the required libraries
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import time

# Initialize a Pinecone client with your API key
pc = Pinecone(api_key="pcsk_2JvGAp_6NPir4v4Drt4hCyZsGjSh7SoFeebofHS9M5sexhaHwXJfCbZ1HMXitt4cQEcgzA")
index_name="transcript-index"
namespace="transcript-namespace"

def generate_and_store_embedding(text):
    """
    Generates an embedding for the given text and stores it in the specified Pinecone index.

    Parameters:
        text (str): The input text to generate the embedding for.
        index_name (str): The name of the Pinecone index.
        namespace (str): The namespace to store the embedding in.

    Returns:
        None
    """
    # Generate an embedding for the text
    embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[text],
        parameters={"input_type": "passage", "truncate": "END"}
    )

    # Target the index
    index = pc.Index(index_name)

    # Create a record with a unique ID and metadata
    record = {
        "id": f"vec-{int(time.time())}",  # Use a timestamp-based unique ID
        "values": embedding[0].values,  # Embedding vector values
        "metadata": {"text": text}  # Store the original text as metadata
    }

    # Upsert the record into the index
    index.upsert(
        vectors=[record],
        namespace=namespace
    )

    print(f"Text '{text}' has been embedded and stored in the index '{index_name}' under namespace '{namespace}'.")

def similarity_search(query_text, top_k=1):
    """
    Performs a similarity search for the given query text in the specified Pinecone index.

    Parameters:
        query_text (str): The query text to search for similar embeddings.
        index_name (str): The name of the Pinecone index.
        namespace (str): The namespace to search within.
        top_k (int): The number of top similar results to return.

    Returns:
        list: A list of matches with their metadata and similarity scores.
    """
    # Generate an embedding for the query text
    query_embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query_text],
        parameters={"input_type": "query"}
    )

    # Target the index
    index = pc.Index(index_name)

    # Perform similarity search
    results = index.query(
        namespace=namespace,  # Search in the specified namespace
        vector=query_embedding[0].values,  # Query vector
        top_k=top_k,  # Number of top matches to return
        include_values=False,  # Don't return the embedding values
        include_metadata=True  # Return metadata
    )

    # Print and return the search results
    print("Similarity Search Results:")
    for match in results['matches']:
        print(f"ID: {match['id']}, Score: {match['score']}, Metadata: {match['metadata']}")

    return results['matches']
