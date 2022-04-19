from django.shortcuts import render

import pymongo, pusher

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb')

todos_db = client['todos-backend']

todos_collection = todos_db['todos']

todos = []

for obj in todos_collection.find({}):
    todos.append(obj)

print(todos)

pusher_client = pusher.Pusher(
  app_id='1388554',
  key='f00c4ec7239d17757971',
  secret='4ad7cbcf6b3ba6e99a1c',
  cluster='ap1',
  ssl=True
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})


def index(request):
    context = {
        'todos': todos
    }
    return render(request, 'index.html', context)
