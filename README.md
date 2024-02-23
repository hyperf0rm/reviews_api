###Импортирование файлов csv в базу данных
Чтобы импортировать тестовую базу данных в проект, находясь в диектории api_yamdb/api_yamdb выполните команду:
```
python manage.py import_test_data
```
Вы также можете импортировать данные из csv файла, используя одну из доступных команд:
- import_category - импортировать категории
- import_genre - импортировать жанры
- import_review - импортировать отзывы
- import_titles - импортировать произведения
- import_users - импортировать пользователей

Для импорта введите команду, находясь в диектории api_yamdb/api_yamdb:

```
python manage.py <название команды> <путь к файлу csv>
```
Пример:

```
python manage.py import_category static/data/category.csv
```
Примеры составления составления csv файла для импортирования в базу данных можно посмотреть в диектории api_yamdb/api_yamdb/static/data/, там подготовлены файлы в правильном оформлении. 