# Variables
variable "aws_region" {
  description = "The AWS region to create resources in"
  default     = "us-west-2"
}

variable "app_name" {
  description = "Name of the application"
  default     = "phi-3-5-vision"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for the public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "ecs_task_cpu" {
  description = "CPU units for the ECS task"
  default     = "4096"
}

variable "ecs_task_memory" {
  description = "Memory for the ECS task"
  default     = "30720"
}

variable "container_port" {
  description = "Port exposed by the docker image"
  default     = 8000
}

variable "app_image" {
  description = "The image tag for the application"
  default     = "latest"
}