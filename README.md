# test.job


## Регистрация пользователя по автотокену

### эндпойнт - /api/users/ POST
```
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "256554test"
}
```
## Получение токена POST
### эндпоинт - /api/auth/token/login/
```
{
  "email": "vpupkin@yandex.ru",
  "password": "256554test"
}
```

## Получаем список продуктов GET
### эндпоинт - api/products/
```
[
    {
        "id": 1,
        "creator": {
            "first_name": "Kolius",
            "last_name": "Varlamov"
        },
        "name": "Бекенд",
        "start_date": "2024-04-01 12:10:30",
        "price": "5500.00"
    }
]
```
## Запись/покупка продукта POST
### эндпоинт - api/products/{int}/shopfavorite/
```
{
    "name": "Фронтенд",
    "start_date": "11-04-2024 12:12",
    "price": "5500.00",
    "student_counter": 5
}
```
- Ответ 
```
{
    "id": 1,
    "purchase_date": "2024-03-01T11:34:20.024634Z",
    "buyer": 2,
    "product": "Бекенд",
    "user": "vasya.pupkin",
    "group": "Группа 2"
}
```
## Создание продукта POST
### ### эндпоинт - api/products/
```
{
    "name": "Фронтенд",
    "start_date": "11-04-2024 12:12",
    "price": "5500.00",
    "student_counter": 5
}
```
- Ответ для обычного юзера
```
{
    "detail": "Только администраторы могут создавать продукты"
}
```
- Ответ для учителей
```
{
    "name": "Фронтенд",
    "start_date": "11-04-2024 12:12",
    "price": "5500.00",
    "student_counter": 5
}
```
## Вовод информации о продукте
### эндпоин - /api/products/
```
[
    {
        "id": 1,
        "creator": {
            "first_name": "Kolius",
            "last_name": "Varlamov"
        },
        "name": "Бекенд",
        "start_date": "01-04-2024 12:10",
        "price": "5500.00",
        "groups": [
            {
                "name": "группа 1",
                "students_count": 1
            },
            {
                "name": "Группа 2",
                "students_count": 1
            }
        ]
    },
    {
        "id": 4,
        "creator": {
            "first_name": "Вася",
            "last_name": "Пупкин"
        },
        "name": "Фронтенд",
        "start_date": "01-04-2024 00:00",
        "price": "5500.00",
        "groups": []
    },
    {
        "id": 5,
        "creator": {
            "first_name": "Вася",
            "last_name": "Пупкин"
        },
        "name": "Фронтенд",
        "start_date": "11-04-2024 12:12",
        "price": "5500.00",
        "groups": []
```
