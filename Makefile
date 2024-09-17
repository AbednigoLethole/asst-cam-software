deploy-astt-cam-software:
	sh startVirtualCANInterface.sh
	sleep 2
	docker compose up -d

teardown-astt-cam-software:
	docker compose down

python-format:
	isort --profile black --line-length 99 src/ tests/
	black --exclude .+\.ipynb --line-length 99 src/ tests/
	flake8 --max-line-length 99 src/ tests/
