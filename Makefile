run:
	POSTGRES_HOSTNAME=localhost POSTGRES_PORT=5430 POSTGRES_USER=admin POSTGRES_PASSWORD=123 POSTGRES_DB=rinha uvicorn main:app --reload --host 0.0.0.0 --port 8080
