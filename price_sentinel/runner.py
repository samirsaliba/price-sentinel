from .notifiers.telegram_bot import TelegramNotifier
from .notifiers.email import EmailNotifier
import os
import pandas as pd
import pymysql
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from .spiders.amazon import AmazonSpider
from .spiders.kabum import KabumSpider

from twisted.internet import reactor


PRICE_INTERVAL = 90  # in days
DROP_FROM_MEAN_THRESHOLD = 0.9

NOTIFIERS = [EmailNotifier, TelegramNotifier]


class PriceSentinel():
    def __init__(self):
        self.HOST = os.environ["HOST"]
        self.USER = os.environ["USER"]
        self.PASSWORD = os.environ["PASSWORD"]
        self.DATABASE = os.environ["DATABASE"]
        self.TABLE = os.environ["TABLE"]
        self.PORT = os.getenv('PORT', None)
        self.notifications = []
        if self.PORT is not None:
            self.PORT = int(self.PORT)

        self.create_connection()

    def create_connection(self):
        self.conn = pymysql.connect(host=self.HOST,
                                    user=self.USER,
                                    password=self.PASSWORD,
                                    database=self.DATABASE,
                                    port=self.PORT)
        self.cursor = self.conn.cursor()

    def scrape(self):
        configure_logging()
        settings = get_project_settings()
        runner = CrawlerRunner(settings)
        runner.crawl(AmazonSpider)
        runner.crawl(KabumSpider)
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()   # the script will block here until
        # all crawling jobs are finished

    def check_price_drop_item(self, product_name):
        historic_values_sql = f"""
        SELECT *
        FROM {self.DATABASE}.{self.TABLE}
        WHERE `timestamp` >= (DATE(NOW()) - INTERVAL {PRICE_INTERVAL} DAY)
        AND CAST(`timestamp` AS date) < (
            SELECT CAST(max(`timestamp`) AS date) 
            FROM {self.DATABASE}.{self.TABLE} 
        )
        AND `name` = %(name)s ;
        """
        historic_df = pd.read_sql(sql=historic_values_sql,
                                  params={"name": product_name},
                                  con=self.conn,
                                  parse_dates=["timestamp"])

        historic_df["day"] = historic_df["timestamp"].dt.date
        min_mean = historic_df[["day", "price"]]\
            .sort_values(by=['day', 'price'], ascending=True)\
            .drop_duplicates(subset=['day'])["price"]\
            .mean()
        historic_min = historic_df["price"].min()

        last_values_sql = f"""
        SELECT *
        FROM {self.DATABASE}.{self.TABLE}
        WHERE CAST(`timestamp` AS date) = (
            SELECT CAST(max(`timestamp`) AS date) 
            FROM {self.DATABASE}.{self.TABLE} 
        )
        """
        df = pd.read_sql(sql=last_values_sql,
                         con=self.conn,
                         parse_dates=["timestamp"])
        df["day"] = df["timestamp"].dt.date
        last_min = df["price"].min()

        retailers = df[df["price"] == last_min]["retailer"].values

        if (last_min < historic_min)\
                or (last_min < DROP_FROM_MEAN_THRESHOLD * min_mean):

            notification = {
                "product": product_name,
                "price": last_min,
                "mean_of_period": min_mean,
                "historic_min": historic_min,
                "retailers": retailers
            }
            self.notifications.append(notification)

    def check_price_drop(self):
        products_names_df = pd.read_sql(
            sql=f"""
            SELECT DISTINCT `name`
            FROM {self.DATABASE}.{self.TABLE}
            WHERE `timestamp` >= (DATE(NOW()) - INTERVAL {PRICE_INTERVAL} DAY);
            """,
            con=self.conn
        )

        products_names = products_names_df["name"].tolist()

        for prod_name in products_names:
            self.check_price_drop_item(prod_name)

    def notify(self):
        for Notifier in NOTIFIERS:
            notifier_object = Notifier()
            notifier_object.notify(self.notifications)


if __name__ == '__main__':
    price_sentinel = PriceSentinel()
    price_sentinel.scrape()
    price_sentinel.check_price_drop()
    price_sentinel.notify()
