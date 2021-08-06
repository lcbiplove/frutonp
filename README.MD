# Hamikisan
The project expects to build an online platform to add fresh products like fruits and vegetables. Users can be authenticated through email and password. Website is compatible with any device.

### Features
- User authentication and authorization
- User integration with email to verify account / reset password
- Google recaptcha version 2 
- Notification System
- Use of websocket in notification and in post page
- Localization in nepali and english language
- Pagination and search 

### Requirements

Django is used as a backend framework of the project. Redis is used to get real-time messages.
- python
- django
- redis

### Installation

To install the project, we will have to first install redis. It is available easily in linux subsystems and also available for [windows](https://github.com/dmajkic/redis/downloads). After you have extracted the zip file, you can run the redis server from *redis-server.exe*. 

Select your directory to use the project and clone the repo.
```
git clone https://github.com/lcbiplove/frutonp.git
```
After you have cloned the project. We will be using a *virtual environment* to separate our dependencies. So in the same directory as frutonp:
```
python -m venv <venv>
```
Where <venv> is the name of our virtual environment folder

To activate the environment we will to:
```
<venv>\Scripts\activate.bat             # In windows cmd
source <venv>/bin/activae               # In Linux bash
```
Now we will install all our dependency:
```
pip install -r requirements.txt
```
And, migrate to create tables before running the server:
```
python manage.py migrate
```
Before starting the server, we will first create a *.env* file add environment variables. Create a *.env* file in the root level as *manage.py*. There is a sample of environment variable in file called *sample_env.txt*. You can copy the content of *sample_env.txt* and add your required values to it. You can ignore *DB_SOMETHING* if  you are going with default database (sqlite). 

Now you have added the environment variables, you can run the server:
```
python manage.py runserver
```