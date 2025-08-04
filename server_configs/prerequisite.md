# install prerequisites for the project

## system dependencies
```bash
sudo apt install -y nginx
sudo apt install postgresql postgresql-contrib -y
sudo apt install g++ libpq-dev gcc
```

## python dependencies
```
sudo apt install python3.12-venv python3.12-dev python3-pip
```
## setup project dependencies
```bash
cd /home/ubuntu/iron-track/backend
python3 -m venv venv
pip install -r requirements.txt
python manage.py migrate
```
## setup a systemd service
## setup nginx
## install ssl certificate 
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```



