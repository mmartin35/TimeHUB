[TOC]

## Setup Django production

### Prepare the project:

#### Ensure settings are production-ready:

Set `DEBUG = False` in `settings.py`.

Add your domain name or server IP to `ALLOWED_HOSTS`.

```
ALLOWED_HOSTS = ['your-domain.com', 'your-server-ip']
```

#### Apply migrations:

```
python manage.py migrate
```

#### Create a virtual environment for your Django project:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

#### Collect static files: Run the following command to gather all static files:

```
python manage.py collectstatic
```

### Install required software:

#### Update and install system packages:

```
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

#### Install Gunicorn:

```
pip install gunicorn
```

### Configure Server:

#### Configure Gunicorn:

Test Gunicorn to ensure it can serve your application:

```
gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application
```

Create a file at `/etc/systemd/system/gunicorn.service`:

```
[Unit]
Description=gunicorn daemon for Django project
After=network.target

[Service]
User=your-user
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/env/bin/gunicorn --workers 3 --bind unix:/path/to/your/project/myproject.sock myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable the Gunicorn service:

```
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

#### Configure Nginx:

Create a file at `/etc/nginx/sites-available/myproject`:

```
server {
    listen 80;
    server_name your-domain.com your-server-ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /path/to/your/project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/your/project/myproject.sock;
    }
}
```

Enable the site:

```
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```

Test the Nginx configuration:

```
sudo nginx -t
```

Restart Nginx:

```
sudo systemctl restart nginx
```

### Secure with SSL (optional):

#### Use Certbot to install and configure an SSL certificate:

Install Certbot:

```
sudo apt install certbot python3-certbot-nginx
```

Obtain and install the certificate:

```
sudo certbot --nginx -d your-domain.com
```

Test automatic renewal:

```
sudo certbot renew --dry-run
```

### Verify the deployment:

Access your Django project in a browser using your domain name or server IP.

#### Check logs for issues:

- Gunicorn: `sudo journalctl -u gunicorn`
- Nginx: `sudo tail -f /var/log/nginx/error.log`