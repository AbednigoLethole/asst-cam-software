Deploy-astt-cam-software:
	sh startVirtualCANInterface.sh
	sleep 2
	docker network create astt-network
	docker compose up -d

Teardown-astt-cam-software:
	docker network rm astt-network
	docker compose down

