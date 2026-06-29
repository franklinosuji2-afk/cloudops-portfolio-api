# ☁️ CloudOps Portfolio API

> **A production-style serverless REST API built on AWS using Infrastructure as Code.**

CloudOps Portfolio API is a fully serverless CRUD API designed to demonstrate real-world **Cloud Engineering**, **DevOps automation**, and **AWS infrastructure design**.

The platform manages a collection of portfolio projects through a scalable event-driven architecture powered by:

* Amazon Web Services Lambda
* Amazon Web Services API Gateway
* Amazon Web Services DynamoDB
* Terraform
* LocalStack

The entire stack can run locally using LocalStack, enabling realistic AWS development without incurring cloud costs.

---

# 🚀 Project Overview

Modern cloud-native APIs should be:

* scalable
* cost-efficient
* highly available
* infrastructure-as-code driven
* observable
* easy to automate

CloudOps Portfolio API demonstrates exactly that.

Rather than relying on traditional servers or container clusters, this project uses a **serverless architecture** where compute is triggered only when requests arrive.

That means:

✅ No always-on servers
✅ No load balancers
✅ No NAT gateways
✅ No VPC management
✅ Near-zero baseline cost

---

# 🎯 What This Project Demonstrates

This repository showcases practical experience in:

✅ Serverless architecture design
✅ Infrastructure as Code (IaC)
✅ AWS resource provisioning with Terraform
✅ CI/CD pipeline automation
✅ Monitoring & alerting
✅ REST API design
✅ Automated testing
✅ Cost-aware cloud architecture

---

# 🏗 Architecture

```text id="rch6i0"
Client
  │
  ▼
API Gateway (HTTP API)
  │
  ├── GET    /projects
  ├── POST   /projects
  ├── GET    /projects/{id}
  ├── PUT    /projects/{id}
  └── DELETE /projects/{id}
  │
  ▼
AWS Lambda Functions
  │
  ▼
DynamoDB
  │
  ▼
CloudWatch Logs & Monitoring
```

---

## Request Flow

1. Client sends HTTP request
2. API Gateway routes request
3. Lambda handler executes business logic
4. DynamoDB stores or retrieves data
5. CloudWatch captures logs and metrics

All compute is fully event-driven.

---

# ⚙️ Technology Stack

| Layer             | Technology                                                                   |
| ----------------- | ---------------------------------------------------------------------------- |
| IaC               | Terraform                                                                    |
| Compute           | Amazon Web Services Lambda (Python 3.12)                                     |
| API               | Amazon Web Services API Gateway v2                                           |
| Database          | Amazon Web Services DynamoDB                                                 |
| Monitoring        | CloudWatch                                                                   |
| Alerting          | SNS                                                                          |
| Local Development | LocalStack                                                                   |
| CI/CD             | [GitHub Actions](https://github.com/features/actions?utm_source=chatgpt.com) |
| Testing           | Pytest + Moto                                                                |

---

# ✨ Features

---

## RESTful CRUD API

Supports complete project lifecycle management.

Endpoints:

* Create project
* List projects
* Get project
* Update project
* Delete project

---

## Serverless Infrastructure

Infrastructure is fully provisioned with Terraform.

Benefits:

* reproducible environments
* version-controlled infrastructure
* easy rollback
* scalable provisioning

---

## Local AWS Simulation

Using LocalStack allows:

* local development
* faster iteration
* zero AWS cost during testing

---

## Monitoring & Alerting

Includes:

* structured application logs
* CloudWatch metrics
* error alarms
* SNS notifications

---

# 📁 Repository Structure

```bash id="xtd40x"
cloudops-portfolio-api/
│
├── .github/workflows/
│   ├── ci.yml
│   └── deploy.yml
│
├── docs/
│   ├── api-spec.md
│   ├── cost-notes.md
│   └── runbook.md
│
├── infra/
│   ├── modules/
│   │   ├── apigateway/
│   │   ├── dynamodb/
│   │   ├── iam/
│   │   ├── lambda/
│   │   └── monitoring/
│   │
│   └── envs/
│       ├── dev/
│       └── prod/
│
├── src/
│   ├── handlers/
│   └── utils/
│
├── tests/
│
└── README.md
```

---

# 🚀 API Endpoints

| Method | Endpoint         | Description    |
| ------ | ---------------- | -------------- |
| GET    | `/projects`      | List projects  |
| POST   | `/projects`      | Create project |
| GET    | `/projects/{id}` | Get project    |
| PUT    | `/projects/{id}` | Update project |
| DELETE | `/projects/{id}` | Delete project |

---

# 📦 Project Schema

```json
{
  "id": "uuid-auto-generated",
  "name": "string",
  "description": "string",
  "status": "active | archived | completed | paused",
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp"
}
```

---

# 🧪 Example Request

## Create Project

```json
POST /projects
{
  "name": "Platform Modernization",
  "description": "Migrate services to serverless",
  "status": "active"
}
```

Response:

```json
{
  "id": "92083e48-eb3f-4843-9081-207645e9532b",
  "name": "Platform Modernization",
  "status": "active"
}
```

---

# 🛠 Local Development

---

## Prerequisites

Install:

* Python 3.12+
* Terraform 1.6+
* Docker
* LocalStack

---

## Clone Repository

```bash id="f9z9z1"
git clone https://github.com/franklinosuji2-afk/cloudops-portfolio-api.git
cd cloudops-portfolio-api
```

---

## Install Dependencies

```bash id="1iv16m"
pip install -r requirements.txt
```

---

## Run Tests

```bash id="y6knzs"
pytest tests/
```

---

## Start LocalStack

```bash id="b2t05m"
localstack start -d
```

---

## Deploy Infrastructure

```bash id="0pfygq"
cd infra/envs/dev
terraform init
terraform apply
```

---

# 🔄 CI/CD Pipeline

Two workflows automate delivery.

---

## CI Pipeline (`ci.yml`)

Runs on push and pull requests.

Stages:

* Python dependency install
* Lint checks
* Unit tests
* Coverage checks
* Terraform formatting
* Terraform validation

---

## Deployment Pipeline (`deploy.yml`)

Runs on merge to main.

Stages:

* Build Lambda package
* Authenticate to AWS
* Terraform plan
* Terraform apply
* Publish API outputs

---

# 🏗 Terraform Infrastructure

Infrastructure is modularized into reusable components.

| Module       | Purpose               |
| ------------ | --------------------- |
| `dynamodb`   | Data persistence      |
| `iam`        | Least-privilege roles |
| `lambda`     | Compute layer         |
| `apigateway` | API routing           |
| `monitoring` | Metrics & alarms      |

---

# 📈 Monitoring & Observability

CloudWatch monitors:

* Lambda errors
* API failures
* execution latency
* request volume

Example log query:

```sql
fields @timestamp, level, message
| filter level = "ERROR"
| sort @timestamp desc
| limit 50
```

Alerts trigger when:

* Lambda errors exceed threshold
* API 5xx responses increase

---

# 🔐 Security

Security best practices include:

---

## Least Privilege IAM

Lambda only receives required DynamoDB permissions.

No wildcard permissions.

---

## Input Validation

Every handler validates request payloads before database writes.

---

## Secure Credentials

* No hardcoded AWS credentials
* LocalStack uses dummy credentials
* Production uses secure AWS authentication

---

## Cost-Aware Design

No VPC means avoiding:

* NAT Gateway charges
* subnet complexity
* extra network overhead

---

# 💰 Cost Analysis

Designed for AWS Free Tier usage.

| Service     | Free Tier         |
| ----------- | ----------------- |
| Lambda      | 1M requests/month |
| API Gateway | 1M calls/month    |
| DynamoDB    | 25 GB storage     |
| CloudWatch  | 5 GB logs         |

Expected portfolio traffic cost:

# **$0/month**

---

# 🧪 Testing

The project includes comprehensive automated testing.

Coverage includes:

* handler behavior
* validation logic
* CRUD operations
* edge cases
* error responses

Total tests:

### 34 unit tests

Uses [Moto](https://github.com/getmoto/moto?utm_source=chatgpt.com) to mock AWS services locally.

No AWS account required.

---

# 📚 Documentation

Additional docs included:

* API specification
* Cost breakdown
* Operations runbook

Located in:

```text id="pnl8hn"
docs/
```

---

# 🔮 Future Improvements

Planned enhancements:

* Amazon Web Services Cognito authentication
* Pagination support
* Secondary indexes
* X-Ray tracing
* Remote Terraform state
* Staging environment
* Blue/green deployments

---

# 💡 Why This Project Matters

Many portfolios show cloud deployment.

Few demonstrate **production-grade cloud operations**.

CloudOps Portfolio API showcases the engineering mindset needed to operate real AWS workloads:

* automation-first
* cost-aware architecture
* secure infrastructure
* observable systems
* scalable serverless design

This is the mindset expected from modern **Cloud Engineers**, **DevOps Engineers**, and **Platform Engineers**.

---

# 🤝 Contributing

Contributions, issues, and pull requests are welcome.

---

# 👨‍💻 Author

## Franklin Chinonso Osuji

Cloud & DevOps Engineer

AWS | Terraform | Serverless | CI/CD | DevOps | Platform Engineering

* [GitHub Profile](https://github.com/franklinosuji2-afk?utm_source=chatgpt.com)
* [LinkedIn Profile](https://www.linkedin.com/in/franklin-osuji-a96003321/?utm_source=chatgpt.com)

> Building scalable cloud systems through automation, observability, and infrastructure excellence.

---

# 📄 License

Licensed under the **MIT License**

