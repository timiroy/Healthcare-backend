start:
	uvicorn ai_health.root.app:app --reload --port 8010

start_rq:
	rq worker --with-scheduler
	
install_requirements:
	pip install -r requirements.txt

freeze_requirements:
	pip freeze > requirements.txt

activate:
	source venv/bin/activate

check_format:
	ruff check ./ai_health --ignore=E731,E712

check_db:
	alembic check

migrate:
	alembic upgrade head

make_migrations:
	python make_db_migrations.py

ssh:
	ssh -i "deployment/ai_health.pem" ubuntu@ec2-13-48-48-198.eu-north-1.compute.amazonaws.com


update_app:
	git pull origin main	
	pip install -r requirements.txt 
	alembic upgrade head
	sudo systemctl restart backend.service;
	sudo systemctl restart rq.service;