## Локальный lakehouse <br> Airflow, Trino, Iceberg, Minio и Postgres с "источником" данных

/init-source.sql - скрипт для создания заглушки источника <br>
/iceberg-catalog.properties - конфигурация айсберга <br>
/dags - DAG скрипты <br>
<br>
Запустите командой `docker-compose up -d` <br>
Проверьте данные в источнике комендой `docker exec -it source-db psql -U postgres -d postgres -c "SELECT * FROM production_daily"`<br>
Зайдите в консоль Minio по адресу <a href="localhost:9001">localhost:9001</a> (логин admin, пароль password) и создайте бакет с именем warehouse<br>
Зайдите в консоль Airflow по адресу <a href="localhost:8081">localhost:8081</a> (логин admin, пароль найдите в логах контейнера), включите DAG vitrina_refresh и дождитесь выполнения<br>
Командой `docker exec -it trino trino --execute "SELECT * FROM iceberg.default.vitrina_production_by_field;"` проверьте, есть ли данные в витрине. <br>
Ожидается (пока что это заглушка): <br>
"2026-07-14","Южное","1951.0","2026-07-18 10:16:13.992339" <br>
"2026-07-13","Северное","1453.7","2026-07-18 10:16:13.992339" <br>
"2026-07-13","Южное","1977.8","2026-07-18 10:16:13.992339" <br>
"2026-07-14","Северное","1428.8","2026-07-18 10:16:13.992339" <br>
