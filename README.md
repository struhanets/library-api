# City Library API

The Library project is a web application for managing library book borrowing, 
allowing users to borrow books, track their status, and manage returns. 
The system includes features such as inventory availability checks, 
automatic inventory updates when books are returned, and sending Telegram notifications 
upon the creation of a new loan. Additionally, data validation is implemented 
through model constraints and serializers to ensure data integrity and business logic consistency.

## Installation

install PostgresSQL and create db

```bash
  git clone https://github.com/struhanets/library-api.git
  cd library-api
  python -m venv venv
  source venv/bin/activate
  pip install requirements.txt
  SET POSTGRES_HOST=<your db host>
  SET POSTGRES_DB=<your db name>
  SET POSTGRES_USER=<your db username>
  SET POSTGRES_PASSWORD=<your db password>
  SET SECRET_KEY=<your secret key>
  python manage.py migrate
  python manage.py runserver
  python manage.py createsuperuser
```
## Creating a Telegram Bot:

- Open the Telegram app and search for BotFather.
- Send the command /start to begin the conversation.
- Use the command /newbot to create a new bot.
- Enter a name for the bot and a unique username (ending with bot, e.g., my_new_bot).
- After the bot is created successfully, BotFather will provide you with an API token for your bot. 
Save this token — it will be needed for connecting the bot to your project.
- To get the chat_id (the chat identifier where the bot will send messages), 
send any message to your new bot.
- Check .env.example and add the following variables.
    
## Features

- User Authentication: Secure JWT token login system.

- Book Management: Create, view, update, and delete books.

- Borrowing Management: Create, view, update borrowings.

- Book inventory feature: automatically decreases the book inventory 
when a new borrowing is created and increases it when the book is returned.

- Telegram message feature: Automatically sends a message to a Telegram bot 
when a new borrowing is created

- Swagger Documentation: Full API documentation with interactive endpoints.


## Technologies Used

**Backend:** Django REST Framework (DRF), Python 3.13

**Authentication:** JWT token

**Documentation:** Swagger (via drf-spectacular)

**Database:** PostgresSQL (or any preferred relational database)

**Containerization:** Docker

## Run with Docker

# Docker should be installed

```bash
docker-compose build
docker-compose up
```

## Getting access
- create user via api/users/
- get access token via api/users/token/
- refresh token via api/users/token/refresh