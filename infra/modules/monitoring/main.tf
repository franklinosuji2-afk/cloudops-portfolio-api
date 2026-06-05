variable "name_prefix"    { type = string }
variable "function_names" { type = list(string) }
variable "api_id"         { type = string }
variable "environment"    { type = string }
variable "alarm_email" {
  type    = string
  default = ""
}
variable "tags" {
  type    = map(string)
  default = {}
}

resource "aws_sns_topic" "alerts" {
  name = "${var.name_prefix}-alerts"
  tags = merge(var.tags, { Environment = var.environment })
}

resource "aws_sns_topic_subscription" "email" {
  count     = var.alarm_email == "" ? 0 : 1
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alarm_email
}

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  for_each            = toset(var.function_names)
  alarm_name          = "${each.value}-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Lambda ${each.value} reported errors"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  dimensions          = { FunctionName = each.value }
  treat_missing_data  = "notBreaching"
  tags                = merge(var.tags, { Environment = var.environment })
}

resource "aws_cloudwatch_metric_alarm" "api_5xx" {
  alarm_name          = "${var.name_prefix}-api-5xx"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "5xx"
  namespace           = "AWS/ApiGateway"
  period              = 60
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "API Gateway 5xx responses"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  dimensions          = { ApiId = var.api_id }
  treat_missing_data  = "notBreaching"
  tags                = merge(var.tags, { Environment = var.environment })
}

output "sns_topic_arn" { value = aws_sns_topic.alerts.arn }
