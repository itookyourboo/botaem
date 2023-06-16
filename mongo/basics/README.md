# Основы MongoDB

MongoDB как документоориентированная база данных NoSQL, особенность и типы данных.

---

## Что это

MongoDB - это СУБД, которая относится к классу NoSQL-баз данных и использует документоориентировааную модель данных. MongoDB хранит данные в документах BSON (бинарный формат JSON), которые могут содержать в себе различные типы данных и могут быть вложенными друг в друга. Благодаря этому MongoDB обеспечивает более гибкую схему данных и более простую масштабируемость.

Особенностью MongoDB является гибкость в управлении схемой данных. В реляционных базах данных требуется определенный набор колонок и типов данных для каждой таблицы, в то время как в MongoDB каждый документ может иметь свою уникальную структуру и схему данных.

## Концепции

- База данных может иметь ноль или более "коллекций".
- Коллекции состоят из нуля или более "документов".
- Документ состоит из одного или более "полей".
- Индексы почти идентичны таковым в реляционных БД.

## Типы данных

- Строки (string)
- Числа (number)
- Булевы значения (boolean)
- Даты (date)
- Объекты (object)
- Массивы (array)
- Объекты идентификаторов (ObjectId)
- Бинарные данные (binary data)
- Регулярные выражения (regular expressions)
- Код JavaScript (JavaScript code)
- Ссылки на другие документы (DBRefs)

## Установка с помощью Docker

### Загрузка образа MongoDB

Чтобы загрузить образ MongoDB, выполните следующую команду:

```shell
docker pull mongo
```

Эта команда загрузит последнюю версию образа MongoDB из Docker Hub и сохранит его локально на вашей машине.

### Запуск контейнера MongoDB

Чтобы запустить контейнер MongoDB, выполните следующую команду:

```shell
docker run -p 27017:27107 --name my-mongo -d mongo
```

Эта команда запускает новый контейнер MongoDB в фоновом режиме и назначает ему имя "my-mongo". Флаг `-d` указывает Docker запустить контейнер в фоновом режиме.

### Проверка работоспособности контейнера

Чтобы проверить, что контейнер MongoDB запущен и работает правильно, мы можем выполнить команду `docker ps`, которая показывает список запущенных контейнеров на нашей машине.

```shell
docker ps
```

Вы должны увидеть контейнер MongoDB с именем "my-mongo" в списке.

### Использование

Теперь, когда контейнер MongoDB запущен, мы можем использовать его для хранения и получения данных. Для подключения к MongoDB в контейнере, мы можем использовать любой инструмент или библиотеку MongoDB, которая поддерживает подключение к MongoDB по IP-адресу и порту.

Например, если вы хотите подключиться к MongoDB в контейнере через терминал, вы можете выполнить следующую команду:

```shell
docker exec -it my-mongo mongosh
```

Эта команда подключает вас к MongoDB в контейнере и открывает интерактивный терминал mongosh. Теперь вы можете использовать mongosh для выполнения команд MongoDB.

### Остановка и удаление контейнера

Когда вы закончите использование контейнера MongoDB, вы можете остановить его с помощью команды `docker stop`, а затем удалить с помощью команды `docker rm`.

Чтобы остановить контейнер MongoDB, выполните следующую команду:

```shell
docker stop my-mongo
```

Чтобы удалить контейнер MongoDB, выполните следующую команду:

```shell
docker rm my-mongo
```

## Практика

Сперва для выбора базы данных воспользуемся глобальным методом `use` — введите `use learn`. Неважно, что база данных пока ещё не существует. В момент создания первой коллекции создастся база данных `learn`. 

Теперь, когда вы внутри базы данных, можно вызывать у неё команды, например `db.getCollectionNames()`. В ответ увидите пустой массив - `[ ]`. 

Мы просто можем вставить документ в новую коллекцию. Чтобы это сделать, используйте команду `insertOne`, передав ей вставляемый документ:

```javascript
test> db.unicorns.insertOne({name: 'Aurora', gender: 'f', weight: 450})
{
  acknowledged: true,
  insertedId: ObjectId("648cb06c5565741ce5003f53")
}
```

Теперь у коллекции `unicorns` можно вызвать метод `find`, который вернёт список документов:

```javascript
test> db.unicorns.find()
[
  {
    _id: ObjectId("648cb06c5565741ce5003f53"),
    name: 'Aurora',
    gender: 'f',
    weight: 450
  }
]
```

Кроме данных, которые мы задавали, появилось дополнительное поле `_id`. Каждый документ должен иметь уникальное поле `_id`.

Давайте вставим кардинально отличный от предыдущего документ в unicorns, вот такой:

```javascript
test> db.unicorns.insertOne({name: 'Leto', gender: 'm', home: 'Arrakeen', worm: false})
{
  acknowledged: true,
  insertedIds: { '0': ObjectId("648cb1ab5565741ce5003f54") }
}
```

И еще раз вызовем метод `find`:

```javascript
test> db.unicorns.find()
[
  {
    _id: ObjectId("648cb06c5565741ce5003f53"),
    name: 'Aurora',
    gender: 'f',
    weight: 450
  },
  {
    _id: ObjectId("648cb1ab5565741ce5003f54"),
    name: 'Leto',
    gender: 'm',
    home: 'Arrakeen',
    worm: false
  }
]
```

## Селекторы

Селектор запросов MongoDB аналогичен предложению **where** SQL-запроса. Он используется для поиска, подсчёта, обновления и удаления документов из коллекций.

Для начала удалим всё, что до этого вставляли с помощью `db.unicorns.deleteMany({})`. Мы не передали селектор, поэтому произойдет удаление всех документов.

```javascript
test> db.unicorns.deleteMany({})
{ acknowledged: true, deletedCount: 2 }
```

Теперь произведём следующие вставки:

```javascript
db.unicorns.insert({name: 'Horny', dob: new Date(1992,2,13,7,47), loves: ['carrot','papaya'], weight: 600, gender: 'm', vampires: 63});
db.unicorns.insert({name: 'Aurora', dob: new Date(1991, 0, 24, 13, 0), loves: ['carrot', 'grape'], weight: 450, gender: 'f', vampires: 43});
db.unicorns.insert({name: 'Unicrom', dob: new Date(1973, 1, 9, 22, 10), loves: ['energon', 'redbull'], weight: 984, gender: 'm', vampires: 182});
db.unicorns.insert({name: 'Roooooodles', dob: new Date(1979, 7, 18, 18, 44), loves: ['apple'], weight: 575, gender: 'm', vampires: 99});
db.unicorns.insert({name: 'Solnara', dob: new Date(1985, 6, 4, 2, 1), loves:['apple', 'carrot', 'chocolate'], weight:550, gender:'f', vampires:80});
db.unicorns.insert({name:'Ayna', dob: new Date(1998, 2, 7, 8, 30), loves: ['strawberry', 'lemon'], weight: 733, gender: 'f', vampires: 40});
db.unicorns.insert({name:'Kenny', dob: new Date(1997, 6, 1, 10, 42), loves: ['grape', 'lemon'], weight: 690,  gender: 'm', vampires: 39});
db.unicorns.insert({name: 'Raleigh', dob: new Date(2005, 4, 3, 0, 57), loves: ['apple', 'sugar'], weight: 421, gender: 'm', vampires: 2});
db.unicorns.insert({name: 'Leia', dob: new Date(2001, 9, 8, 14, 53), loves: ['apple', 'watermelon'], weight: 601, gender: 'f', vampires: 33});
db.unicorns.insert({name: 'Pilot', dob: new Date(1997, 2, 1, 5, 3), loves: ['apple', 'watermelon'], weight: 650, gender: 'm', vampires: 54});
db.unicorns.insert({name: 'Nimue', dob: new Date(1999, 11, 20, 16, 15), loves: ['grape', 'carrot'], weight: 540, gender: 'f'});
db.unicorns.insert({name: 'Dunx', dob: new Date(1976, 6, 18, 18, 18), loves: ['grape', 'watermelon'], weight: 704, gender: 'm', vampires: 165});
```

Приступим к освоению селекторов.

* `{поле: значение}` используется для поиска всех документов, у которых _поле_ равно _значение_.
* `{поле1: значение1, поле2: значение2}` работает как логическое И.
* Специальные операторы `$lt`, `$lte`, `$gt`, `$gte`, `$ne` используются для выражения операций "меньше", "меньше или равно", "больше", "больше или равно" и "не равно". Например, чтобы получить всех самцов единорога, весящих более 700 фунтов, можно написать:
    ```javascript
    db.unicorns.find({gender: 'm', weight: {$gt: 700}})
    ```
* Оператор `$exists` используется для проверки наличия или отсутствия поля, например:
    ```javascript
    db.unicorns.find({vampires: {$exists: false}})
    ```
* Если нужно ИЛИ вместо И, можно использовать оператор `$or` и присвоить массив значений:
    ```javascript
    db.unicorns.find({gender: 'f', $or: [{loves: 'apple'}, {loves: 'orange'}, {weight: {$lt: 500}}]})
    ```
  Вышеуказанный запрос вернёт всех самок единорогов, которые или любят яблоки, или любят апельсины, или весят менее 500 фунтов. 
* MongoDB поддерживает массивы как объекты первого класса. Выборка по значению массива: `{loves: 'watermelon'}` вернёт все документы, у которых `watermelon` является одним из значений поля `loves`.
* Самый гибкий оператор - `$where`. Он позволяет передавать JavaScript для его выполнения на сервере.
    ```javascript
    db.unicorns.find({$where: function() { return (this.weight % 100 == 0) }})
    ```
