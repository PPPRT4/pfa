from langsmith.evaluation import evaluate
from Langgraph_agent.eval_agent import run_my_agent
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

from langsmith.evaluation import run_evaluator
import json
import re

def safe_parse(output):
    try:
        return json.loads(output)
    except:
        match = re.search(r"\{.*\}", output, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
    return {
        "correctness": 0,
        "relevance": 0,
        "hallucination": 0,
        "conciseness": 0,
        "final_score": 0,
        "reason": output
    }


api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

@run_evaluator
def correctness_evaluator(run, example):
    question = example.inputs["question"]
    prediction = run.outputs["answer"]
    reference = example.outputs.get("answer", "")

    prompt = f"""
You are a strict and objective AI evaluator.

Use the reference answer as the primary source of truth, 
but allow semantically equivalent answers.
Do NOT use external knowledge.

---------------------
Question:
{question}

Reference Answer (ground truth):
{reference}

Model Answer:
{prediction}
---------------------
SPECIAL CASE — NO INFORMATION / NO RELATION:

If the reference answer indicates that the information is NOT present in the notes 
(e.g., "not in the notes", "cannot answer from notes", "no specific guidance", etc.),

AND the model answer expresses the SAME idea 
(e.g., "no clear relation", "not found", "no info available"),

THEN:
- correctness = 1.0
- relevance = 1.0
- hallucination = 1.0
- conciseness = 1.0

These answers MUST be considered semantically equivalent 
even if wording is completely different.

Evaluation criteria:

1. Correctness (0-1)
- 1.0: Fully correct, matches reference meaning
- 0.5: Partially correct or missing key details
- 0.0: Incorrect

2. Relevance (0-1)
- 1.0: Fully answers the question
- 0.5: Partially relevant / incomplete
- 0.0: Irrelevant

3. Hallucination (0-1)
- 1.0: Every claim is directly supported or logically implied by the reference
- 0.5: Contains minor extra details not in reference but not harmful
- 0.0: Contains unsupported, fabricated, or contradictory information

CRITICAL:
If the model adds facts not present in the reference, reduce the score.

4. Conciseness (0-1)
- 1.0: Answer is clear and not unnecessarily verbose
- 0.5: Slightly verbose
- 0.0: Overly long or unfocused
---------------------

Final score rule:
- Final score = (correctness * 0.4) + (relevance * 0.3) + (hallucination * 0.2) + 
(conciseness * 0.1)

---------------------

IMPORTANT RULES:
- Be STRICT (do not give high scores easily)
- Penalize hallucinations heavily
If the reference is empty:
    - Ignore hallucination score
    - Final score = (correctness * 0.6) + (relevance * 0.4)
- Output MUST be valid JSON
- DO NOT add any text outside JSON

---------------------

Return format:
{{
  "correctness": float,
  "relevance": float,
  "hallucination": float,
   "conciseness": float,
  "final_score": float,
  "reason": "short, precise explanation"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a strict AI evaluator."},
            {"role": "user", "content": prompt}
        ]
    )

    output = response.choices[0].message.content

    # try to extract score safely

    output = response.choices[0].message.content
    result = safe_parse(output)

    return {
        "score": result.get("final_score", 0),
        "comment": result.get("reason", ""),
        "metadata": result  
    }

evaluate(
    run_my_agent,
    data="second_brain_eval_v1",
    evaluators=[correctness_evaluator]

)