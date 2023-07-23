# scanner.py
- т.к. подразумевалось отправление POST запросов - был добавлен флаг -p (--payload) для отправки нагрузки
- я выбрал другой фреймворк для запуска сервера. http.server показался слишком усложенным для 2х простых апи

Сценарии использования
1. Root folder
`cd module_6`
2. Сканирование сети
`python ./cli/scanner.py scan -i 10.0.0.1 -n 10`
3. GET запрос 
`python ./cli/scanner.py curl -t http://numbersapi.com/07/31/date -m GET`
4. POST запрос с нагрузкой
`python ./cli/scanner.py curl -t https://jsonplaceholder.typicode.com/posts -m POST --headers Content-Type:application/json -p "{\"title\": \"Sample Post2\", \"body\": \"This is a test post.\",\"userId\": 1 }"`

# server.py

1. Сборка образа 
`docker build -t python-server .`
2. Запуск контейнера
`docker run -p 3000:3000 python-server`
3. Сканирование сети
`http://localhost:3000/scan?ip=10.0.0.1&num_of_host=1`
4. Проксирование GET
`http://127.0.0.1:3000/sendHttp`
body:
{
    "target": "http://numbersapi.com/07/31/date"
}
5. Проксирование POST
`http://127.0.0.1:3000/sendHttp`
body: 
{
    "target": "https://jsonplaceholder.typicode.com/posts",
    "method": "POST",
    "headers": "Content-Type:application/json",
    "payload": "{\"title\": \"Sample Post2\", \"body\": \"This is a test post.\",\"userId\": 1 }"
}