# API deployment on vps server guide
### TODO:
- write detailed description for each step
- add links to the source (https://medium.com/geekculture/deploying-flask-application-on-vps-linux-server-using-nginx-a1c4f8ff0010)
- write another way to deploy api with docker and docker-compose!!!

## 1. Create a new user for api service and grant it sudo privileges
```bash
adduser api_user
usermod -aG sudo user_name
```

## 2. Setup and run python virtual environment
```bash
su user_name
sudo apt-get install python3-pip
sudo pip3 install virtualenv
virtualenv --version
virtualenv --python=/usr/bin/python3.6 webapp
source webapp/bin/activate
```

## 3. Preapare virtual environment - install dependencies
```bash
pip3 install wheel
pip3 install flask
pip3 install gunicorn
```

## 4. Prepare basic project file
```python
from flask import Flask
import os
app = Flask(__name__)
@app.route('/')
def index():
   return "Hello World!"
if __name__ == "__main__":
   app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 5000)))
```

Test the code locally:
```bash
python3 flaskapp.py
```

## 5. WSGI(Web Server Gateway Interface) Configuration
Create a wsgi.py file like a crossover point to use in configuration
```python
from flaskapp import app
if __name__ == "__main__":
   app.run()
```
This will be in the same directory with the flaskapp.py main module
We can control Gunicorn with belove command by giving IP and port parameters information that we want to run on.
```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

## 6. Create a service file for Gunicorn
```bash
sudo vi /etc/systemd/system/flaskapp.service
```
```bash
[Unit]
Description=A Gunicorn example to serve Flask project
After=network.target
[Service]
User=user_name
Group=www-data
WorkingDirectory=/home/user_name/webapp/project_folder
Environment="PATH=/home/user_name/webapp/bin"
ExecStart=/home/user_name/webapp/bin/gunicorn --workers 3 --bind unix:/home/user_name/webapp/project_folder/flaskapp.sock -m 007 wsgi:app
[Install]
WantedBy=multi-user.target
```
Change the user_name with yours. webapp is the python virtual environment folder we have created before. project_folder is the folder that contains flaskapp.py, wsgi.py, and your other project files

Control the service with the following commands:
```bash
sudo systemctl start flaskapp
sudo systemctl enable flaskapp
sudo systemctl status flaskapp
```

## 7. Configure Nginx as a reverse proxy
Install the server
```bash
sudo apt-get install nginx
```

There are two different directories names sites-available and sites-enabled. Sites under available are defined but inactive sites. So, we will make a connection with a symbolic link to the enabled directory after making the definition available. Thus, our website will be active.
```bash
sudo vi /etc/nginx/sites-available/flaskapp
```
```bash
server {
    listen port_no;
    server_name external_ip domain_name;
location / {
        proxy_pass http://unix:/home/user_name/webapp/project_folder/flaskapp.sock;
    }
}
```
The path in location is the same as the socket that we created in the service configuration. Give the port_no to listen, you choose.
```bash
sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled
```
Restart the Nginx server
```bash
sudo systemctl restart nginx
```
Need to give Nginx full access:
```bash
sudo ufw allow ‘Nginx Full’
```
?Check what that command does?


