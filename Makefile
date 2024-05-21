deploy-astt-with-elk:
	docker-compose -f elk-logging/docker-compose.yaml up -d
	export LOGSTASH_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' logstash) && \
	echo $(LOGSTASH_IP)



teardown-elk:
	docker-compose -f elk-logging/docker-compose.yaml down