# Деплой и инфраструктура

порядок запуска приложения:

`sudo docker compose up -d --build` - для сборки докера

`sudo docker compose up` - для запуска

`sudo docker compose exec web python manage.py createsuperuser` - для создания суперпользователя

везде `sudo` потому как докер как-то очень хреново работает с виндой. в результате пришлось расчехлять свой vb :)
