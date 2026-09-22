# CloudOps Portfolio API

A serverless AWS CRUD API demonstrating Lambda, API Gateway, DynamoDB, Terraform, LocalStack, automated testing, and DevOps practices.

## Quality checks

Install the project and development dependencies:

```bash
make install
```

Run the full local validation suite:

```bash
make check
```

Individual checks are also available:

```bash
make test
make coverage
make lint
make format-check
make terraform-fmt-check
make terraform-validate
```

The CI workflow runs Python linting, formatting checks, tests with a 70% minimum coverage threshold, Terraform formatting, and backend-free Terraform validation. These checks do not deploy infrastructure or require AWS credentials.

## Production considerations

Before using this project for a real service, add authentication and authorization, request throttling, structured logging, alarms, audit logging, encryption-key management, dependency update automation, and a reviewed deployment and rollback process.
