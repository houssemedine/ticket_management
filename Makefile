.PHONY: run test cov lint fmt docker-build docker-run

PY=python
UVICORN=uvicorn
APP=app.main:app

run:
	$(UVICORN) $(APP) --reload

test:
	pytest -q

cov:
	pytest --cov=app --cov-report=term-missing

lint:
	ruff check .

fmt:
	ruff check . --fix

docker-build:
	docker build -t ticket-managements:latest .

docker-run:
	docker run --rm -p 8010:8010 ticket-managements:latest
