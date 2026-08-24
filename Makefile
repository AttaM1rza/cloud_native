REGION ?= eu-central-1
APP    ?= receipt-service
TAG    ?= v1.1
IMAGE   = $(shell terraform -chdir=terraform output -raw ecr_repository_url):$(TAG)

.PHONY: help install run test docker-build docker-run login push deploy ip logs

install: ## Create the venv and install dependencies
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

run: ## Run the API locally on :8000
	.venv/bin/uvicorn main:app --reload

deploy:
	terraform -chdir=terraform apply -target=aws_ecr_repository.app
	docker build --platform linux/amd64 --provenance=false -t 117891393357.dkr.ecr.eu-central-1.amazonaws.com/receipt-service:v1.1 .
	docker push 117891393357.dkr.ecr.eu-central-1.amazonaws.com/receipt-service:v1.1

ip: # D	EPRICATED after using DNS
	@TASK=$$(aws ecs list-tasks --cluster $(APP) --region $(REGION) --query 'taskArns[0]' --output text); \
	ENI=$$(aws ecs describe-tasks --cluster $(APP) --tasks $$TASK --region $(REGION) --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value' --output text); \
	aws ec2 describe-network-interfaces --network-interface-ids $$ENI --region $(REGION) --query 'NetworkInterfaces[0].Association.PublicIp' --output text