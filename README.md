# LMS API
---

Проект разработан командой из трех человек:

- Разработчик 1 - Михаил Гаврилов _(@m.gavrilov)_

- Разработчик 2 - Константин Попов _(@k.popov)_

- Разработчик 3 - Василий Белов _(@v.belov)_

  

---

## Краткое описание
LMS API — это система управления обучением, предназначенная для создания и управления курсами, темами, задачами и пользователями. Она обеспечивает базовые функции для преподавателей и студентов, включая регистрацию пользователей, создание и управление курсами, а также решение и оценку задач.

## Возможности приложения
- **Регистрация пользователей**: Возможность регистрации студентов и преподавателей с автоматической генерацией пароля для студентов.
- **Управление курсами**: Создание, обновление и удаление курсов.
- **Управление темами**: Создание, обновление и удаление тем внутри курсов.
- **Управление задачами**: Создание, обновление, удаление и решение задач с возможностью оценки.
- **Авторизация и контроль доступа**: Реализация базовой авторизации с использованием заголовка `Authorization` и контроля прав доступа для различных ролей.

## Инструкции по запуску
### 1. Установка зависимостей
Для запуска приложения необходимо установить все необходимые пакеты. Для этого выполните команду:

``pip install -r requirements.txt``

### 2. Запуск приложения
После установки зависимостей запустите приложение с помощью команды:

``python app.py``

Приложение будет доступно по адресу `http://localhost:5000`.

### 3. Использование API
#### Регистрация пользователя
````curl -X POST  
[http://localhost:5000/auth/signIn](http://localhost:5000/auth/signIn)  
-H 'Content-Type: application/json'  
-d '{"login": "user1", "first_name": "Иван", "last_name": "Иванов", "role": "student"}'
````

#### Создание курса
````
curl -X POST  
[http://localhost:5000/courses](http://localhost:5000/courses)  
-H 'Content-Type: application/json'  
-d '{"name": "Test Course", "description": "Test Description"}'
````

#### Создание темы в курсе
````
curl -X POST  
[http://localhost:5000/courses/1/topics](http://localhost:5000/courses/1/topics)  
-H 'Content-Type: application/json'  
-d '{"title": "Test Topic", "content": "Test Content"}'
````


#### Создание задачи в курсе
````
curl -X POST  
[http://localhost:5000/courses/1/problems](http://localhost:5000/courses/1/problems)  
-H 'Content-Type: application/json'  
-d '{"description": "Test Problem"}'
````

#### Решение задачи
````
curl -X PUT  
[http://localhost:5000/courses/1/problems/1/solve](http://localhost:5000/courses/1/problems/1/solve)  
-H 'Content-Type: application/json'  
-d '{"solution": "Test Solution", "student_id": 1}'
````

#### Оценка задачи
````
curl -X POST  
[http://localhost:5000/courses/1/problems/1/grade](http://localhost:5000/courses/1/problems/1/grade)  
-H 'Content-Type: application/json'  
-d '{"grade": "A", "student_id": 1}'
````

 ### 4. Авторизация Для авторизации используйте заголовок `Authorization` с типом `Basic`. Например: 
````
curl -X GET  
[http://localhost:5000/test](http://localhost:5000/test)  
-H 'Authorization: Basic <base64_encoded_login_and_password>'
````

Замените `<base64_encoded_login_and_password>` на закодированные в base64 логин и пароль, разделенные двоеточием.   ## Тестирование Для запуска тестов используйте команду:

``python -m unittest discover``
Эта команда запустит все тесты, определенные в директории `tests`.   

## Docker Для запуска приложения в Docker выполните следующие шаги: 
`1. Создайте образ:`

``docker build -t my-lms-app``

`2. Запустите контейнер:` 

``docker run -p 5000:5000 my-lms-app``

 ``Приложение будет доступно по адресу `http://localhost:5000``