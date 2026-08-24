variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "app_name" {
  type    = string
  default = "receipt-service"
}

# Bump this to deploy a new version.
variable "image_tag" {
  type    = string
  default = "v1"
}

