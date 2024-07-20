sudo nano /etc/systemd/system/rq_worker.service 

journalctl --unit=my.service -n 100 --no-pager

systemctl daemon-reload

sudo nano /etc/systemd/system/my.service

sudo certbot --nginx -d example.com -d www.example.com

sudo systemctl status certbot.timer

alembic revision --autogenerate -m "Added account table"