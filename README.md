# Инструкция по развёртыванию системы на ОС Linux Ubuntu

## Шаг 1. Клонирование репозитория
1. Открыть терминал.
2. С помощью команды `cd` перейти в каталог, где будет размещён проект.
3. Выполнить команду для клонирования проекта:
```bash
git clone https://github.com/arinazaikina/Skypro_Course_6_SkyStore.git
```
4. Перейти в каталог проекта
```bash
cd Skypro_Course_6_SkyStore
```
5. Переключиться на ветку разработки
```bash
git checkout hw_23.1
```

## Шаг 2. Установка зависимостей
1. Убедиться, что в системе установлен Python3.x. 
Если нет, установить его в соответствии с инструкциями для вашей операционной системы.
2. Создать виртуальное окружение
```bash
python3 -m venv venv
```
4. Активировать виртуальное окружение
```bash
source venv/bin/activate
```
5. Перейти в каталог sky_store
```bash
cd sky_store
```
6. Установить зависимости проекта, указанные в файле `requirements.txt`
```bash
pip install -r requirements.txt
```

## Шаг 3. Установка и настройка Redis
1. Установить Redis, если он не установлен.
Например, для Ubuntu выполнить следующую команду
```bash
sudo apt-get install redis-server
```
2. Запустить Redis
```bash
sudo service redis-server start
```
Это запустит Redis сервер и он будет слушать на стандартном порту 6379.
3. Убедиться, что Redis работает правильно, выполнив команду
```bash
redis-cli ping
```
Если Redis работает должным образом, в ответ придёт `PONG`.

## Шаг 4. Установка и настройка PostgreSQL
1. Установить PostreSQL, если он не установлен.
Например, для Ubuntu выполнить следующую команду
```bash
sudo apt-get install postgresql
```
2. Выполнить вход в интерактивную оболочку PostgreSQL от имени пользователя postgres
```bash
sudo -u postgres psql
```
3. Внутри интерактивной оболочки PostgreSQL создать базу данных 
с помощью следующей команды:
```bash
CREATE DATABASE sky_store_project;
```
`sky_store_project` - название БД
4. Закрыть интерактивную оболочку PostgreSQL
```bash
\q
```

## Шаг 5. Настройка окружения
1. В директории sky_store создать файл `.env`
```bash
touch .env
```
2. Открыть файл
```bash
nano .env
```
3. Записать в файл следующие настройки
```
DB_NAME=название_бд (sky_store_project)
DB_USER=имя_пользователя_бд (postgres)
DB_PASSWORD=пароь_пользователя_бд
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=адрес_электронной_почты_для_аутенфикации_на_почтовом_сервере
EMAIL_HOST_PASSWORD=пароль_для_для_аутенфикации_на_почтовом_сервере
```
В каталоге sky_store есть шаблон файла .env

## Шаг 6. Применение миграций
1. Из каталога проекта sky_store выполнить команду
```bash
python manage.py migrate
```

## Шаг 7. Создание групп пользователей
1. Из каталога проекта sky_store выполнить команду
```bash
python manage.py creategroups
```

## Шаг 7. Загрузка данных с помощью фикстур
```bash
python manage.py loaddata app_user_data.json
```
```bash
python manage.py loaddata app_blog_data.json
```
```bash
python manage.py loaddata app_catalog_data.json
```
```bash
python manage.py loaddata app_newsletter_data.json
```

## Шаг 8. Запуск celery
1. Открыть новое окно терминала
2. Если виртуальное окружение неактивно, активировать его
```bash
cd .. &&  source venv/bin/activate
```
3. Из каталога проекта sky_store запустить celery
```bash
cd sky_store && celery -A config worker --loglevel=info
```

## Шаг 8. Запуск celery-beat
1. Открыть новое окно терминала
2. Если виртуальное окружение неактивно, активировать его
```bash
cd .. &&  source venv/bin/activate
```
3. Из каталога проекта sky_store запустить celery
```bash
cd sky_store && celery -A config beat --loglevel=info
```

## Шаг 9. Запуск сервера Django
1. Открыть новое окно терминала
2. Если виртуальное окружение неактивно, активировать его
```bash
cd .. &&  source venv/bin/activate
```
3. Из каталога проекта sky_store запустить сервер
```bash
cd sky_store && python manage.py runserver
```