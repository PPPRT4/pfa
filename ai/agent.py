import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from fastapi import APIRouter
from pydantic import BaseModel

os.environ.setdefault("GROQ_API_KEY", "")

REACT_SYSTEM_PROMPT = """You are an intelligent second-brain assistant using the ReAct reasoning pattern.

For every user question, you MUST follow this exact structure:

Thought 1: [Analyze what the user is really asking. What do they need?]
Thought 2: [Think about what information or reasoning is needed to answer well.]
Thought 3: [Formulate your approach before giving the final answer.]
Final Answer: [Your complete, helpful answer based on your reasoning above.]

Rules:
- ALWAYS show your thoughts before the final answer
- The Final Answer must directly address the user's question
- You are helping users organize their second brain (notes, ideas, tasks, research)
"""

class ReActAgent:
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.llm = ChatGroq(model=model)
        self.conversation_history = []

    def chat(self, user_message: str) -> dict:
        self.conversation_history.append(HumanMessage(content=user_message))
        messages = [SystemMessage(content=REACT_SYSTEM_PROMPT)] + self.conversation_history
        response = self.llm.invoke(messages)
        full_response = response.content
        self.conversation_history.append(AIMessage(content=full_response))
        thoughts, final_answer = self._parse(full_response)
        return {"full_response": full_response, "thoughts": thoughts, "final_answer": final_answer}

    def reset(self):
        self.conversation_history = []

    def _parse(self, response: str):
        lines = response.strip().split("\n")
        thoughts = []
        final_answer_lines = []
        in_final = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Thought") and ":" in line:
                thoughts.append(line.split(":", 1)[1].strip())
                in_final = False
            elif line.startswith("Final Answer:"):
                start = line.split(":", 1)[1].strip()
                if start:
                    final_answer_lines.append(start)
                in_final = True
            elif in_final:
                final_answer_lines.append(line)
        final_answer = "\n".join(final_answer_lines).strip()
        if not final_answer:
            final_answer = response.strip()
        return thoughts, final_answer


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