from django.shortcuts import render

import time
import pymongo
import pusher

client = pymongo.MongoClient(
    'mongodb+srv://grenkiat:grenkiat@root-cluster.zi16t.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db = client['cluster']

test_collection = db['test']

tasks = []

for obj in test_collection.find({}):
    tasks.append(obj)

print(tasks)

pusher_client = pusher.Pusher(
    app_id='1388554',
    key='f00c4ec7239d17757971',
    secret='4ad7cbcf6b3ba6e99a1c',
    cluster='ap1',
    ssl=True
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})

pipeline = [{'$match': {'operationType': 'update'}}]

# cursor = db.inventory.watch()
# document = pymongo.next(cursor)
# resume_token = cursor.resume_token
# cursor = test_collection.watch(resume_after=resume_token)
# document = pymongo.next(cursor)

# with test_collection.watch() as stream:
#     while stream.alive:
#         change = stream.try_next()
#         # Note that the ChangeStream's resume token may be updated
#         # even when no changes are returned.
#         print("Current resume token: %r" % (stream.resume_token,))
#         if change is not None:
#             print("Change document: %r" % (change,))
#             continue
#         # We end up here when there are no recent changes.
#         # Sleep for a while before trying again to avoid flooding
#         # the server with getMore requests when no changes are
#         # available.
#         time.sleep(10)

# try: 
#     resume_token = None
#     with test_collection.watch(pipeline=pipeline) as stream:
#         for insert_change in stream:
#             print(insert_change)
#             resume_token = stream.resume_token

# except pymongo.errors.PyMongoError:
#     # The ChangeStream encountered an unrecoverable error or the
#     # resume attempt failed to recreate the cursor.
#     if resume_token is None:
#         # There is no usable resume token because there was a
#         # failure during ChangeStream initialization.
#         print('resume token is none')
#     else:
#         # Use the interrupted ChangeStream's resume token to create
#         # a new ChangeStream. The new stream will continue from the
#         # last seen insert change without missing any events.
#         with test_collection.watch(
#                 pipeline, resume_after=resume_token) as stream:
#             for insert_change in stream:
#                 print(insert_change)
with test_collection.watch() as stream:
    while stream.alive:
        change = stream.try_next()
        # Note that the ChangeStream's resume token may be updated
        # even when no changes are returned.
        if change is not None:
            print("Change document: %r" % (change,))
            pusher_client.trigger('my-channel', 'my-event', {"data": change.fullDocument})
            continue
        # We end up here when there are no recent changes.
        # Sleep for a while before trying again to avoid flooding
        # the server with getMore requests when no changes are
        # available.
        time.sleep(10)

def index(request):
    context = {
        'tasks': tasks
    }
    
    return render(request, 'index.html', context)
    