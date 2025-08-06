# BFAChallenge
BFAChallenge dockers
To build this Docker container, clone the repository and run the following command in the root directory:

DOCKER_BUILDKIT=1 sudo docker build -t nimg:v0.8.6 .

The Docker runs the code from scripts/entrypoint.sh.


To run this Docker:

input_dir=".../input_data"
output_dir=".../output_data"

mkdir -p $output_dir

DOCKER_NOOP_VOLUME="beyondfa_baseline-volume"
sudo docker volume create "$DOCKER_NOOP_VOLUME" > /dev/null
sudo docker run \
    -it \
    --platform linux/amd64 \
    --network none \
    --gpus all \
    --rm \
    --volume $input_dir:/input:ro \
    --volume $output_dir:/output \
    --volume "$DOCKER_NOOP_VOLUME":/tmp \
    nimg:v0.8.6
sudo docker volume rm "$DOCKER_NOOP_VOLUME" > /dev/null
