# Проект онлайн-обучения на Django + Docker

## Быстрый запуск

1. Склонируйте репозиторий
   git clone https://github.com/Shegol164/Django-REST-Framework.git

2. Создайте и настройте .env файл
   cp .env.example .env
3. Запустите все сервисы
   docker-compose up -d

4. Выполните миграции (если нужно)
   docker-compose exec backend python manage.py migrate
5. Создайте суперпользователя
   docker-compose exec backend python manage.py createsuperuser

## Сервисы и порты
 - Django Backend: http://localhost:8000
 - PostgreSQL Database: localhost:5432
 - Redis: localhost:6379
 - Celery Worker: работает в фоне
 - Celery Beat: работает в фоне

### Проверка работоспособности
- Бэкенд
   curl http://localhost:8000/api/courses/
- База данных
   docker-compose exec db psql -U ${DB_USER} -d ${DB_NAME} -c "\l"
- Redis
   docker-compose exec redis redis-cli ping
Celery
- docker-compose logs celery
- Celery Beat
  docker-compose logs celery_beat

   
    


   