# CloudOps Portfolio API

CloudOps Portfolio API is a Python-based API and infrastructure engineering project demonstrating **REST API development, automated testing, infrastructure as code, AWS-oriented architecture, local cloud simulation, and CI/CD automation**.

The project is designed to demonstrate how application code, automated quality checks, and infrastructure configuration can be developed and validated together in a reproducible local environment.

---

## Overview

CloudOps Portfolio API combines application development with cloud and DevOps engineering practices.

The project demonstrates:

- REST API development with FastAPI
- CRUD application workflows
- Automated testing with Pytest
- Python code quality with Flake8
- Infrastructure as Code with Terraform
- AWS-oriented infrastructure patterns
- Local AWS-compatible development with LocalStack
- Automated CI validation with GitHub Actions
- Local-first development without requiring paid AWS infrastructure

---

## Architecture

```text
                         Developer
                             |
                             v
                       Git Repository
                             |
                             v
                       GitHub Actions
                             |
              +--------------+--------------+
              |              |              |
              v              v              v
           Flake8         Pytest       Terraform
           Linting        Tests        Validation
              |              |              |
              +--------------+--------------+
                             |
                             v
                       CloudOps API
                             |
                             v
                          FastAPI
                             |
                +------------+------------+
                |                         |
                v                         v
          Application Logic       Cloud Infrastructure
                                      |
                                      v
                                  Terraform
                                      |
                                      v
                                   LocalStack


Technology Stack
Application
Python
FastAPI
REST API
CRUD operations
Testing and Quality
Pytest
Flake8
Automated test validation
Infrastructure
Terraform
AWS infrastructure patterns
LocalStack
Infrastructure as Code
CI/CD
GitHub Actions
Automated linting
Automated testing
Terraform validation
API Capabilities

The API provides CRUD operations for portfolio project resources.

The application supports workflows for:

Create Project
      |
      v
Read Project
      |
      v
List Projects
      |
      v
Update Project
      |
      v
Delete Project

The test suite also covers request validation.

Project Structure
cloudops-portfolio-api/
|
|-- app/
|   |
|   `-- API application
|
|-- tests/
|   |
|   +-- test_create_project.py
|   +-- test_get_project.py
|   +-- test_list_projects.py
|   +-- test_update_project.py
|   +-- test_delete_project.py
|   `-- test_validation.py
|
|-- infra/
|   `-- envs/
|       `-- dev/
|
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|
|-- requirements.txt
|
`-- README.md
Automated Testing

The project currently contains 34 automated tests covering API functionality and validation.

Test coverage includes:

Project creation
Project retrieval
Project listing
Project updates
Project deletion
Request validation

Install the project dependencies:

pip install -r requirements.txt

Install the development testing and linting tools:

pip install pytest flake8

Run the complete test suite:

python -m pytest tests/

Expected result:

34 tests passed
Code Quality

Flake8 is used to perform static Python code-quality checks.

Run:

python -m flake8 app tests

This provides an automated quality gate before changes are integrated into the main branch.

Infrastructure as Code

Terraform infrastructure is located under:

infra/envs/dev/

Terraform is used to represent infrastructure configuration as version-controlled code.

Initialize Terraform without configuring a remote backend:

terraform init -backend=false

Validate the Terraform configuration:

terraform validate

This allows the infrastructure configuration to be validated locally without provisioning paid cloud resources.

Local AWS Development

The project supports local AWS-oriented development using LocalStack.

LocalStack provides an AWS-compatible local environment that can be used to develop and test cloud-oriented workflows without requiring the application to connect to live AWS services.

This supports the project's local-first development approach.

Application
     |
     v
CloudOps API
     |
     v
AWS-oriented Infrastructure
     |
     v
LocalStack
     |
     v
Local Development Environment
CI/CD

The repository uses GitHub Actions for automated validation.

Workflow:

Git Push / Pull Request
          |
          v
    GitHub Actions
          |
    +-----+-----+
    |           |
    v           v
  Flake8      Pytest
    |           |
    +-----+-----+
          |
          v
   Terraform Init
          |
          v
   Terraform Validate

The CI pipeline performs:

Python dependency installation
Flake8 validation
Pytest execution
Terraform initialization
Terraform validation

Workflow file:

.github/workflows/ci.yml
Local-First Development

A key objective of the project is to make cloud-oriented engineering workflows available locally.

The project can be developed and validated without continuously running paid AWS infrastructure.

This approach is useful for:

API development
Automated testing
Terraform development
AWS-compatible experimentation
CI/CD validation
Infrastructure engineering practice
DevOps Engineering Workflow

The project demonstrates an integrated application and infrastructure workflow:

Source Code
     |
     v
FastAPI Application
     |
     +------------------+
     |                  |
     v                  v
   Pytest             Flake8
     |                  |
     +--------+---------+
              |
              v
        GitHub Actions
              |
              v
          Terraform
              |
              v
          LocalStack

This reflects a practical approach to combining software engineering, infrastructure as code, automated testing, and CI/CD.

Engineering Practices Demonstrated

CloudOps Portfolio API demonstrates practical experience with:

REST API development
FastAPI
Python
Automated testing
Test-driven validation
Static code analysis
Terraform
Infrastructure as Code
AWS-oriented infrastructure
Local cloud simulation
LocalStack
GitHub Actions
CI/CD automation
Reproducible local development
Cost-Conscious Architecture

The project is intentionally designed to support local development.

Terraform validation can be performed without provisioning AWS infrastructure, while LocalStack provides an AWS-compatible environment for local experimentation.

This allows cloud engineering workflows to be developed and tested while minimizing unnecessary cloud costs.

Getting Started

Clone the repository:

git clone https://github.com/franklinosuji2-afk/cloudops-portfolio-api.git
cd cloudops-portfolio-api

Install dependencies:

pip install -r requirements.txt

Install development tools:

pip install pytest flake8

Run linting:

python -m flake8 app tests

Run tests:

python -m pytest tests/

Validate Terraform:

cd infra/envs/dev
terraform init -backend=false
terraform validate
CI Validation

Every change targeting main can be validated through the GitHub Actions workflow.

The CI pipeline provides automated checks for:

Python code quality
Application tests
Terraform configuration

This helps ensure that application and infrastructure changes remain consistently validated.

Security and Configuration

The repository should not contain:

AWS access keys
Secret tokens
Passwords
Private credentials
Production secrets

Environment-specific credentials should be supplied through appropriate environment variables, secret-management systems, or secure CI/CD configuration.

Project Goals

CloudOps Portfolio API was built to demonstrate the intersection of:

Software Engineering
        +
Cloud Infrastructure
        +
Infrastructure as Code
        +
Automated Testing
        +
CI/CD
        +
Local Cloud Development

The result is a practical portfolio project demonstrating how application and infrastructure engineering workflows can be developed and validated together.

Author

Franklin Osuji

Cloud Infrastructure and DevOps Engineer

GitHub:
https://github.com/franklinosuji2-afk

Portfolio:
https://fc-dev.netlify.app/

Project Focus

Python | FastAPI | AWS | Terraform | LocalStack | Infrastructure as Code | CI/CD | Pytest | DevOps
