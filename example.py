import multireq

mr = multireq.multiRequester(use_proxy=True)

urls = [
    "https://jsonplaceholder.typicode.com/todos/1",
    "https://jsonplaceholder.typicode.com/todos/2",
    "https://jsonplaceholder.typicode.com/todos/3"
]

results = mr.get_many(urls)

for i in results:
    print(i.json()['title'])