import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY", "")

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from fastapi import APIRouter
from pydantic import BaseModel
from ai.vector_store import search_notes

llm = ChatGroq(model="llama-3.3-70b-versatile")


class ReActAgent:
    def __init__(self):
        self.conversation_history = []

    def chat(self, user_message: str) -> dict:
        # Search relevant notes from Chroma
        relevant = search_notes(user_message, n_results=3)
        context = ""
        if relevant:
            context = "Here are relevant notes from the user's Second Brain:\n"
            for r in relevant:
                context += f"- [{r['topic']}] {r['content']}\n"

        system = f"""You are an intelligent second-brain assistant.
You help the user recall and reason about their notes.

{context}

Answer the user's question based on their notes above.
If no relevant notes exist, answer from your general knowledge and clearly say 
that this answer comes from your general knowledge, not from their notes."""

        self.conversation_history.append(HumanMessage(content=user_message))
        messages = [SystemMessage(content=system)] + self.conversation_history
        response = llm.invoke(messages)
        answer = response.content
        self.conversation_history.append(AIMessage(content=answer))
        return {
            "full_response": answer,
            "thoughts": [],
            "final_answer": answer
        }

    def reset(self):
        self.conversation_history = []


agent_router = APIRouter(prefix="/agent", tags=["agent"])
_global_agent = ReActAgent()


class AgentChatRequest(BaseModel):
    message: str
    reset: bool = False


@agent_router.post("/chat")
def agent_chat(payload: AgentChatRequest):
    if payload.reset:
        _global_agent.reset()
    return _global_agent.chat(payload.message)


@agent_router.delete("/chat/reset")
def reset_agent():
    _global_agent.reset()
    return {"message": "Conversation reset successfully"}