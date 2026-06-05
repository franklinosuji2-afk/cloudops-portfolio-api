# CloudOps Portfolio API

A production-style serverless REST API built on AWS, demonstrating real Cloud/DevOps engineering skills. Manages a collection of "projects" through a fully serverless architecture using Terraform, Lambda, API Gateway, and DynamoDB — runs locally for free using LocalStack.

---

## Live Demo (LocalStack)
POST   /projects          → Create a project
GET    /projects          → List all projects
GET    /projects/{id}     → Get a project by ID
PUT    /projects/{id}     → Update a project
DELETE /projects/{id}     → Delete a project

---

## Architecture
Client
│
▼
API Gateway v2 (HTTP API)
│
├── GET    /projects           → Lambda: list_projects
├── POST   /projects           → Lambda: create_project
├── GET    /projects/{id}      → Lambda: get_project
├── PUT    /projects/{id}      → Lambda: update_project
└── DELETE /projects/{id}      → Lambda: delete_project
│
▼
DynamoDB Table
(PAY_PER_REQUEST)
│
CloudWatch Logs & Alarms

All compute is event-driven. No always-on servers, no NAT Gateways, no load balancers, no VPC — zero baseline cost.

---

## Tech Stack

| Layer         | Technology                          |
|---------------|-------------------------------------|
| IaC           | Terraform 1.6+                      |
| Compute       | AWS Lambda (Python 3.12)            |
| API           | AWS API Gateway v2 (HTTP API)       |
| Database      | AWS DynamoDB (PAY_PER_REQUEST)      |
| Observability | AWS CloudWatch (Logs + Alarms)      |
| Alerts        | AWS SNS                             |
| Local Dev     | LocalStack (full AWS simulation)    |
| CI/CD         | GitHub Actions                      |
| Testing       | Pytest + moto (34 tests)            |

---

## Folder Structure
cloudops-portfolio-api/
├── .github/workflows/
│   ├── ci.yml              # Lint, test, terraform validate on every PR
│   └── deploy.yml          # Package + terraform apply on push to main
├── docs/
│   ├── api-spec.md         # Full endpoint documentation with examples
│   ├── cost-notes.md       # Free Tier breakdown and cleanup guide
│   └── runbook.md          # Incident response and operations guide
├── infra/
│   ├── modules/
│   │   ├── apigateway/     # HTTP API v2 + routes + Lambda permissions
│   │   ├── dynamodb/       # PAY_PER_REQUEST table
│   │   ├── iam/            # Least-privilege Lambda execution role
│   │   ├── lambda/         # 5 functions + CloudWatch log groups
│   │   └── monitoring/     # CloudWatch alarms + SNS topic
│   └── envs/
│       ├── dev/            # Dev environment (LocalStack / AWS)
│       └── prod/           # Prod environment
├── src/
│   ├── handlers/
│   │   ├── list_projects.py
│   │   ├── get_project.py
│   │   ├── create_project.py
│   │   ├── update_project.py
│   │   └── delete_project.py
│   └── utils/
│       ├── dynamodb.py
│       ├── logger.py
│       ├── response.py
│       └── validation.py
└── tests/                  # 34 pytest unit tests

---

## Local Development

### Prerequisites
- Python 3.12+
- Terraform 1.6+
- Docker Desktop
- LocalStack

### Setup

```bash
git clone https://github.com/franklinosuji2-afk/cloudops-portfolio-api.git
cd cloudops-portfolio-api

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

### Run Tests

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Start LocalStack

```powershell
$env:LOCALSTACK_AUTH_TOKEN = "your-token"
localstack start -d
```

### Build Lambda Package

```powershell
Remove-Item -Recurse -Force dist\package -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path dist\package | Out-Null
pip install boto3 --target dist\package --quiet
Copy-Item -Recurse src\handlers dist\package\handlers
Copy-Item -Recurse src\utils dist\package\utils
cd dist\package
Compress-Archive -Path * -DestinationPath ..\lambda.zip -Force
cd ..\..
```

### Deploy to LocalStack

```powershell
cd infra\envs\dev
terraform init
terraform apply -var="lambda_zip=..\..\..\dist\lambda.zip" -auto-approve
cd ..\..\..
```

---

## API Endpoints

| Method   | Path              | Description           | Status |
|----------|-------------------|-----------------------|--------|
| `GET`    | `/projects`       | List all projects     | 200    |
| `POST`   | `/projects`       | Create a project      | 201    |
| `GET`    | `/projects/{id}`  | Get a project by ID   | 200    |
| `PUT`    | `/projects/{id}`  | Update a project      | 200    |
| `DELETE` | `/projects/{id}`  | Delete a project      | 200    |

### Project Schema

```json
{
  "id":          "uuid-auto-generated",
  "name":        "string (required, max 100 chars)",
  "description": "string (optional, max 1000 chars)",
  "status":      "active | archived | completed | paused",
  "created_at":  "ISO 8601 UTC timestamp",
  "updated_at":  "ISO 8601 UTC timestamp"
}
```

### Example — Create a Project

```json
POST /projects
{
  "name": "Platform Modernisation",
  "description": "Migrate legacy services to serverless",
  "status": "active"
}
```

Response 201:
```json
{
  "id": "92083e48-eb3f-4843-9081-207645e9532b",
  "name": "Platform Modernisation",
  "description": "Migrate legacy services to serverless",
  "status": "active",
  "created_at": "2026-06-05T00:03:33.909859+00:00",
  "updated_at": "2026-06-05T00:03:33.909859+00:00"
}
```

Full API docs: [docs/api-spec.md](docs/api-spec.md)

---

## CI/CD Pipeline

**ci.yml** — runs on every push and pull request:
- Python 3.12 setup + dependency install
- flake8 lint check
- pytest with coverage (minimum 80%)
- terraform fmt check
- terraform validate

**deploy.yml** — runs on push to main:
- Build Lambda deployment zip
- Configure AWS credentials via OIDC
- terraform init + plan + apply
- Output deployed API URL to job summary

---

## Terraform Infrastructure

37 resources across 5 modules:

| Module     | Resources                                             |
|------------|-------------------------------------------------------|
| dynamodb   | DynamoDB table (PAY_PER_REQUEST)                      |
| iam        | Lambda execution role + least-privilege inline policy |
| lambda     | 5 Lambda functions + 5 CloudWatch log groups          |
| apigateway | HTTP API + 5 routes + 5 integrations + stage          |
| monitoring | 6 CloudWatch alarms + SNS topic                       |

---

## Monitoring & Observability

CloudWatch alarms fire on:
- Lambda error count > 1 per function per minute
- API Gateway 5xx errors > 1 per minute

Structured JSON logs queryable in CloudWatch Logs Insights:

```sql
fields @timestamp, level, message, project_id
| filter level = "ERROR"
| sort @timestamp desc
| limit 50
```

Full operations guide: [docs/runbook.md](docs/runbook.md)

---

## Security

- **Least-privilege IAM** — Lambda role grants only 6 DynamoDB actions on the specific table ARN
- **No hardcoded credentials** — LocalStack uses dummy keys; AWS uses OIDC
- **Input validation** — all handlers validate and sanitise input before touching DynamoDB
- **No VPC / NAT Gateway** — Lambda accesses DynamoDB via AWS service network directly

---

## Cost

Designed to run at $0 on AWS Free Tier:

| Service     | Free Tier                           |
|-------------|-------------------------------------|
| Lambda      | 1M requests + 400K GB-sec/month     |
| API Gateway | 1M calls/month (first 12 months)    |
| DynamoDB    | 25 GB + 25 WCU + 25 RCU (forever)  |
| CloudWatch  | 5 GB logs/month (first 12 months)   |

Expected cost at portfolio traffic: **$0.00/month**

Full breakdown: [docs/cost-notes.md](docs/cost-notes.md)

---

## Tests

| File                     | Tests |
|--------------------------|-------|
| test_list_projects.py    | 3     |
| test_get_project.py      | 3     |
| test_create_project.py   | 7     |
| test_update_project.py   | 7     |
| test_delete_project.py   | 4     |
| test_validation.py       | 10    |
| **Total**                | **34**|

All tests use [moto](https://github.com/getmoto/moto) to mock DynamoDB in-process. No AWS account needed.

---

## Future Improvements

- Add Cognito or API key authorisation to API Gateway
- Add GSI on `status` for filtered queries without full Scan
- Implement `LastEvaluatedKey` pagination on `GET /projects`
- Enable AWS X-Ray tracing on Lambda and API Gateway
- Add remote Terraform state with S3 + DynamoDB locking
- Add a staging environment between dev and prod


🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

👤 Author
Franklin Chinonso

GitHub: (https://github.com/franklinosuji2-afk/)
LinkedIn: (https://www.linkedin.com/in/franklin-osuji-a96003321/)
🙏 Acknowledgments
AWS Documentation
Terraform Registry
Docker Best Practices
DevOps Community
⭐ If you find this project helpful, please give it a star!