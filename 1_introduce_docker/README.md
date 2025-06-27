### 1. Docker Basics (`1_introduce_docker/`)
Introduction to containerization for ML models:
- Basic Docker setup for ML applications
- Best practices for containerizing ML models
- Foundation for more complex deployment scenarios

```bash
# simple nginx with static
docker run -it --rm -p 80:80 nginx:latest
docker run -it --rm -p 80:80 -v ./nginx_container_1/index.html:/usr/share/nginx/html/index.html nginx:latest

# nginx as load balancer
docker network create nginx_network
docker run -d --name nginx_static_1 --network nginx_network -v ./nginx_container_1/index.html:/usr/share/nginx/html/index.html nginx:latest
docker run -d --name nginx_static_2 --network nginx_network -v ./nginx_container_2/index.html:/usr/share/nginx/html/index.html nginx:latest
docker run -d --name nginx_balancer --network nginx_network -p 80:80 -v ./nginx_balancer/nginx.conf:/etc/nginx/nginx.conf nginx:latest

# or docker compose
docker compose up -d
```