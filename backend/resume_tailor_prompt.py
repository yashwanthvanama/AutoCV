"""
Prompt template for resume tailoring using Claude on Amazon Bedrock.
"""

RESUME_TAILOR_PROMPT = """You are an expert resume-tailoring model.

TASK
Given the JOB DESCRIPTION and the candidate's ROLE CONTEXTS + BASE SKILLS, generate ONLY:
1) an updated Skills section (same structure as BASE_SKILLS, but reordered and minimally edited to match the JD),
2) updated bullet points for each Work Experience role (keep role order and dates unchanged).

HARD OUTPUT RULES (to avoid wasted tokens)
- Output MUST be valid JSON only. No commentary, no markdown, no extra keys.
- Output MUST follow exactly this schema:

{{
  "skills": {{
    "languages_scripting": "comma-separated list",
    "frameworks_libraries": "comma-separated list",
    "tools_platforms": "comma-separated list",
    "methodologies_concepts": "comma-separated list"
  }},
  "experience": [
    {{
      "role_id": "R1|R2|R3",
      "bullets": [
        "bullet 1",
        "bullet 2",
        "bullet 3",
        "bullet 4"
      ]
    }}
  ]
}}

CONTENT RULES (quality + concision)
- Each role MUST have exactly 4 bullets.
- Each bullet MUST be 1 sentence, 22–32 words, resume-style, past tense for past roles, present tense allowed for current role.
- Bullets MUST be highly specific: action + system/feature + tech + outcome.
- Use metrics only when plausible; avoid stuffing percentages. Prefer variety: latency, throughput, #users, $ impact, incidents, SLO, build time, deploy frequency, etc.
- Do NOT invent employers, titles, or dates. Do NOT change the role timeline.

TIME-PERIOD REALISM (no anachronisms)
For each role, you MUST obey the allowed tech list for that role.
- You MUST NOT mention technologies/tools that launched after the role's end date.
- If the JD requests a modern tool that conflicts with a role's time window, express the capability using period-appropriate equivalents from allowed_tech.

ANACHRONISM GUARDRAILS (examples, not exhaustive)
- Do NOT mention: GitHub Copilot before 2021; ChatGPT/Bedrock/modern LLM tooling before late 2022; LangGraph before 2024.
- If unsure about a tool's timeline, do NOT use it (choose a safer alternative from that time period).

INPUTS

JOB_DESCRIPTION:
{job_description}

BASE_SKILLS (use as the exact structural target; you may reorder and minimally edit items):
{base_skills}

ROLE_CONTEXTS (timeline is authoritative; do not alter):
{role_contexts}

NOW PRODUCE JSON ONLY."""
