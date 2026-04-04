from google import genai
from ai.notes_ai import chercher_notes

client = genai.Client()

def rag_answer(question: str):
    notes = chercher_notes(question)
    if isinstance(notes, str):
        notes = [notes]
    context = "\n".join(notes)

    prompt = f"""
You are an AI second brain assistant.

Use ONLY these notes:

{context}

Question:
{question}

Answer clearly.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "answer": response.text,
        "used_notes": notes
    }