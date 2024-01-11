#arbitrary thread
a thread has been created and stored in the database.  big step. we can view the thread_id by first creating a thread if there isn't one, storing the thread.id value in db with `db.create_thread_id(thread.id)` then we pull that stored value
or we use `existing_thread_id` to check db for most recently added thread with `db.get_thread_id()`
#add message
from where? why would I add a message through this method as opposed to any other method of interacting with the assistants api?
the vision is that this is not just another chatbot interface and powerful, impressive tools can be made with FastUI
#message storage, retrieval and transformation
messages are stored within thread ids.  does that mean the database does not need to be responsible for storing messages?  maybe, but probably not.
utilization of message data necessitates transformation to another data type, storage in a db and retrieval
##transformation
for display-displaying a model response doesn't necessitate transformation out of json format, neither does chaining model output into another's input.
But eventually, our use case will necessitate the transformation of message formatted JSON data into another form
###copy-paste
Though I'd like to avoid it wherever possible, copy-paste is the first transformation that comes to mind.
###use-case
model architecture for creating FastUI documentation
