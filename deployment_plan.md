# Deployment Plan: astrology-service Docker Image

This plan outlines the steps to build and push the `astrology-service` Docker image to the Azure Container Registry.

## 1. Verify Local Docker Image

- [ ] Check if the `cosmotalksacr.azurecr.io/astrology-service:latest` Docker image exists locally using the `docker images` command.

## 2. Log in to Azure Container Registry

- [ ] Ensure authentication with Azure Container Registry by running `az acr login --name cosmotalksacr`.

## 3. Push Docker Image

- [ ] Push the Docker image to the registry with `docker push cosmotalksacr.azurecr.io/astrology-service:latest`.

## 4. Verify Image in Registry

- [ ] List the repositories in the ACR to confirm the image was pushed successfully, using `az acr repository list --name cosmotalksacr -o table`.