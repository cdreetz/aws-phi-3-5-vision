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
if [ -z "$AWS_ACCOUNT_ID" ] || [ -z "$AWS_REGION" ] || [ -z "$ECR_REPOSITORY_NAME" ]; then
    echo "Required environment variables are not set. Please check your .env file."
    exit 1
fi

# Login to Amazon ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build the Docker image
docker build -t $ECR_REPOSITORY_NAME:latest .

# Tag the image
docker tag $ECR_REPOSITORY_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:latest

# Push the image to ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:latest

echo "Image built and pushed successfully to $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:latest"