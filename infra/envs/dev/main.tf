locals {
  table_name = "${var.name_prefix}-projects"

  functions = {
    list = {
      name      = "${var.name_prefix}-list-projects"
      handler   = "handlers.list_projects.handler"
      route_key = "GET /projects"
    }
    get = {
      name      = "${var.name_prefix}-get-project"
      handler   = "handlers.get_project.handler"
      route_key = "GET /projects/{id}"
    }
    create = {
      name      = "${var.name_prefix}-create-project"
      handler   = "handlers.create_project.handler"
      route_key = "POST /projects"
    }
    update = {
      name      = "${var.name_prefix}-update-project"
      handler   = "handlers.update_project.handler"
      route_key = "PUT /projects/{id}"
    }
    delete = {
      name      = "${var.name_prefix}-delete-project"
      handler   = "handlers.delete_project.handler"
      route_key = "DELETE /projects/{id}"
    }
  }
}

module "dynamodb" {
  source      = "../../modules/dynamodb"
  table_name  = local.table_name
  environment = var.environment
}

module "iam" {
  source       = "../../modules/iam"
  name_prefix  = var.name_prefix
  dynamodb_arn = module.dynamodb.table_arn
  environment  = var.environment
}

module "lambda" {
  for_each      = local.functions
  source        = "../../modules/lambda"
  function_name = each.value.name
  handler       = each.value.handler
  role_arn      = module.iam.role_arn
  zip_path      = var.lambda_zip
  table_name    = module.dynamodb.table_name
  environment   = var.environment
}

module "apigateway" {
  source      = "../../modules/apigateway"
  api_name    = "${var.name_prefix}-api"
  environment = var.environment
  integrations = {
    for k, fn in local.functions : fn.route_key => {
      invoke_arn    = module.lambda[k].invoke_arn
      function_name = module.lambda[k].function_name
    }
  }
}

module "monitoring" {
  source         = "../../modules/monitoring"
  name_prefix    = var.name_prefix
  environment    = var.environment
  alarm_email    = var.alarm_email
  api_id         = module.apigateway.api_id
  function_names = [for k, _ in local.functions : module.lambda[k].function_name]
}

output "api_endpoint" { value = module.apigateway.api_endpoint }
output "table_name" { value = module.dynamodb.table_name }
output "sns_topic_arn" { value = module.monitoring.sns_topic_arn }
