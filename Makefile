
# Target to deploy with ELK
python-format:
	isort --profile black --line-length 70 -w 70 src/ tests/
	black --exclude .+\.ipynb --line-length 70 --line-length 70 src/ tests/
	flake8 --max-line-length 70 --max-line-length=70 src/ tests/

deploy-astt-with-elk:
	docker-compose -f elk-logging/docker-compose.yaml up -d
	export LOGSTASH_IP=$$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' logstash); \
	python3 src/astt_gui/app.py


teardown-elk:
	docker-compose -f elk-logging/docker-compose.yaml down