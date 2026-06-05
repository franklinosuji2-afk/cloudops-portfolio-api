variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "name_prefix" {
  type    = string
  default = "cloudops-portfolio-dev"
}

variable "alarm_email" {
  type    = string
  default = ""
}

variable "lambda_zip" {
  type    = string
  default = "../../../dist/lambda.zip"
}
