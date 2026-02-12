"""
Resume data maps for different job roles.
Each map contains base_skills and role_contexts extracted from resume templates.
"""

# AI/ML Engineer Resume Data
AI_ML_ENGINEER = {
    "base_skills": {
        "languages_scripting": "Python, SQL",
        "frameworks_libraries": "TensorFlow, PyTorch, scikit-learn, XGBoost, LangChain, LangGraph, OpenAI API, pandas, NumPy, Apache Spark",
        "tools_platforms": "AWS (SageMaker, Lambda, S3, EC2), ChromaDB, PostgreSQL, MongoDB, FastAPI, Flask, MLflow, Airflow, Docker, Kubernetes, Git",
        "methodologies_concepts": "NLP, RAG, LLMs, Feature Engineering, Model Deployment, A/B Testing, MLOps"
    },
    "role_contexts": [
        {
            "role_id": "R1",
            "company": "Moodys Corporation",
            "title": "AI/ML Engineer 2",
            "start_date": "2025-08",
            "end_date": "present",
            "focus": "LLM-powered credit risk assessment, rating prediction models, MLOps pipelines, RAG systems"
        },
        {
            "role_id": "R2",
            "company": "Cognizant",
            "title": "Machine Learning Engineer 2",
            "start_date": "2022-03",
            "end_date": "2023-07",
            "focus": "predictive pricing models, NLP-powered quote extraction, recommendation engine, feature engineering"
        },
        {
            "role_id": "R3",
            "company": "Cognizant",
            "title": "Machine Learning Engineer 1",
            "start_date": "2020-07",
            "end_date": "2022-03",
            "focus": "ML inference services, churn prediction, ETL pipelines, model monitoring and drift detection"
        }
    ]
}

# Salesforce Administrator Resume Data
SALESFORCE_ADMINISTRATOR = {
    "base_skills": {
        "languages_scripting": "SOQL, SOSL, Apex",
        "frameworks_libraries": "Flow Builder, Process Builder, LWC, Visualforce",
        "tools_platforms": "User Setup, Object Manager, Reports & Dashboards, Data Loader, Workbench, Schema Builder, Change Sets, Salesforce (Sales Cloud, Service Cloud, Experience Cloud, CPQ)",
        "methodologies_concepts": "Permissions, Profiles, Role Hierarchies, Validation Rules, Sharing Rules, Territory Management, Duplicate Rules, Automation (Record-Triggered Flows, Screen Flows, Auto-Launched Flows, Scheduled Flows), Field-Level Security, Organization-Wide Defaults"
    },
    "role_contexts": [
        {
            "role_id": "R1",
            "company": "Moody's Corporation",
            "title": "Salesforce Administrator",
            "start_date": "2025-08",
            "end_date": "present",
            "focus": "user management, permission sets, Flow automation for HR onboarding, custom reports and dashboards, data hygiene, Change Set deployments"
        },
        {
            "role_id": "R2",
            "company": "Comcast",
            "title": "Associate Salesforce Administrator",
            "start_date": "2020-07",
            "end_date": "2023-07",
            "focus": "Case Assignment Rules, Email-to-Case, Omni-Channel routing, Record-Triggered Flows, Territory Management, security monitoring, stakeholder collaboration"
        }
    ]
}

# Salesforce Developer Resume Data
SALESFORCE_DEVELOPER = {
    "base_skills": {
        "languages_scripting": "Apex, JavaScript, HTML, CSS, SOQL, SOSL",
        "frameworks_libraries": "Lightning Web Components, Aura Components, Apex Classes, Triggers, Visualforce, REST/SOAP APIs, Bulk API, Metadata API",
        "tools_platforms": "VS Code, Dataloader, Workbench, Postman, Salesforce CLI, GitHub, Gearset, Jenkins, Salesforce CPQ, Revenue Cloud, Sales Cloud, Service Cloud, Experience Cloud, Conga CLM",
        "methodologies_concepts": "Platform Events, Batch, Schedulable, Queueable jobs, DevOps, CI/CD"
    },
    "role_contexts": [
        {
            "role_id": "R1",
            "company": "Moodys Corporation",
            "title": "Senior Salesforce Developer",
            "start_date": "2025-08",
            "end_date": "present",
            "focus": "record-triggered Flows, Lightning Web Components, Sales Cloud territory management, Service Cloud Omni-Channel, data migration"
        },
        {
            "role_id": "R2",
            "company": "Cognizant Technology Solutions",
            "title": "Salesforce Developer",
            "start_date": "2020-07",
            "end_date": "2023-07",
            "focus": "Salesforce CPQ configuration, Revenue Cloud integration with SAP ERP, asynchronous Apex batch jobs, Conga CLM implementation, DevOps pipelines"
        }
    ]
}

# Software Engineer Resume Data
SOFTWARE_ENGINEER = {
    "base_skills": {
        "languages_scripting": "Python, Java, C, JavaScript, TypeScript, SQL, HTML, CSS",
        "frameworks_libraries": "Spring Boot, React.js, Flask, FastAPI, Kafka, GraphQL, LangGraph",
        "tools_platforms": "Docker, Kubernetes, Jenkins, AWS, PostgreSQL, MongoDB, Selenium, CloudWatch, Datadog",
        "methodologies_concepts": "Microservices Architecture, CI/CD, Test Driven Development, Agile, REST APIs"
    },
    "role_contexts": [
        {
            "role_id": "R1",
            "company": "Moodys Corporation",
            "title": "Software Development Engineer 2",
            "start_date": "2025-08",
            "end_date": "present",
            "focus": "microservices migration, asynchronous messaging with Kafka, Jenkins CI/CD pipelines, GraphQL API gateway"
        },
        {
            "role_id": "R2",
            "company": "Cognizant",
            "title": "Software Development Engineer 2",
            "start_date": "2022-03",
            "end_date": "2023-07",
            "focus": "quoting UI with React and TypeScript, pricing and approval workflows with Python REST APIs, PostgreSQL and MongoDB integration"
        },
        {
            "role_id": "R3",
            "company": "Cognizant",
            "title": "Software Development Engineer 1",
            "start_date": "2020-07",
            "end_date": "2022-03",
            "focus": "AWS microservices deployment, testing with pytest and Selenium, CI/CD with Jenkins and AWS CodePipeline, monitoring with CloudWatch and Datadog"
        }
    ]
}
