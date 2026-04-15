from langsmith.evaluation import evaluate
from Langgraph_agent.eval_agent import run_my_agent
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

from langsmith.evaluation import run_evaluator


api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

@run_evaluator
def correctness_evaluator(run, example):
    question = example.inputs["input"]
    prediction = run.outputs["output"]
    reference = example.outputs.get("answer", "")

    prompt = f"""
You are an expert evaluator.

Your task is to grade an AI answer.

Question:
{question}

Reference Answer:
{reference}

Model Answer:
{prediction}

Evaluate:
- correctness
- relevance
- hallucination

Return ONLY JSON like:
{{
  "score": 0 to 1,
  "reason": "short explanation"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a strict AI evaluator."},
            {"role": "user", "content": prompt}
        ]
    )

    output = response.choices[0].message.content

    # try to extract score safely
    try:
        import json
        result = json.loads(output)
        score = result.get("score", 0)
        reason = result.get("reason", "")
    except:
        score = 0
        reason = output

    return {
        "score": score,
        "comment": reason
    }

evaluate(
    run_my_agent,
    data="PFA",
    evaluators=[correctness_evaluator]

)