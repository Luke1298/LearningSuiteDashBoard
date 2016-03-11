# LearningSuiteDashBoard
sudo pip install virtualenv
virtualenv -p /usr/bin/python2.7 venv
source ./venv/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver
Go to 127.0.0.1:8000
