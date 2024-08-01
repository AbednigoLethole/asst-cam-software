Deploy-astt-cam-software:
	sh startVirtualCANInterface.sh
	sleep 2
	docker compose up -d

Teardown-astt-cam-software:
	docker compose down

