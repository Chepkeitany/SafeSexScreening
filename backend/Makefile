IMAGE_NAME := ss2backend
PORT := 80
TAG := latest

all: clean build run test

clean:
	-docker stop $(IMAGE_NAME)
	-docker rm $(IMAGE_NAME)
	-docker rmi -f $(IMAGE_NAME):$(TAG)
	rm -rf */__pycache__

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

run:
	docker run --name $(IMAGE_NAME) -d -p $(PORT):80 $(IMAGE_NAME):$(TAG)

test:
	docker exec $(IMAGE_NAME) python -m unittest discover -s tests
