variable "table_name"  { type = string }
variable "environment" { type = string }
variable "tags" {
  type    = map(string)
  default = {}
}

resource "aws_dynamodb_table" "this" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = merge(var.tags, { Environment = var.environment })
}

output "table_name" { value = aws_dynamodb_table.this.name }
output "table_arn"  { value = aws_dynamodb_table.this.arn }
