## Create a systemd service for backend
```
%% /etc/systemd/system/irontrack.service
[Unit]
Description=iron-track
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/irontrack
ExecStart=/home/ubuntu/iron-track/backend/venv/bin/gunicorn \
          --access-logfile - \
          --bind 127.0.0.1:8000 \
         core.wsgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```
