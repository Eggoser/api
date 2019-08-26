# Представляю вам REST API сервис на python

## Installation

#### 1. Необходимо клонировать репозиторий в папку с проектами и перейти в неё<br>
  `git clone https://github.com/Eggoser/api`<br>
  `cd api/mysite`

#### 2.1. Если вы на linux необходимые следующие python пакеты
  `sudo apt-get install python3-virtualenv python3-pip python3-setuptools`
  
#### 2.2. Если ваша ось windows введите следующие команды,<br>при этом у вас должен стоять третий питон
  `pip install virtualenv`
  
#### 3. Создайте виртуальное окружение и активируйте его (linux)
  `python3 -m virtualenv venv`  and  `source venv/bin/activate`<br><br>
   на виндовс операция почти аналогичная
   
#### 4. Установите python зависимости
  `pip install -r requirements.txt`
  

 
 #### 5.1. Установите mysql если у вас его нет
  `sudo apt-get install mysql-server`
  
 #### 5.2. Создайте базы данных flask и flasky
 Войдите:
  `mysql -u <user> -p <password>`
  
 Создайте:
```
  CREATE DATABASE flask;
  CREATE DATABASE flasky;
  exit
```
 
 #### 5.3. Запишите в виртуальное окружение пароль и пользователя от mysql
 `export DATABASE_USER=<your-database-username>`<br>
 `export DATABASE_PASSWORD=<your-database-password>`
 
 #### 6.1. Запустите скрипт создания таблиц который воспользуется данными из venv
 `python cr_all.py`<br><br> Используйте `python` без тройки
 
 #### 6.2. Перейдите в папку app/compile_c скомпильте сишки и вернитесь обратно
 `cd app/compile_c & python setup.py build_ext --inplace & cd ../..`
 
 #### 7.1. Для запуска тестов используйте
  `python manage.py runtest <peoples>`<br><br>
  peoples = Колличество пользователей которое будет сгенерировано
  
#### 7.2 Для запуска приложения введите команду
  `uwsgi --ini mysite.ini`
 
#### 8. Радуйтесь!!!!

## Немного под капотом

**Python Зависимости**
 * `flask` – Фреймворк очень удобен в разработке такого REST API
 * `flask_sqlalchemy` – `ORM` для баз данных, дополнение к `flask` основан на `sqlalchemy`
 * `numpy` – Библиотека для нахождения процентилей
 * `mimesis` – Может сгенерировать почти любую фейковую информацию
 * `cython` – Такого рода веб приложение требует высокой производительности, 
 cython ускоряет python код в **30** и более раз, компилируя его в `c`
 * `pymysql` – этот коннектор для `sqlalchemy` т. к. `mysql-connector` почему-то не работает
 * `mysql-connector` – для свободного доступа к таблицам, просто он мне нравиться
 * `uwsgi` – модуль для nginx
 
**Структура таблиц**
* persons – (id INT PRIMARY KEY auto_increment, value JSON not null) CHARACTER SET utf8 COLLATE utf8_general_ci
* birthdays – (id INT PRIMARY KEY auto_increment, value JSON not null)
* percentiles – (id INT PRIMARY KEY auto_increment, value JSON not null, date datetime not null) CHARACTER SET utf8 COLLATE utf8_general_ci
* booleans – (id INT PRIMARY KEY auto_increment, birthday_bool  tinyint(1) not null, percentile_bool  tinyint(1) not null)

* **POST /imports**
Принимает на вход json, 

**Не валидными данными являются**
* номер квартиры больше либо равен 0
* родственные связи не взаимообратные
* человек сам себе родственник
* дата не валидная
* какой либо из параметров = null
* название какого либо из параметров записано не верно

**Валидными данными являются**
* в списке родственников значения повторяются
* все остальное, что не перечислено выше

После загрузки данных в таблицу *persons*
вызываются `cython` функции, которые заполняют таблицы *birthdays* и *percentiles*.
Намного выгоднее записать результат выполнения всех трех get запросов и потом просто показывать его.
Значения в таблице booleans по умолчанию False и False, почему расскажу далее

* **PATCH /imports/$import_id/citizens/$citizen_id**<br>
Валидация входа той же функцией что и вход `POST /imports`
Так как массив citizens обновился стоило бы апдейтнуть *birthdays* и *perscentiles* под текущем *import_id*,
для этого запишем в booleans значения True для percentiles или для birthdays, это можно определить, по json, который подается на вход,
если в нем есть поле "town", тогда True для `percentiles`. Или если в json присутствует "relatives" соответственно это поле 
измениться, необходимо True для `birthdays`. Может измениться "birth_date", в таком случая True для `birthdays` и `percentiles`

* **GET /imports/$import_id/citizens**<br>
Здесь ничего сверхестественного, достаем из persons и показываем

* **GET /imports/$import_id/citizens/birthdays**<br>
В этом запросе смотрим, если в таблице booleans под этим import_id есть True для `birthdays`, тогда перезаписываем 
контент и возвращаем его пользователю. В случае с False, на что я и расчитывал, проектируя такую систему, стоит только достать из `birthdays`
и вернуть это

* **GET /imports/$import_id/towns/stat/percentile/age**<br>
Точно также как и с `birthdays`, только теперь проверяем на свежесть дату последнего апдейта, должна быть сегодняшней, иначе придется перезаписать

* Итог

Как итог, это умное приложение, способное правильно и объективно распределять производительность

## Testing

#### Тесты неотъемлемая часть каждого приложения в числе и веб

Я создал тесты, генерирующие фейковые данные, достаточно лишь указать сколько человек и они начнут генерацию, проверяя, сколько времени уйдет на
на обработку такого запроса приложением и выведут status_code.
Да, relatives тоже генерируются!!!
Еще у них есть возможность генерировать не валидные данные, они об этом все время оповещают

Если ожидался другой status_code, возбуждается ошибка

**Спасибо, что уделили внимание прочтению моего README**
