variable "api_name"    { type = string }
variable "environment" { type = string }
variable "integrations" {
  type = map(object({
    invoke_arn    = string
    function_name = string
  }))
}
variable "tags" {
  type    = map(string)
  default = {}
}

resource "aws_apigatewayv2_api" "this" {
  name          = var.api_name
  protocol_type = "HTTP"
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers = ["Content-Type", "Authorization"]
  }
  tags = merge(var.tags, { Environment = var.environment })
}

resource "aws_apigatewayv2_integration" "this" {
  for_each               = var.integrations
  api_id                 = aws_apigatewayv2_api.this.id
  integration_type       = "AWS_PROXY"
  integration_uri        = each.value.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "this" {
  for_each  = var.integrations
  api_id    = aws_apigatewayv2_api.this.id
  route_key = each.key
  target    = "integrations/${aws_apigatewayv2_integration.this[each.key].id}"
}

resource "aws_apigatewayv2_stage" "this" {
  api_id      = aws_apigatewayv2_api.this.id
  name        = "$default"
  auto_deploy = true

  default_route_settings {
    throttling_burst_limit = 100
    throttling_rate_limit  = 50
  }

  tags = merge(var.tags, { Environment = var.environment })
}

resource "aws_lambda_permission" "apigw" {
  for_each      = var.integrations
  statement_id  = "AllowAPIGW-${replace(replace(replace(replace(each.key, " ", "-"), "/", "-"), "{", ""), "}", "")}"
  action        = "lambda:InvokeFunction"
  function_name = each.value.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.this.execution_arn}/*/*"
}

output "api_endpoint" { value = aws_apigatewayv2_api.this.api_endpoint }
output "api_id"       { value = aws_apigatewayv2_api.this.id }
