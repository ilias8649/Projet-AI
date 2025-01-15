from utils.embeding import similarity_search
from openai import OpenAI
import os

# Définition de la clé API directement
OPENAI_API_KEY = ""
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return "Une erreur s'est produite lors de la génération de la réponse."

def process_prompt(prompt):
    # Step 1: Find similar content using similarity search
    similar_content = similarity_search(prompt)
    if not similar_content:
        print("No similar content found. Using prompt as is.")
        return "I'm sorry, but I couldn't find relevant information to answer your question."

    # Step 2: Retrieve the most relevant content
    retrieved_texts = [match["metadata"]["text"] for match in similar_content]
    context = "\n".join(retrieved_texts)

    # Step 3: Construct the enhanced prompt
    enhanced_prompt = f"""
    ### Context:
    {context}

    ### Question:
    {prompt}

    ### Answer:
    """

    # Step 4: Generate response using OpenAI
    response = generate_response(enhanced_prompt)
    
    return response
