resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = "${file("assume-role-policy.json")}"
}

resource "aws_lambda_function" "test" {
  filename         = "app.zip"
  function_name    = "test"
  handler          = "test.handler"
  role             = "${aws_iam_role.iam_for_lambda.arn}"
  runtime          = "python2.7"
  source_code_hash = "${base64sha256(file("app.zip"))}"
}

resource "aws_api_gateway_rest_api" "test" {
  name        = "test"
  description = "test Rest Api"
  depends_on  = ["aws_lambda_function.test"]
}

resource "aws_api_gateway_resource" "test" {
  rest_api_id = "${aws_api_gateway_rest_api.test.id}"
  parent_id   = "${aws_api_gateway_rest_api.test.root_resource_id}"
  path_part   = "test"
}

resource "aws_api_gateway_method" "test" {
  rest_api_id   = "${aws_api_gateway_rest_api.test.id}"
  resource_id   = "${aws_api_gateway_resource.test.id}"
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "test" {
  http_method             = "${aws_api_gateway_method.test.http_method}"
  integration_http_method = "POST"
  resource_id             = "${aws_api_gateway_resource.test.id}"
  rest_api_id             = "${aws_api_gateway_rest_api.test.id}"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${data.terraform_remote_state.vpc.config.region}:lambda:path/2015-03-31/functions/arn:aws:lambda:${data.terraform_remote_state.vpc.config.region}:${data.aws_caller_identity.current.account_id}:function:${aws_lambda_function.test.function_name}/invocations"
}

resource "aws_lambda_permission" "test" {
  function_name = "${aws_lambda_function.test.function_name}"
  statement_id  = "AllowExecutionFromApiGateway"
  action        = "lambda:InvokeFunction"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${data.terraform_remote_state.vpc.config.region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.test.id}/*/${aws_api_gateway_method.test.http_method}/test"
}

resource "aws_api_gateway_deployment" "test" {
  depends_on = [
    "aws_api_gateway_method.test",
    "aws_api_gateway_integration.test",
  ]

  rest_api_id = "${aws_api_gateway_rest_api.test.id}"
  stage_name  = "api"
}

output "api_url" {
  value = "https://${aws_api_gateway_deployment.test.rest_api_id}.execute-api.${data.terraform_remote_state.vpc.config.region}.amazonaws.com/${aws_api_gateway_deployment.test.stage_name}"
}
