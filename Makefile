
# Target to deploy with ELK
deploy-astt-with-elk:
	docker-compose -f elk-logging/docker-compose.yaml up -d
	export LOGSTASH_IP=$$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' logstash); \
	python3 src/astt_gui/app.py



teardown-elk:
	docker-compose -f elk-logging/docker-compose.yaml down