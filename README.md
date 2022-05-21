# price-sentinel
Price monitor built with Scrapy: collects latest prices, checks for price drops and notifies users. 
**Still in ultra early dev phase :)**

## IMPORTANT:
- Notifiers haven't been added yet, so the application collects data, stores in a database and checks for price drops. No notifying yet.
- Only handles Amazon.com or Kabum.com.br websites. Each different website is handled by a different spider class (see price-sentinel/spiders/), so one can add more spiders to handle other websites.
- Handling of out-of-stock products hasn't been added, so it will probably just crash if that happens. Or maybe scrapy handles it on its own, I haven't got to that bit yet.

So..
## TODO: 
- Notifiers
- Add more websites
- Handle out-of-stock exceptions
- Let user define 


## DATABASE:
The application requires a mysql database running somewhere for storing the products. I'm currently running a local mysql instance (see how to do that [here](https://hevodata.com/learn/docker-mysql/)). It also expects the database to be already created (not the table, it will create it).

## SETUP: 
The application expects the following environment variables to work (between quotes are examples of values):
- RESOURCES_DIR="/home/user/price-sentinel/resources/"
- DB_HOST="127.0.0.1"
- DB_PORT="3306"
- DB_USER="user"
- DB_PASSWORD="password"
- DB_DATABASE="price_sentinel"
- DB_TABLE="products_prices"

For the Telegram Notifier, please refer to the Telegram documentation on how to create 
your own Telegram Bot [here](https://core.telegram.org/bots#6-botfather). Then, refer to the script utils/telegram_get_chat_id.py to get your telegram chat_id (so the Bot can find you). Finally, set tthe following envinroment variables:
- TELEGRAM_TOKEN="your-bot-token"
- TELEGRAM_CHAT_ID="your-chat-id"

For the Email Notifier, the following variables must be set (between quotes are also examples):
- EMAIL_SMTP="smtp.gmail.com"
- EMAIL_FROM="bot@gmail.com"
- EMAIL_USER="bot@gmail.com"
- EMAIL_TO="user@gmail.com"
- EMAIL_PORT="587"
- EMAIL_PASSWORD="password"

PS. For Gmail, you should create an App Password -- normal user password won't work. Please refer to [this article](https://support.google.com/accounts/answer/185833?hl=en) from Google on how to do that.

Install the requirements with pip (highly recommend that you do that in a virtual environment - venv) with
- pip install -r requirements.txt

## RUNNING THE APPLICATION
If you've done all the setup required (has a mysql db running somewhere, created the database, added the environment variables and installed the requirements)
run the application with the following command
- python3 -m price_sentinel.runner  
Has to be done this way so python can recognize the relative imports. I'll probably dig into this issue later on.


**Just as a reminder/warning: since this project is in super early development stage, expect to encounter different issues. 
If you're cool with that, feel free to join in, help out or just ask for help :)**



