# price-sentinel
Price monitor built with Scrapy: collects latest prices, checks for price drops and notifies users. 
**Still in ultra early dev phase :)**

## IMPORTANT:
- Notifiers haven't been added yet, so the application collects data, stores in a database and checks for price drops. No notifying yet.
- Only handles Amazon.com or Kabum.com.br websites. Each different website can be handled by a different spider class (see price-sentinel/spiders/)
- Handling of out-of-stock products hasn't been added, so it will probably just crash if that happens. Or maybe scrapy handles it on its own, I haven't got to that bit yet.

So..
## TODO: 
- Notifiers
- Add more websites
- Handle out-of-stock exceptions
- Let user define 


## DATABASE:
It also requires a mysql database running somewhere for storing the products. I'm currently running a local mysql database instance of mysql 
(see how to do that [here](https://hevodata.com/learn/docker-mysql/)).

## SETUP: 
The application expects the following environmental variables to work (between quotes are examples of values):
- RESOURCES_DIR="/home/user/price-sentinel/resources/"
- HOST="127.0.0.1"
- PORT="3306"
- USER="user"
- PASSWORD="password"
- DATABASE="price_sentinel"
- TABLE="products_prices"

Install the requirements with pip (highly recommend that you do that in a virtual environment - venv) with
- pip install -r requirements.txt

## RUNNING THE APPLICATION
If you've done all the setup required (has a mysql db running somewhere, created the database, added the environment variables and installed the requirements)
run the application with the following command
- python3 -m price_sentinel.runner  
Has to be done this way so python can recognize the relative imports. I'll probably dig into this issue later on.


**Just as a reminder/warning: since this project is in super early development stage, expect to encounter different issues. 
If you're cool with that, feel free to join in, help out or just ask for help :)**



