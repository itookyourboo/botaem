# Конфигурация Redis

Понимание основных параметров конфигурации Redis, включая файл redis.conf.

---

Один из ключевых аспектов работы с Redis - это конфигурация, которая позволяет настроить различные параметры для оптимальной работы базы данных.

Основные параметры конфигурации Redis задаются в файле redis.conf. Этот файл содержит набор директив, которые определяют поведение Redis при работе. Рассмотрим некоторые из наиболее важных параметров конфигурации Redis:

* Порт (`port`): Директива `port` определяет номер порта, на котором Redis будет прослушивать входящие соединения. По умолчанию Redis использует порт 6379.

* IP-адрес (`bind`): Директива `bind` указывает IP-адрес, на котором Redis будет прослушивать соединения. Если вам нужно прослушивать соединения на всех доступных сетевых интерфейсах, можно задать значение 0.0.0.0.
 
* Каталог данных (`dir`): Директива `dir` определяет каталог, в котором Redis будет сохранять свою базу данных на диске. Если вы не задаете этот параметр, Redis будет сохранять данные в оперативной памяти, что может привести к потере данных при перезапуске сервера.
 
* Пароль (`requirepass`): Директива `requirepass` позволяет установить пароль для доступа к Redis. Если вы хотите, чтобы Redis требовал аутентификации при подключении, вы можете задать пароль с помощью этой директивы.
 
* Максимальное количество клиентов (`maxclients`): Директива `maxclients` устанавливает максимальное количество одновременных подключений к Redis. Если это значение достигнуто, Redis будет отклонять новые соединения.
 
* Максимальный размер базы данных (`maxmemory`): Директива `maxmemory` определяет максимальный объем памяти, который Redis может использовать для хранения данных. Если эта граница достигнута, Redis будет использовать определенные алгоритмы удаления данных, чтобы освободить место для новых записей.
 
* Журнал (`logfile`): Директива `logfile` указывает файл, в который Redis будет записывать журнал своей работы. В журнале содержится информация о событиях, ошибках и других сведениях, которые могут быть полезными для анализа работы базы данных.

Помимо указанных директив, существует ряд других полезных и наиболее используемых директив в конфигурационном файле Redis. Вот несколько из них:

1. Таймауты соединений:
    * `timeout`: Директива `timeout` задает время ожидания для операций чтения/записи в Redis в секундах. Если клиент не отправляет или не получает данные в течение этого времени, соединение считается разорванным.
    * `tcp-keepalive`: Директива `tcp-keepalive` позволяет включить или отключить поддержку TCP-keepalive, что помогает обнаруживать разорванные соединения.
2. Журналирование и сохранение:
    * `save`: Директива `save` определяет, как часто Redis будет сохранять свою базу данных на диск. Вы можете настроить периодические точки сохранения, указав время и количество изменений данных, после которого происходит сохранение.
    * `appendonly`: Директива `appendonly` позволяет включить журналирование команд Redis для обеспечения долговременного хранения данных. Когда включена эта функция, Redis записывает все команды в файл журнала appendonly.aof, который можно использовать для восстановления данных при перезапуске Redis.
3. Ограничение по размеру строки:
    * `maxmemory-policy`: Директива `maxmemory-policy` определяет алгоритм, используемый Redis для удаления данных, когда достигнут максимальный размер памяти (установленный параметром `maxmemory`). Некоторые распространенные варианты включают LRU (наименее используемые элементы), LFU (наименее часто используемые элементы) и noeviction (не удалять данные, а возвращать ошибку при попытке добавления новых).
4. Репликация и высокая доступность:
    * `slaveof`: Директива `slaveof` позволяет настроить Redis в режим репликации, где Redis-серверы могут служить в роли мастера (primary) или слейва (replica). Это позволяет создавать резервные копии данных и повышать доступность системы.
    * `repl-diskless-sync`: Директива `repl-diskless-sync` позволяет настроить Redis для синхронизации слейвов с мастером без использования диска. Это может повысить производительность в условиях высокой нагрузки на ввод-вывод.

## Ссылки
- [Полный перечень ключевых слов с описанием](https://raw.githubusercontent.com/redis/redis/7.0/redis.conf)