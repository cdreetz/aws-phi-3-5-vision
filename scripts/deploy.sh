#!/bin/bash
set -e

# Load environment variables
if [ -f .env ]; then
    source .env
else
    echo ".env file not found"
    exit 1
fi

# Check if required variables are set
if [ -z "$AWS_REGION" ] || [ -z "$ECS_CLUSTER_NAME" ] || [ -z "$ECS_SERVICE_NAME" ]; then
    echo "Required environment variables are not set. Please check your .env file."
    exit 1
fi

# Update the ECS service to force a new deployment
aws ecs update-service --cluster $ECS_CLUSTER_NAME --service $ECS_SERVICE_NAME --force-new-deployment --region $AWS_REGION

echo "Deployment initiated for service $ECS_SERVICE_NAME in cluster $ECS_CLUSTER_NAME"

# Wait for the service to stabilize
echo "Waiting for service to stabilize..."
aws ecs wait services-stable --cluster $ECS_CLUSTER_NAME --services $ECS_SERVICE_NAME --region $AWS_REGION

echo "Deployment completed successfully"