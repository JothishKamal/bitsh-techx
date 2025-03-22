import cohere
import os
from typing import List, Optional

# Initialize Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))

def generate_embedding(text: str) -> List[float]:
    """Generate embeddings using Cohere's FIM model."""
    if not text:
        return []
    
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    return response.embeddings[0]

def generate_form_embeddings(name: str, description: Optional[str] = None) -> List[float]:
    """Generate embeddings for a form based on its name and description."""
    text = name
    if description:
        text += " " + description
    
    return generate_embedding(text)