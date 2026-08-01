
import json
import time
import re
from langchain_core.messages import  SystemMessage,HumanMessage
from backend.config import get_llm

# ---------------------------------------------------------
# Judge LLM
# ---------------------------------------------------------

judge_llm = get_llm()

# ---------------------------------------------------------
# Extract JSON from LLM response
# ---------------------------------------------------------

def extract_json(text: str) -> dict:
    """
    Extract JSON object from LLM response.
    Handles extra markdown and strips hallucinated comments.
    """
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        json_text = text[start:end]
        
        # Remove any // comments the smaller 8B LLM might hallucinate
        json_text = re.sub(r'//.*', '', json_text)
        
        return json.loads(json_text)
        
    except Exception:
        print("\n========== JUDGE PARSE ERROR ==========")
        print(text)
        print("=======================================\n")
        raise

# ---------------------------------------------------------
# Generic Judge
# ---------------------------------------------------------

def judge(
    prompt_template: str,
    **kwargs,
):
    """
    Generic LLM-as-a-Judge with Rate Limit handling.
    """
    prompt = prompt_template.format(**kwargs)
    
    messages = [
        SystemMessage(
            content="""
You are an impartial evaluator.

Your task is ONLY to score the AI output.

Rules:
1. Return ONLY strict JSON.
2. Do NOT explain your thoughts outside the JSON.
3. Do NOT use markdown.
4. Give fair scores based on the provided 1-5 scale.
5. If information is missing or hallucinates, reduce the score.
"""
        ),
        HumanMessage(content=prompt),
    ]

    # --- Retry Logic for Groq API Rate Limits ---
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = judge_llm.invoke(messages)
            return extract_json(response.content)
            
        except Exception as e:
            error_msg = str(e)
            
            # If it's a Rate Limit (429) error, wait and retry
            if "429" in error_msg or "Rate limit" in error_msg or "rate_limit_exceeded" in error_msg:
                print(f"\n⏳ [Rate Limit Hit] Groq needs a break. Sleeping for 5 seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(5)  # Wait 5 seconds before trying again
            else:
                # If it's a different error (like a network drop), crash normally
                raise e
                
    raise Exception("Max retries exceeded due to Groq rate limits. Try evaluating fewer examples.")


