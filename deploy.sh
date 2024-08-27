#!/bin/bash
set -e

# Load environ variables
source .env

# Update the ECS service
aws ecs update-service --cluster $ECS_CLUSTER_NAME --service $ECS_SERVICE_NAME --force-new-deployment

echo "Deployment initiated"
