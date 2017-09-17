terraform {
  backend "s3" {
    bucket         = "terraform-test-nbari-com"
    key            = "infrastructure/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = "true"
    dynamodb_table = "terraform_locks"
  }
}
