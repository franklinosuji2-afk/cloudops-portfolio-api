variable "function_name" { type = string }
variable "handler"       { type = string }
variable "role_arn"      { type = string }
variable "zip_path"      { type = string }
variable "table_name"    { type = string }
variable "environment"   { type = string }
variable "log_level" {
  type    = string
  default = "INFO"
}
variable "tags" {
  type    = map(string)
  default = {}
}

resource "aws_cloudwatch_log_group" "this" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = 7
  tags              = merge(var.tags, { Environment = var.environment })
}

resource "aws_lambda_function" "this" {
  function_name    = var.function_name
  role             = var.role_arn
  handler          = var.handler
  runtime          = "python3.12"
  filename         = var.zip_path
  source_code_hash = filebase64sha256(var.zip_path)
  timeout          = 10
  memory_size      = 256

  environment {
    variables = {
      DYNAMODB_TABLE = var.table_name
      LOG_LEVEL      = var.log_level
    }
  }

  depends_on = [aws_cloudwatch_log_group.this]
  tags       = merge(var.tags, { Environment = var.environment })
}

output "function_name" { value = aws_lambda_function.this.function_name }
output "function_arn"  { value = aws_lambda_function.this.arn }
output "invoke_arn"    { value = aws_lambda_function.this.invoke_arn }
