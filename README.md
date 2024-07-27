![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)

# Task Hub API

> API сервис для управления задачами

## Содержание

+ [Описание](#description)
+ [Установка и запуск](#install)
+ [API Endpoints:](#api_endpoints)
    + [Создание новой задачи](#create)
    + [Получение списка всех задач](#get_all)
    + [Получение задачи по идентификатору](#get_one)
    + [Обновление задачи](#update)
    + [Удаление задачи](#delete)
+ [Errors](#errors)
+ [Contacts](#contacts)

<a id="description"></a>

## Описание

API Сервис предоставляет возможность создания, обновления, удаления и получения информации о задачах.

Сервис написан на языке `Python` с использование библиотеки `FastAPI`.
Данные хранятся в базе данных `MySQL`.  
API сервис и база данных запускаются в `Docker` контейнерах с использованием `Docker Compose`.  
Данные в хранилище `MySQL` сохраняются после остановки или удаления контейнеров.

Особенности:
    + код покрыт тестами `pytest` и проверен с использованием `coverage`, `mypy`, `pylint`.

<a id="install"></a>

## Установка и запуск

> Для запуска сервиса требуется установленный [Docker](https://www.docker.com/get-started/).

1. Клонировать репозиторий с GitHub:

  ```bash
  git clone git@github.com:moduleb/task_hub.git
  ```

> альтернативный вариант - скачать архив проекта со страницы на [GitHub](https://github.com/moduleb/task_hub)

2. Перейти в папку с проектом:

  ```bash
  cd task_hub
  ```

3. Собираем и запускаем образ

  ```bash
docker compose up -d --build
  ```

4. Для остановки контейнера используйте команду:

  ```bash
  docker compose down
  ```

<a id="api_endpoints"></a>

# API Endpoints

- Address: [http://0.0.0.0:8000](http://0.0.0.0:8000)
- Документация Swagger [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

<a id="create"></a>

## Create

> Создание новой задачи

#### Request

**`POST /tasks`**

>'taskname' должно быть уникальным, остальные поля могут быть пустыми

```json
  {
    "taskname": "Task1",
    "description": "Create a picture",
    "category": "Hobby"
  }
```

#### Response

`200 Successful`

```json
{
  "detail": "Task created successfully"
}
```

---

<a id="get_one"></a>
## Get one

> Получение информации о задаче

#### Request

`GET /tasks/{task_id}`

#### Response

`200 Successful`

```json
{
  "data": {
    "id": 18,
    "taskname": "Task1",
    "description": "Create a picture",
    "category": "Hobby",
    "creation_date": "2023-12-11T19:35:46"
  }
}
```

<a id="get_all"></a>
## Get all

> Получение информации о всех заданиях

#### Request

`GET /tasks`

#### Response

`200 Successful`

```json
{
  "data": [
    {
      "id": 18,
      "taskname": "Task1",
      "description": "Create a picture",
      "category": "Hobby",
      "creation_date": "2023-12-11T19:35:46"
    },
    {
      "id": 20,
      "taskname": "Task2",
      "description": "Create a program",
      "category": "Hobby",
      "creation_date": "2023-12-11T19:35:46"
    }
  ]
}
```

---

<a id="update"></a>
## Update

> Обновление информации о задаче

#### Request

**`PUT /tasks`**

>'taskname' должно быть уникальным, остальные поля могут быть пустыми

```json
  {
    "taskname": "Task1",
    "description": "Create a picture",
    "category": "Hobby"
  }
```

#### Response

`200 Successful`

```json
{
  "detail": "Task updated successfully"
}
```

---

<a id="delete"></a>
## Delete
> Удаление задачи

#### Request

`DELETE /tasks/{task_id}`

#### Response

`204 No Content`


---

<a id="errors"></a>

## Errors

- **404 Not Found** - задача не найдена
- **405 Method Not Allowed**
- **409 Conflict** - задача с таким названием уже существует
- **422 Unprocessable Entity** - поле содержит недопустимые символы
- **500 Internal Server Error** - внутренняя ошибка сервера


