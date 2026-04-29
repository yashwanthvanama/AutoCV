"""Tailor a resume .tex file in place using the Claude Agent SDK.

Reads the template from templates/, copies it into the submission folder, and asks
the agent to rewrite the Professional Summary, Work Experience bullets, and Skills
sections to match the job description. The agent is scoped to the submission folder
and restricted to Read/Edit only.
"""

import shutil
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, query

from template_manager import get_template_for_role

SYSTEM_PROMPT = """You are a resume-tailoring agent editing a LaTeX (.tex) resume file in place.

SCOPE — edit ONLY these three sections:
  1. \\section*{Professional Summary} — rewrite the paragraph so it targets the job description.
  2. \\section*{Work Experience} — rewrite each \\item bullet inside every \\begin{itemize}...\\end{itemize}.
  3. \\section*{Skills} — reorder / lightly edit the comma-separated lists after each \\textbf{...:} label.

HARD RULES:
- DO NOT modify any \\subsection{Company | Title | Dates} header line — companies, titles, and dates are authoritative.
- DO NOT touch the \\section*{Projects}, \\section*{Education}, the header \\begin{center} block, or any \\usepackage / \\setmainfont / \\titleformat / \\setlist preamble.
- Keep the same number of bullets per role as the original. Each bullet: one sentence, 22-32 words, action + system/feature + tech + outcome.
- Preserve LaTeX escaping: & -> \\&, % -> \\%, $ -> \\$, # -> \\#. Keep existing \\href{...}{...} links intact.
- No anachronisms: do not mention a technology inside a role whose end date predates that technology's release (e.g. no LangGraph/Bedrock/ChatGPT in roles ending before late 2022; no GitHub Copilot before 2021).
- Use the Edit tool to make targeted replacements. Do not rewrite the whole file with Write. Make multiple Edit calls if needed.
- When finished, reply with a single line: DONE.
"""


def _build_prompt(job_description: str, role: str, tex_filename: str) -> str:
    return f"""Tailor the resume in `{tex_filename}` to the job description below.

TARGET ROLE: {role}

JOB DESCRIPTION:
{job_description}

Steps:
1. Read `{tex_filename}`.
2. Edit the Professional Summary, Work Experience bullets, and Skills section to match the JD while obeying the rules in your system prompt.
3. Reply with `DONE` when the file is saved.
"""


async def tailor_resume_tex(
    role: str, job_description: str, record_folder: Path
) -> Path | None:
    """Copy the role's template into record_folder and tailor it to the JD.

    Returns the path to the tailored .tex, or None if the role has no template.
    """
    template_filename = get_template_for_role(role)
    if not template_filename:
        print(f"agent_tailor: no template mapped for role {role!r}")
        return None

    templates_dir = Path(__file__).parent.parent / "templates"
    source = templates_dir / template_filename
    if not source.exists():
        print(f"agent_tailor: template not found at {source}")
        return None

    destination = record_folder / template_filename
    shutil.copy2(source, destination)
    print(f"agent_tailor: copied template -> {destination}")

    options = ClaudeAgentOptions(
        cwd=str(record_folder),
        allowed_tools=["Read", "Edit"],
        permission_mode="dontAsk",
        system_prompt=SYSTEM_PROMPT,
    )

    prompt = _build_prompt(job_description, role, template_filename)

    print("agent_tailor: invoking Claude Agent SDK...")
    async for message in query(prompt=prompt, options=options):
        msg_type = type(message).__name__
        if msg_type == "AssistantMessage":
            for block in getattr(message, "content", []) or []:
                text = getattr(block, "text", None)
                if text:
                    print(f"agent: {text[:200]}")
        elif msg_type == "ResultMessage":
            print(f"agent_tailor: done (result message received)")

    return destination
