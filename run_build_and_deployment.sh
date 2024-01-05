#! /bin/bash
DOCKER_HUB_USERNAME=$1
PAPERSPACE_API_KEY=$2
PAPERSPACE_PROJECT_ID=$3

if [ "$#" -ne 3 ]; then
    echo "Usage: ./run_build_and_deployment.sh DOCKER_HUB_USERNAME PAPERSPACE_API_KEY PAPERSPACE_PROJECT_ID"
    exit 1
fi

# build docker image
docker build -t ${DOCKER_HUB_USERNAME}/nlp-tunnel-vision:latest .

# push docker image to docker hub
docker login
docker tag ${DOCKER_HUB_USERNAME}/nlp-tunnel-vision:latest ${DOCKER_HUB_USERNAME}/nlp-tunnel-vision:latest
docker push ${DOCKER_HUB_USERNAME}/nlp-tunnel-vision:latest

# update deployment-paperspace.yaml with docker image
sed -i "s/image: .*/image: ${DOCKER_HUB_USERNAME}\/nlp-tunnel-vision:latest/g" deployment-paperspace.yaml

# deploy docker image to Paperspace Gradient
gradient deployments create \
    --name "nlp-tunnel-vision" \
    --projectId ${PAPERSPACE_PROJECT_ID} \
    --spec deployment-paperspace.yaml \
    --apiKey ${PAPERSPACE_API_KEY} 




