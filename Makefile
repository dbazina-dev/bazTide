build:
	docker build -t backend .

clean:
	-docker kill backend
	-docker rm backend

run: build clean
	docker run -d --name backend -p 5000:5000 backend
	docker ps

log: run
	docker logs -f backend
