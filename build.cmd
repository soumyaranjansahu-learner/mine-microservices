call venv\Scripts\activate.bat
pip install django djangorestframework djangorestframework-simplejwt requests django-cors-headers

django-admin startproject mine_gateway
cd mine_gateway
python manage.py startapp gateway
cd ..

django-admin startproject mine_kitchen
cd mine_kitchen
python manage.py startapp kitchen
cd ..

django-admin startproject mine_shop
cd mine_shop
python manage.py startapp shop
cd ..

django-admin startproject mine_music
cd mine_music
python manage.py startapp music
cd ..
