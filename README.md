# receipt_service

How to the FASTapi Application: `uvicorn main:app --reload`

How to run the container:

- build: `docker build -t receipt_service .`
- run: `docker run --rm -p 8000:8000 receipt_service`

# Terraform Setup

## Only once

1. Create a default VPC (once per account/region, free)

```bash
aws ec2 create-default-vpc --region eu-central-1
```

2. First apply ECR repo only. The task definition references an image that doesn't exist yet, so build the registry first. Execute this within the `terraform` directory.

```bash
terraform apply -target=aws_ecr_repository.app
```

## For every new version

1. Build docker image

```bash
docker build --platform linux/amd64 --provenance=false -t 117891393357.dkr.ecr.eu-central-1.amazonaws.com/receipt-service:v1.1 .
```

2. Push docker image

```bash
docker push 117891393357.dkr.ecr.eu-central-1.amazonaws.com/receipt-service:v1.1
```

3. Run terraform

```bash
terraform apply
```

4. Retrieve the IP-Address (DNS needed to get a static IP-Address)

```bash
CLUSTER=receipt-service; REGION=eu-central-1; TASK=$(aws ecs list-tasks --cluster $CLUSTER --region $REGION --query 'taskArns[0]' --output text); ENI=$(aws ecs describe-tasks --cluster $CLUSTER --tasks $TASK --region $REGION --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value' --output text); aws ec2 describe-network-interfaces --network-interface-ids $ENI --region $REGION --query 'NetworkInterfaces[0].Association.PublicIp' --output text
```

## To see logs

Logs are in CloudWatch under /ecs/receipt-service:

```bash
aws logs tail /ecs/receipt-service --region eu-central-1 --follow
```
