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

ssh_server:
	ssh -i "deployment/ai_health_dev.pem" ubuntu@ec2-35-178-213-221.eu-west-2.compute.amazonaws.com


update_app:
	git pull origin dev	
	pip install -r requirements.txt 
	alembic upgrade head
	sudo systemctl restart backend_app.service;
