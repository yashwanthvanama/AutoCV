"""
Fetch a job description from a posting URL using the Claude Agent SDK.

The agent is given a single tool (WebFetch), navigates to the URL, and extracts
the posting's title, company, and full description. It also performs the
liveness check described in the reference flow
(https://github.com/santifer/career-ops/blob/main/modes/scan.md) so we can flag
expired or removed postings before storing them.
"""
import json
import re
from dataclasses import dataclass
from typing import Optional

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    TextBlock,
    query,
)


SYSTEM_PROMPT = """You are a job-posting extraction agent.

Given a single URL to a job posting, use the WebFetch tool to retrieve the page
and extract the posting's details. Follow this flow:

1. Call WebFetch on the provided URL with a prompt that asks for the job title,
   company/employer, location, and the complete job description text (including
   responsibilities, requirements, and qualifications - preserve structure with
   line breaks).
2. Perform a liveness check on the result:
   - ACTIVE signals: visible job title, description body, and an apply action.
   - EXPIRED signals: phrases like "no longer available", "position filled",
     "this job has expired", or a redirect/error page (e.g. `?error=true`).
   If the posting looks expired or removed, set `status` to `expired` and leave
   `job_description` empty.
3. If the page is an ATS listing index rather than a single posting, set
   `status` to `not_a_posting`.
4. Otherwise set `status` to `active`.

Output ONLY a single JSON object on the final turn, no prose, no markdown
fences. Shape:

{
  "status": "active" | "expired" | "not_a_posting" | "error",
  "title": string | null,
  "company": string | null,
  "location": string | null,
  "job_description": string,
  "notes": string | null
}

`job_description` should be the full posting body as plain text. Do not
summarise it. If you truly cannot extract it, set status to "error" and explain
in `notes`."""


@dataclass
class FetchedJobDescription:
    status: str
    title: Optional[str]
    company: Optional[str]
    location: Optional[str]
    job_description: str
    notes: Optional[str]


def _extract_json(text: str) -> Optional[dict]:
    """Pull the first JSON object out of the agent's final text."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Fallback: grab the widest {...} span.
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


async def fetch_job_description_from_url(url: str) -> FetchedJobDescription:
    """Run the extraction agent against a posting URL."""
    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        allowed_tools=["WebFetch"],
        max_turns=6,
    )

    final_text_parts: list[str] = []
    async for message in query(prompt=f"Extract the job posting at: {url}", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    final_text_parts.append(block.text)

    raw = "".join(final_text_parts).strip()
    parsed = _extract_json(raw)

    if parsed is None:
        return FetchedJobDescription(
            status="error",
            title=None,
            company=None,
            location=None,
            job_description="",
            notes=f"Agent did not return parseable JSON. Raw output: {raw[:500]}",
        )

    return FetchedJobDescription(
        status=parsed.get("status", "error"),
        title=parsed.get("title"),
        company=parsed.get("company"),
        location=parsed.get("location"),
        job_description=parsed.get("job_description", "") or "",
        notes=parsed.get("notes"),
    )
