import json, pymongo

class DataOutput:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017')

    def process_item(self, item):
        db = self.client.Dang
        collection = db.dang
        if collection.find({'product_id': item['product_id']}):
            collection.update({'product_id': item['product_id']}, {'$set': item})
        else:
            collection.insert(item)
        print('存储结果： %s' % str(item))

    def process_close(self):
        self.client.close()