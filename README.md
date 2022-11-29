![Foodgram workflow](https://github.com/an-nastasiia/foodgram-project-react/actions/workflows/main.yml/badge.svg)

[English](#about-foodgram) | [Русский](#что-такое-foodgram)

---

# FOODGRAM

### Project domain name:

http://foodgram.serveblog.net/

## **About Foodgram:**

**Foodgram** is a website with user-added recipes. Unauthorized users are restricted to creating a new account and viewing recipes with filtration by tags and author available. Those who already has account can authorize with their email and password and then publish their own recipes, follow other users, add recipes to the Favorites and Shopping Cart.

* To sign up a user needs to enter their first name, last name, email, username and password. After authorization is complete a user can change their password. When signing in with the email and password, a user recieves a token which is deleted after logout.

* Users can add new recipes to the website choosing at least one of pre-added ingredients. Picture, Descriprion, Cooking Time and Tags fields must be specified.

* Recipes liked by a user are stored in the Favorites section. Filtration by tag is available.

* Subscriptions section represents authors followed by current user and some of their recipes. Full lists of authors' recipes are available via hyperlinks.

* Recipes added to the Shopping Cart are transformed into a list of unique ingredients with its amount indicated. A user can download the list as PDF file.

## **Tech Stack:**

*Python 3.7.9*

*Django 3.2.16*

*Django REST framework 3.14.0*

*Docker 20.10.20*

*Docker Compose 2.12.1*

*PostgreSQL 13.0*

*nginx 1.21.3*

*Gunicorn 20.0.4*

## **Starting Foodgram in Docker Containers:**

Navigate to the *foodgram-project-react/infra/* directory and input the following commands. Project will be available at *localhost/*.

```
# Build the images and run the containers:
docker-compose up -d

# Create and apply the migrations inside the 'backend' container:
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate

# Collect static files:
docker-compose exec backend python manage.py collectstatic --no-input

# Fill in database:
docker-compose exec backend python manage.py read_csv
docker-compose exec backend python manage.py loaddata data/fixtures.json
docker-compose exec backend cp -r data/media media/.

# Stop containers:
docker-compose stop

# Run stopped containers:
docker-compose start

# Stop and delete running containers:
docker-compose down -v
```

## **Example of .env file contents:**
```
SECRET_KEY='very_secret_key'
DEBUG=
ALLOWED_HOSTS='allowed_host_1 allowed_host_2 ... allowed_host_N'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db_name
DB_PORT=1234
```

## **Foodgram API**:

While Docker containers are running, documentation on the project's API with request examples and response schemas is available at http://localhost/api/docs/.

<br>
<br>
<br>
<br>
<br>

*Author: Anastasiia Antipina*

*Email: ananastasiia13@gmail.com*

---
# FOODGRAM

### Доменное имя проекта:

http://foodgram.serveblog.net/

## **Что такое Foodgram**:

Проект **Foodgram** - это сайт с пользовательскими рецептами. Неавторизованным посетителям доступны страница регистрации и просмотр рецептов с фильтрацией по тегам и авторам. Зарегистрированные пользователи, помимо просмотра, после авторизации могут публиковать собственные рецепты, подписываться на других пользователей, добавлять рецепты в избранное и список покупок.

* Для регистрации пользователь вводит свои имя и фамилию, юзернейм, адрес электронной почты и пароль. После авторизации пароль можно сменить. При авторизации по email и паролю пользователь получает токен, который удаляется при выходе из учетной записи.

* Рецепт создается из предустановленных ингредиентов. К нему нужно добавить фотографию, описание, время приготовления и выбрать теги для фильтрации. Все поля обязательные.

* Раздел "Избранное" содержит рецепты, добавленные туда пользователем. Доступна фильтрация по тегам.

* В разделе "Подписки" представлены авторы рецептов, на которых подписан текущий пользователь, и несколько их рецептов. Есть ссылка, по которой доступен полный список рецептов автора.

* Список покупок формируется автоматически из добавленных пользователем рецептов и содержит перечисление уникальных ингредиентов с указанием количества. Его можно скачать на свое устройство в формате PDF.

## **Технологии**:

*Python 3.7.9*

*Django 3.2.16*

*Django REST framework 3.14.0*

*Docker 20.10.20*

*Docker Compose 2.12.1*

*PostgreSQL 13.0*

*nginx 1.21.3*

*Gunicorn 20.0.4*

## **Запуск проекта в контейнерах:**

Находясь в директории *foodgram-project-react/infra/*, последовательно введите в терминале приведенные ниже комнады. Проект будет доступен по адресу *localhost/*.

```
# Создать и запустить контейнеры:
docker-compose up -d

# Создать и применить миграции в контейнере:
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate

# Собрать статику для корректного отображения сайта в браузере:
docker-compose exec backend python manage.py collectstatic --no-input

# Заполнить базу данных:
docker-compose exec backend python manage.py read_csv
docker-compose exec backend python manage.py loaddata data/fixtures.json
docker-compose exec backend cp -r data/media media/.

# Остановить контейнеры:
docker-compose stop

# Запустить остановленные контейнеры:
docker-compose start

# Остановить и удалить контейнеры:
docker-compose down -v
```

## **Шаблон наполнения env-файла:**
```
SECRET_KEY='very_secret_key'
DEBUG=
ALLOWED_HOSTS='allowed_host_1 allowed_host_2 ... allowed_host_N'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db_name
DB_PORT=1234
```

## **API сайта Foodgram:**

После запуска проекта в контейнерах полная документация с примерами запросов к API и схемами ответов станет доступна по ссылке http://localhost/api/docs/.

<br>
<br>
<br>
<br>
<br>

*Автор проекта: Анастасия Антипина*

*Email: ananastasiia13@gmail.com*

---