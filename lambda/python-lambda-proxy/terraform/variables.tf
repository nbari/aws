data "terraform_remote_state" "vpc" {
  backend = "s3"

  config {
    bucket = "terraform-test-nbari-com"
    key    = "vpc/terraform.tfstate"
    region = "eu-central-1"
  }
}

data "aws_caller_identity" "current" {}
