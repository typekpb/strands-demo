terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.23"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.6.2"
    }

  }
  required_version = ">= 1.12"
}

variable "aws_region" {
  default = "us-east-1"
}

provider "aws" {
  region = var.aws_region
}

provider "docker" {
  host = "unix://${pathexpand("~/.colima/default/docker.sock")}"

  registry_auth {
    address  = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com"
    username = "AWS"
    password = data.aws_ecr_authorization_token.token.password
  }
}

resource "aws_ecr_repository" "lambda" {
  name                 = "strands_agents_demo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

locals {
  py_files  = [for f in fileset(path.module, "*.py")  : filesha1(f)]
  tf_files  = [for f in fileset(path.module, "*.tf")  : filesha1(f)]
  docker_files  = [for f in fileset(path.module, "Dockerfile")  : filesha1(f)]
  source_hash = sha1(join("", concat(local.py_files, local.tf_files, local.docker_files)))
}

resource "docker_image" "strands_demo" {
  name = "${aws_ecr_repository.lambda.repository_url}:${local.source_hash}"

  build {
    context = "${path.module}"
    platform = "linux/amd64" # needed for amazon lambda publishing
  }

  triggers = {
    dir_sha1 = sha1(join("", [for f in fileset(path.module, "*.py") : filesha1(f)]))
  }
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "strands_agents_demo"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_bedrock_policy" {
  name        = "lambda_bedrock_policy"
  description = "Allows Lambda to call Bedrock and write logs"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_bedrock_attach" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_bedrock_policy.arn
}

resource "docker_registry_image" "lambda_image" {
  depends_on = [docker_image.strands_demo]

  name = docker_image.strands_demo.name

  triggers = {
    image_id = docker_image.strands_demo.id
  }
}

resource "aws_lambda_function" "lambda" {
  function_name = "strands-agent-demo-01"
  package_type  = "Image"
  image_uri     = docker_registry_image.lambda_image.name
  role          = aws_iam_role.lambda_exec_role.arn
  timeout = 30
}

data "aws_caller_identity" "current" {}

data "aws_ecr_authorization_token" "token" {}
