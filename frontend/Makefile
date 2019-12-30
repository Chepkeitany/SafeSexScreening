IMAGE_NAME := ss2frontend
PORT := 5000
TAG := latest

all: clean build run

clean:
	-docker stop $(IMAGE_NAME)
	-docker rm $(IMAGE_NAME)
	-docker rmi -f $(IMAGE_NAME):$(TAG)
	rm -rf */__pycache__

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

run:
	docker run --name $(IMAGE_NAME) -d -p $(PORT):80 $(IMAGE_NAME):$(TAG)
