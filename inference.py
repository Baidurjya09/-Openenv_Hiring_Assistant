"""
OpenEnv Competition Compliant Inference Script
===============================================

MANDATORY STDOUT FORMAT:
[START] task=<task_name> env=<benchmark> model=<model_name>
[STEP]  step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
[END]   success=<true|false> steps=<n> score=<score> rewards=<r1,r2,...,rn>

Environment variables:
  API_BASE_URL  - OpenAI-compatible API base URL
  MODEL_NAME    - Model to use
  HF_TOKEN      - API key / HuggingFace token
"""

import json
import os
import sys
import re
from typing import List

from openai import OpenAI

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from env.hiring_env import HiringEnv
from models.schemas import Action


# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

API_BASE_URL = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.environ.get("HF_TOKEN", "")
BENCHMARK = "ai-hiring-assistant"

if not HF_TOKEN:
    print("WARNING: HF_TOKEN is not set. Requests may fail if authentication is required.", file=sys.stderr)

client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)


# ------------------------------------------------------------------
# Prompt builder
# ------------------------------------------------------------------

def build_prompt(observation) -> str:
    """Build prompt for LLM to select candidates."""
    job = observation.job_description
    resumes = observation.resumes

    resumes_text = ""
    for r in resumes:
        resumes_text += (
            f"\n- ID: {r['id']}\n"
            f"  Name: {r['name']}\n"
            f"  Skills: {', '.join(r['skills'])}\n"
            f"  Experience: {r['experience_years']} years\n"
            f"  Summary: {r['summary']}\n"
        )

    prompt = f"""You are an expert technical recruiter. Your task is to screen candidates for the following job.

## Job Description
Title: {job['title']}
Required Skills: {', '.join(job['required_skills'])}
Preferred Skills: {', '.join(job['preferred_skills'])}
Minimum Experience: {job['min_experience_years']} years
Description: {job['description']}

## Candidates
{resumes_text}

## Instructions
Review each candidate carefully. Select ONLY the candidates who best match the job requirements.
A candidate must have ALL required skills and meet the minimum experience threshold to be selected.
Prefer candidates who also have preferred skills.

Respond with ONLY a JSON object in this exact format (no explanation, no markdown):
{{"selected_candidates": ["<candidate_id>", ...]}}

If no candidate qualifies, return: {{"selected_candidates": []}}
"""
    return prompt


# ------------------------------------------------------------------
# Response parser
# ------------------------------------------------------------------

def parse_response(content: str) -> List[str]:
    """Extract selected_candidates list from model response."""
    # Try direct JSON parse first
    try:
        data = json.loads(content.strip())
        return data.get("selected_candidates", [])
    except json.JSONDecodeError:
        pass

    # Fallback: extract JSON object via regex
    match = re.search(r'\{.*?"selected_candidates"\s*:\s*\[.*?\].*?\}', content, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            return data.get("selected_candidates", [])
        except json.JSONDecodeError:
            pass

    return []


# ------------------------------------------------------------------
# Main evaluation loop
# ------------------------------------------------------------------

def run_task(task_name: str, difficulty: str) -> dict:
    """
    Run a single task and return results.
    
    Returns:
        dict with keys: success, steps, score, rewards, error
    """
    rewards = []
    error = None
    
    # Emit [START] line
    print(f"[START] task={task_name} env={BENCHMARK} model={MODEL_NAME}")
    
    try:
        # Create environment
        env = HiringEnv(difficulty=difficulty)
        observation = env.reset()
        
        # Build prompt
        prompt = build_prompt(observation)
        
        # Call LLM
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=256,
            )
            content = response.choices[0].message.content.strip()
        except Exception as e:
            error = f"API call failed: {str(e)}"
            content = '{"selected_candidates": []}'
        
        # Parse response
        selected = parse_response(content)
        
        # Create action string for logging
        action_str = json.dumps({"selected_candidates": selected})
        
        # Execute step
        action = Action(selected_candidates=selected)
        result = env.step(action)
        
        # Extract results
        reward = result.reward.score
        done = result.done
        rewards.append(reward)
        
        # Emit [STEP] line
        error_str = error if error else "null"
        done_str = "true" if done else "false"
        print(f"[STEP]  step=1 action={action_str} reward={reward:.2f} done={done_str} error={error_str}")
        
        # Calculate final score (same as reward for single-step)
        score = reward
        success = (score >= 0.95)  # Consider >= 0.95 as success since max is 0.9999
        
        return {
            "success": success,
            "steps": 1,
            "score": score,
            "rewards": rewards,
            "error": error
        }
        
    except Exception as e:
        error = str(e)
        return {
            "success": False,
            "steps": 0,
            "score": 0.0,
            "rewards": [0.0],
            "error": error
        }


def main():
    """Run all tasks and emit compliant output."""
    
    tasks = [
        ("task_easy_001", "easy"),
        ("task_medium_001", "medium"),
        ("task_hard_001", "hard"),
        ("task_management_001", "management"),
        ("task_marketing_001", "marketing"),
        ("task_business_001", "business"),
    ]
    
    all_scores = []
    
    for task_name, difficulty in tasks:
        result = run_task(task_name, difficulty)
        
        # Emit [END] line
        success_str = "true" if result["success"] else "false"
        rewards_str = ",".join([f"{r:.2f}" for r in result["rewards"]])
        print(f"[END]   success={success_str} steps={result['steps']} score={result['score']:.2f} rewards={rewards_str}")
        
        all_scores.append(result["score"])
    
    # Print summary to stderr (not part of required stdout format)
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0.0
    print(f"\n=== Summary ===", file=sys.stderr)
    print(f"Easy:       {all_scores[0]:.2f}", file=sys.stderr)
    print(f"Medium:     {all_scores[1]:.2f}", file=sys.stderr)
    print(f"Hard:       {all_scores[2]:.2f}", file=sys.stderr)
    print(f"Management: {all_scores[3]:.2f}", file=sys.stderr)
    print(f"Marketing:  {all_scores[4]:.2f}", file=sys.stderr)
    print(f"Business:   {all_scores[5]:.2f}", file=sys.stderr)
    print(f"Average:    {avg_score:.2f}", file=sys.stderr)
    
    return avg_score


if __name__ == "__main__":
    main()
