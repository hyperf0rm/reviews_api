# reviews_api
Проект представляет собой API, через который можно публиковать отзывы к различным произведениям, а также оставлять комментарии к этим отзывам

### Импортирование файлов csv в базу данных
Чтобы импортировать тестовую базу данных в проект, находясь в диектории api_yamdb/api_yamdb выполните команду:
```
python manage.py import_test_data
```
Вы также можете импортировать данные из csv файла, используя одну из доступных команд:
- import_users - импортировать пользователей
- import_category - импортировать категории
- import_genre - импортировать жанры
- import_titles - импортировать произведения
- import_review - импортировать отзывы
- import_comments - импортировать комментарии к отзывам

Для импорта введите команду, находясь в диектории api_yamdb/api_yamdb:

```
python manage.py <название команды> <путь к файлу csv>
```
Пример:

```
python manage.py import_category static/data/category.csv
```
Примеры составления составления csv файла для импортирования в базу данных можно посмотреть в диектории api_yamdb/api_yamdb/static/data/, там подготовлены файлы в правильном оформлении. 
