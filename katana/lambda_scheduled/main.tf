# terraform configuration for a lambda function that uses invokust to run scheduled

provider "aws" {
  region = "eu-west-1"
}

resource "aws_iam_role" "lambda_basic_execution2" {
  name               = "lambda_basic_execution2"
  path               = "/service-role/"
  assume_role_policy = "${data.aws_iam_policy_document.lambda_basic_execution2_assume_role.json}"
}

data "aws_iam_policy_document" "lambda_basic_execution2_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "lambda_basic_execution2" {
  statement {
    effect  = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "lambda_basic_execution2" {
  name        = "lambda_basic_execution2"
  description = "Basic execution policy for a Lambda function"
  policy      =  "${data.aws_iam_policy_document.lambda_basic_execution2.json}"
}

resource "aws_iam_policy_attachment" "lambda_basic_execution2" {
  name       = "lambda_basic_execution2"
  roles      = ["${aws_iam_role.lambda_basic_execution2.name}"]
  policy_arn = "${aws_iam_policy.lambda_basic_execution2.arn}"
}

data "archive_file" "lambda_scheduled_code" {
  type = "zip"
  source_dir = "${path.module}/lambda_scheduled/"
  output_path = "${path.module}/.terraform/archive_files/lambda_scheduled.zip"
}

resource "aws_lambda_function" "lambda_scheduled" {
  filename = "${data.archive_file.lambda_scheduled_code.output_path}"
  source_code_hash = "${base64sha256(file("${data.archive_file.lambda_scheduled_code.output_path}"))}"
  function_name = "lambda_scheduled"
  role          = "${aws_iam_role.lambda_basic_execution2.arn}"
  handler       = "lambda_scheduled.lambda_handler"
  runtime       = "python3.6"

  timeout       = 300
  description   = "A function that pings sharepoint to generate a ping"
  environment {
    variables = {
      expected="WopiDocWACContainer"
      site="https://sumologictest-my.sharepoint.com/:w:/g/personal/collection_sumologictest_onmicrosoft_com/Eca9n_c_44tNj8PqwH3XTaQBrA7kABYAdfHtY-f4LnGCBA?e=WyKHzE"
    }
  }
}

resource "aws_cloudwatch_event_rule" "every_five_minutes" {
      name = "every-five-minutes"
      description = "Fires every five minutes"
      schedule_expression = "rate(1 minute)"
  }

resource "aws_cloudwatch_event_target" "lambda_scheduled_every_five_minutes" {
    rule = "${aws_cloudwatch_event_rule.every_five_minutes.name}"
    target_id = "lambda_scheduled"
    arn = "${aws_lambda_function.lambda_scheduled.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda_scheduled" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.lambda_scheduled.function_name}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.every_five_minutes.arn}"
}
