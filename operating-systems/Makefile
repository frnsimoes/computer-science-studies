IMAGE_NAME = linux-env
CONTAINER_NAME = linux-dev

build-linux:
	docker build -t $(IMAGE_NAME) .

run-linux: check-container

check-container:
	@if [ $$(docker ps -a -q -f name=$(CONTAINER_NAME)) ]; then \
		echo "Container $(CONTAINER_NAME) already exists"; \
		make start-attach-container; \
	else \
		make run-new-container; \
	fi

start-attach-container:
	@if [ $$(docker ps -q -f name=$(CONTAINER_NAME)) ]; then \
		echo "Attaching to running container $(CONTAINER_NAME)"; \
		docker attach $(CONTAINER_NAME); \
	else \
		echo "Starting and attaching to container $(CONTAINER_NAME)"; \
		docker start $(CONTAINER_NAME); \
		docker attach $(CONTAINER_NAME); \
	fi

run-new-container:
	docker run -it --name $(CONTAINER_NAME) -v $(pwd):/ $(IMAGE_NAME)
