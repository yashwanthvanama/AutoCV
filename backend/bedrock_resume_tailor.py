import json
import os
import boto3
from typing import Dict, Any
from dotenv import load_dotenv
from resume_tailor_prompt import RESUME_TAILOR_PROMPT

# Load environment variables from .env file
load_dotenv()


def tailor_resume(job_description: str, base_skills: Dict[str, str], role_contexts: list) -> Dict[str, Any]:
    """
    Call Claude Sonnet 4.5 on Amazon Bedrock to tailor a resume based on job description.
    
    Args:
        job_description: The job description text
        base_skills: Dictionary with skills categories (languages_scripting, frameworks_libraries, etc.)
        role_contexts: List of role context objects with timeline and allowed_tech
    
    Returns:
        Dictionary containing tailored skills and experience bullets
    """
    
    # Format the inputs for the prompt
    base_skills_str = json.dumps(base_skills, indent=2)
    role_contexts_str = json.dumps(role_contexts, indent=2)
    
    # Construct the prompt using the template
    prompt = RESUME_TAILOR_PROMPT.format(
        job_description=job_description,
        base_skills=base_skills_str,
        role_contexts=role_contexts_str
    )

    # Initialize Bedrock client with credentials from environment variables
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    
    # Prepare the request body for Claude Sonnet 4.5
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3  # Lower temperature for more consistent, focused output
    }
    
    # Call Bedrock - using US inference profile for Claude Sonnet 4.5
    # This provides better availability within US regions
    response = bedrock_runtime.invoke_model(
        modelId='us.anthropic.claude-sonnet-4-5-20250929-v1:0',
        body=json.dumps(request_body)
    )
    
    # Parse response
    response_body = json.loads(response['body'].read())
    
    # Extract the content from Claude's response
    assistant_message = response_body['content'][0]['text']
    
    # Clean the response - remove markdown code blocks if present
    assistant_message = assistant_message.strip()
    if assistant_message.startswith('```'):
        # Remove markdown code fences
        lines = assistant_message.split('\n')
        assistant_message = '\n'.join(lines[1:-1]) if len(lines) > 2 else assistant_message
        assistant_message = assistant_message.replace('```json', '').replace('```', '').strip()
    
    # Parse the JSON response
    tailored_resume = json.loads(assistant_message)
    
    return tailored_resume


def main():
    """
    Example usage of the resume tailoring function.
    """
    # Example inputs
    job_description = """
    Senior Software Engineer
    We are looking for a senior software engineer with experience in Python, AWS, 
    and microservices architecture. The ideal candidate will have strong backend 
    development skills and experience with cloud infrastructure.
    """
    
    base_skills = {
        "languages_scripting": "Python, JavaScript, SQL, Bash",
        "frameworks_libraries": "FastAPI, React, SQLAlchemy, Pandas",
        "tools_platforms": "AWS, Docker, Git, PostgreSQL",
        "methodologies_concepts": "Microservices, REST APIs, CI/CD, Agile"
    }
    
    role_contexts = [
        {
            "role_id": "R1",
            "company": "Tech Corp",
            "title": "Senior Software Engineer",
            "start_date": "2022-01",
            "end_date": "present",
            "focus": "quoting platform modernization, async messaging, CI/CD, API gateway"
        },
        {
            "role_id": "R2",
            "company": "StartupXYZ",
            "title": "Software Engineer",
            "start_date": "2020-03",
            "end_date": "2021-12",
            "focus": "quoting UI, pricing/approval workflows, integrations"
        }
    ]
    
    try:
        result = tailor_resume(job_description, base_skills, role_contexts)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
