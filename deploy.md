### How to deploy the backend to an Ubuntu Machine

Follow this step-by-step guide to set the FastAPI backend on an Ubuntu instance.

#### 1. Update and Install Dependencies

Start by updating your package lists and installing the required packages:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib redis nginx make
```

#### 2. Install Python 3.11

Add the deadsnakes PPA and install Python 3.11:

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11
sudo apt-get install python3.11-venv
```

#### 3. Start PostgreSQL Service

Start the PostgreSQL service:

```bash
sudo systemctl start postgresql.service
```

#### 4. Generate SSH Key

Generate an SSH key for secure access to your server and Git:

```bash
ssh-keygen -t ed25519 -C "roytim1065@gmail.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```

Copy the output starting with `ssh-ed25519` and add it to your GitHub SSH keys.

#### 5. Clone Your GitHub Repository

Create a directory for your project and clone the repository:

```bash
mkdir srv
cd srv
git clone git@github.com:timiroy/Healthcare-backend.git
```

#### 6. Set Up Python Virtual Environment

Create and activate a Python virtual environment:

```bash
cd Healthcare-backend
python3.11 -m venv venv
source venv/bin/activate
```

#### 7. Install Python Dependencies

Install the required Python packages, including Gunicorn:

```bash
pip install -r requirements.txt
pip install gunicorn
```

#### 8. Configure Environment Variables

Create a `.env` file and add your configuration settings:

```bash
nano .env
```

Add the following content (replace with your actual values):

```env
POSTGRES_URL = postgresql+asyncpg://postgres@localhost/ai_health
ACCESS_TOKEN_SECRET = your_access_token_secret
REFRESH_TOKEN_SECRET = your_refresh_token_secret
RESET_PASSWORD_SECRET = your_reset_password_secret
SECRET_KEY = your_secret_key
JWT_ALGORITHM = HS256
REDIS_HOST = localhost
REDIS_PORT = 6379
AWS_ACCESS_KEY = your_aws_access_key
AWS_SECRET_KEY = your_aws_secret_key
BUCKET_NAME = your_bucket_name
AWS_REGION = your_aws_region
CLOUD_FRONT_URL = your_cloud_front_url
```

#### 9. Set Up PostgreSQL Configuration

Modify the PostgreSQL configuration to allow local connections without a password:

```bash
sudo nano /etc/postgresql/16/main/pg_hba.conf
```

Change the following lines to use `trust` for all local connections:

```conf
# "local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
```

Then restart the PostgreSQL service:

```bash
sudo systemctl restart postgresql
```

#### 10. Set Up the PostgreSQL Database

Log in to PostgreSQL and create the database:

```bash
sudo -u postgres psql
```

Inside the PostgreSQL prompt, run:

```sql
CREATE DATABASE ai_health;
```

Exit the PostgreSQL prompt:

```sql
\q
```

Update your `.env` file with the correct database URL:

```env
POSTGRES_URL = postgresql+asyncpg://localhost/ai_health
```

#### 11. Generate JWT Secret Key (Optional)

If you need to generate a new JWT secret key and have Node.js installed:

First, install Node.js if you haven't already:

```bash
sudo apt install nodejs npm
```

Then generate the key:

```bash
node -e "console.log(require('crypto').randomBytes(256).toString('base64'))"
```

#### 12. Set Up Nginx

Create a configuration file for your FastAPI backend:

```bash
sudo nano /etc/nginx/sites-available/backend.conf
```

Add the following configuration:

```nginx
server {
    listen 80;
    listen 443;
    server_name api-dev.ai_health.com;

    location / {
        proxy_pass http://localhost:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the configuration and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/backend.conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### 13. Create a Systemd Service File

Create a service file to manage your backend application with systemd:

```bash
sudo nano /etc/systemd/system/backend.service
```

Add the following content:

```ini
[Unit]
Description=ai_health app server
After=network.target

[Service]
User=ubuntu
Group=sudo
WorkingDirectory=/home/ubuntu/srv/Healthcare-backend
Environment="PATH=/home/ubuntu/srv/Healthcare-backend/venv/bin"
EnvironmentFile=/home/ubuntu/srv/Healthcare-backend/.env
ExecStart=/home/ubuntu/srv/Healthcare-backend/venv/bin/gunicorn -w 2 -k uvicorn.workers.UvicornWorker ai_health.root.app:app --bind 0.0.0.0:9000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 14. Enable and Start the Service

Enable and start the backend service:

```bash
sudo systemctl enable backend.service
sudo systemctl start backend.service
```

You can check the status of the service to ensure it is running:

```bash
sudo systemctl status backend.service
```

#### 15. Configure Firewall (Optional)

Ensure your firewall allows traffic on the necessary ports:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 5432/tcp
sudo ufw allow 6379/tcp
sudo ufw enable
```

#### 16. Checking Logs

If something goes wrong, check the logs for debugging:

```bash
sudo journalctl -u backend.service
sudo tail -f /var/log/nginx/error.log
```