# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.utils.project import get_project_settings
from .items import LogrocketArticleItem

from dataclasses import asdict

settings = get_project_settings()

class MongoDBPipeline:
    def __init__(self):
        conn = pymongo.MongoClient(
            settings.get('MONGO_HOST'),
            settings.get('MONGO_PORT')
        )
        db = conn[settings.get('MONGO_DB_NAME')]
        self.collection = db[settings['MONGO_COLLECTION_NAME']]

    def process_item(self, item, spider):
        if isinstance(item, LogrocketArticleItem): # article item
            self.collection.update({"_id": item._id}, asdict(item), upsert = True)
        else:
            comments = []
            for comment in item.get("comments"):
                comments.append(asdict(comment))
            self.collection.update({"_id": item.get("article_id")}, {"$set": {"comments": comments} }, upsert=True)

        return item

