# Outputs
output "ecr_repository_url" {
  value       = aws_ecr_repository.main.repository_url
  description = "The URL of the ECR repository"
}

output "alb_dns_name" {
  value       = aws_lb.main.dns_name
  description = "The DNS name of the load balancer"
}

output "ecs_cluster_name" {
  value       = aws_ecs_cluster.main.name
  description = "The name of the ECS cluster"
}

output "ecs_service_name" {
  value       = aws_ecs_service.main.name
  description = "The name of the ECS service"
}