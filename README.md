---
title: AI Hiring Assistant
emoji: 💼
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
license: apache-2.0
tags:
  - openenv
  - hiring
  - nlp
  - reasoning
  - evaluation
---

# AI Hiring Assistant — OpenEnv Environment

A production-ready OpenEnv environment that simulates a technical recruiter screening job candidates. Designed for evaluating LLM agents on structured reasoning tasks involving skill matching, experience thresholds, and multi-criteria decision making.

---

## Problem Description

Hiring is one of the most consequential decisions in any organization. This environment tests whether an AI agent can act as a competent recruiter — reading a job description, reviewing candidate resumes, and selecting the best-fit candidates based on required skills, preferred skills, and experience.

## Motivation

Real-world hiring involves:
- Matching hard requirements (must-have skills, minimum experience)
- Weighing soft preferences (nice-to-have skills)
- Avoiding false positives (selecting unqualified candidates)
- Avoiding false negatives (missing qualified candidates)

This environment captures all of these dimensions in a clean, evaluable format.

---

## Environment Design

The environment follows the OpenEnv specification and supports 6 diverse tasks across multiple domains (IT, Management, Marketing, Business):

```
reset()         → Observation
step(action)    → (Observation, Reward, done, info)
state()         → dict
```

### Observation Space

| Field            | Type              | Description                              |
|------------------|-------------------|------------------------------------------|
| job_description  | dict              | Job title, required/preferred skills, min experience, description |
| resumes          | list[dict]        | Candidate profiles with skills, experience, summary |
| task_id          | string            | Unique task identifier                   |
| difficulty       | easy/medium/hard  | Task difficulty level                    |

### Action Space

| Field               | Type        | Description                          |
|---------------------|-------------|--------------------------------------|
| selected_candidates | list[str]   | Candidate IDs chosen by the agent    |

---

## Task Descriptions

### Easy (IT/Technical)
- Job: Junior Python Developer
- Pool: 4 candidates
- Challenge: One candidate clearly matches (Python + Git + experience). Others are Java devs, designers, or analysts.
- Correct answer: `["c_easy_001"]`

### Medium (IT/Technical)
- Job: Full Stack Engineer (JS, React, Node.js, SQL)
- Pool: 5 candidates
- Challenge: Multiple candidates have partial overlaps. Two satisfy all required + preferred skills. Requires distinguishing strong fits from partial fits.
- Correct answer: `["c_med_001", "c_med_005"]`

### Hard (IT/Technical)
- Job: Senior ML Engineer (PyTorch, MLOps, 5+ years)
- Pool: 5 very similar ML candidates
- Challenge: All candidates have Python and ML experience. Requires reasoning over PyTorch vs TensorFlow, presence of MLOps, preferred skills (Kubernetes, Spark, LLMs, CUDA), and experience years.
- Correct answer: `["c_hard_001", "c_hard_002"]`

### Management
- Job: Product Manager (MBA, Agile/Scrum, Product Strategy)
- Pool: 3 candidates
- Challenge: Requires matching management candidates with leadership skills, distinguishing between technical PMs and strategic PMs.
- Correct answer: `["c_mgmt_001"]`

### Marketing
- Job: Marketing Manager (Digital Marketing, SEO/SEM, Analytics)
- Pool: 3 candidates
- Challenge: Evaluating marketing professionals with diverse backgrounds in content, digital, and growth marketing.
- Correct answer: `["c_mkt_001"]`

### Business
- Job: Business Analyst (SQL, Excel, Business Intelligence)
- Pool: 3 candidates
- Challenge: Matching business-focused candidates with analytical skills, distinguishing between finance, operations, and data analysis backgrounds.
- Correct answer: `["c_biz_001"]`

---

## Reward Logic

Scoring uses the **F1 metric** for multi-label selection:

```
precision = correct_selections / total_selected
recall    = correct_selections / total_correct
score     = 2 * precision * recall / (precision + recall)
```

- Score range: `0.0` to `1.0`
- `1.0` = perfect selection (no false positives, no missed candidates)
- Partial credit for partially correct selections
- `0.0` for empty selection or completely wrong selection
- Deterministic — no randomness

---

## Project Structure

```
hiring-openenv/
├── env/
│   └── hiring_env.py       # Core OpenEnv environment
├── models/
│   └── schemas.py          # Pydantic models (Observation, Action, Reward)
├── tasks/
│   ├── easy.py             # Easy task definition (IT)
│   ├── medium.py           # Medium task definition (IT)
│   ├── hard.py             # Hard task definition (IT)
│   ├── management.py       # Management task definition
│   ├── marketing.py        # Marketing task definition
│   └── business.py         # Business task definition
├── graders/
│   ├── base_grader.py      # Abstract grader interface
│   └── hiring_grader.py    # F1-based deterministic grader
├── data/
│   ├── jobs.json           # Job descriptions
│   └── resumes.json        # Candidate resume pools
├── inference.py            # End-to-end evaluation script
├── openenv.yaml            # Environment metadata
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Setup & Running

### For OpenEnv Validator

The validator automatically injects these environment variables:
- `API_KEY` — Authentication key for the LiteLLM proxy
- `API_BASE_URL` — Base URL for the LiteLLM proxy
- `MODEL_NAME` — Model to use for inference

Your code must use these variables to ensure API calls are tracked.

### Local Testing

For local development and testing, you can use `HF_TOKEN` instead of `API_KEY`:

```bash
cd hiring-openenv
pip install -r requirements.txt
```

**Linux/macOS:**
```bash
export HF_TOKEN=your_api_key
export MODEL_NAME=gpt-4o-mini
export API_BASE_URL=https://router.huggingface.co/v1
python inference.py
```

**Windows (PowerShell):**
```powershell
$env:HF_TOKEN = "your_api_key"
$env:MODEL_NAME = "gpt-4o-mini"
$env:API_BASE_URL = "https://router.huggingface.co/v1"
python inference.py
```

**Windows (CMD):**
```cmd
set HF_TOKEN=your_api_key
set MODEL_NAME=gpt-4o-mini
set API_BASE_URL=https://router.huggingface.co/v1
python inference.py
```

### Docker

```bash
docker build -t hiring-openenv .

docker run \
  -e HF_TOKEN=your_api_key \
  -e MODEL_NAME=gpt-4o-mini \
  -e API_BASE_URL=https://router.huggingface.co/v1 \
  hiring-openenv
```

### Using a HuggingFace-hosted model

```bash
docker run \
  -e HF_TOKEN=hf_xxxxxxxxxxxx \
  -e MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct \
  -e API_BASE_URL=https://api-inference.huggingface.co/v1 \
  hiring-openenv
```

---

## Example Output

```
============================================================
  AI Hiring Assistant — OpenEnv Evaluation
============================================================
  Model     : gpt-4o-mini
  API Base  : https://api.openai.com/v1
============================================================

[Task: EASY]
  Job      : Junior Python Developer
  Resumes  : 4 candidates
  Selected : ['c_easy_001']
  Score    : 1.0000
  Feedback : Perfect selection. All correct candidates identified with no false positives.
  Correct  : ['c_easy_001']

[Task: MEDIUM]
  Job      : Full Stack Engineer
  Resumes  : 5 candidates
  Selected : ['c_med_001', 'c_med_005']
  Score    : 1.0000
  Feedback : Perfect selection. All correct candidates identified with no false positives.
  Correct  : ['c_med_001', 'c_med_005']

[Task: HARD]
  Job      : Senior ML Engineer
  Resumes  : 5 candidates
  Selected : ['c_hard_001', 'c_hard_002']
  Score    : 1.0000
  Feedback : Perfect selection. All correct candidates identified with no false positives.
  Correct  : ['c_hard_001', 'c_hard_002']

============================================================
  Scores   : easy=1.0000  medium=1.0000  hard=1.0000
  Average  : 1.0000
============================================================
```

---

## Resource Requirements

- CPU: 2 vCPU
- Memory: 8GB RAM
- Inference time: < 20 minutes (typically < 2 minutes for fast models)

---

## Dependencies

- `openai>=1.14.0` — OpenAI-compatible client
- `pydantic>=2.0.0` — Data validation and schemas
- `pyyaml>=6.0` — YAML config parsing
