# Chat Log Server

This system is a chat log server that stores chat messages for users. It exposes several HTTP interfaces allowing other
internal services to use the logs stored in the server.

Please note that this is only an MVP(Minimum Viable Product).

## Prerequisites
* Python 3.7.3

## Steps to Set Up
1. Clone the repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate virtual environment: `source venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`
5. Migrate DB: `python manage.py migrate`
6. Run: `python manage.py runserver`

## How to Use
* Since there is no login/registration system, users can be created using Django admin commands: 
`python manage.py createsuperuser`
* To fetch all the chat logs of a user in descending order of timestamp, send a GET request to the 
`/chatlogs/<user_id>` endpoint, e.g `/chatlogs/1`. The number of chat logs returned can be modified using the `limit`
query parameter (default value 10). The `start` query parameter can be used to specify the id of the chat log from 
where to begin searching
* To create a new chat log, send a POST request to the same endpoint as above with the following fields: content,
timestamp, is_sent
* To delete all the chat logs of a user, send a DELETE request to the same endpoint as above
* To delete a single particular chat log, send a DELETE request to the `/chatlogs/<user_id>/<msg_id>` endpoint, where
msg_id is the ID of the message to be deleted