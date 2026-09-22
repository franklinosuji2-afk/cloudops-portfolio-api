# CloudOps Portfolio API

CloudOps Portfolio API is a Python API project demonstrating cloud-oriented application development, automated testing, infrastructure as code, and local cloud simulation.

Technology Stack
Python
FastAPI
Pytest
Flake8
Terraform
AWS infrastructure patterns
LocalStack for local AWS development
GitHub Actions
Project Structure
cloudops-portfolio-api/
|-- app/
|-- tests/
|-- infra/
|   `-- envs/
|       `-- dev/
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- requirements.txt
`-- README.md
API

The application provides CRUD operations for portfolio project resources.

The test suite covers:

Create project
Read project
List projects
Update project
Delete project
Request validation
Testing

Install dependencies:

pip install -r requirements.txt
pip install pytest flake8

Run linting:

python -m flake8 app tests

Run tests:

python -m pytest tests/

The project currently contains 34 automated tests.

Terraform

Terraform infrastructure is located under:

infra/envs/dev/

Initialize Terraform without a remote backend:

terraform init -backend=false

Validate the configuration:

terraform validate
Local AWS Development

LocalStack can be used for AWS-compatible local development and testing without creating paid AWS resources.

CI

The repository uses one GitHub Actions workflow:

.github/workflows/ci.yml

The CI pipeline performs:

Python dependency installation
Flake8 validation
Pytest execution
Terraform initialization
Terraform validation
Cost

The project is designed to support local development. Running the application and Terraform validation locally does not require paid AWS infrastructure.

Author

Franklin Osuji

Cloud Infrastructure and DevOps Engineer

GitHub: https://github.com/franklinosuji2-afk
Portfolio: https://fc-dev.netlify.app/
