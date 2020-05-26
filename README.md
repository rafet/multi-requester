# multireq
`multireq` is a python package that helps you to send multiple requests simultaneously and secretly.

## Installation
```
pip install multireq
```

## Simple Usage

```python
import multireq

mr = multireq.multiRequester(use_proxy=True)

urls = [
    "https://jsonplaceholder.typicode.com/todos/1",
    "https://jsonplaceholder.typicode.com/todos/2",
    "https://jsonplaceholder.typicode.com/todos/3"
]

responses = mr.get_many(urls)

for response in responses:
    print(response.json()['title'])

```
### Output
```
delectus aut autem
quis ut nam facilis et officia qui
fugiat veniam minus
```
<hr>

If you don't want to use proxies, you can simply set the `use_proxy`  to False. When you use a proxy, requests can be so slow. However, sometimes you have to hide your identity when you send requests. If you don't have privacy issues, don't use the proxy and send requests faster.
```python
mr = multireq.multiRequester(use_proxy=False)
```
<hr>

Also, you can send just one request.
```python
response = mr.get(url)
```