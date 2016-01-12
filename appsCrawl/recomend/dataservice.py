__author__ = 'zhengyiwang'
from pymongo import MongoClient
import random
import json

class DataService(object):
    @classmethod
    def init(cls, client):
        cls.client = client
        cls.db = client.appstore2
        cls.user_download_history = cls.db.user_download_history
        cls.app_info = cls.db.app_info

    @classmethod
    def retrieve_user_download_history(cls, filter_dict={}):
        #return a dictP{user_id: download_history}
        #return all data int the collection if no filter is specified

        #print "retrive user download history"

        result = {}
        cursor = cls.user_download_history.find(filter_dict)
        for user_download_history in cursor:
            uid = user_download_history['user_id']
            result[uid] = user_download_history['download_history']
        return result

    @classmethod
    def retrieve_app_info(cls, filter_dict = {}):
        #print "retriving app info --------------"
        result = {}
        cursor = cls.app_info.find(filter_dict)
        for appinfo in cursor:

            appid = appinfo['app_id']
            title = appinfo['title']
            result[appid] = {'title' :title}
        return result



    @classmethod
    def update_app_info(cls, filter_dict, update):
        cls.app_info.update_one(filter_dict, update, True)

    @classmethod
    def update_user_info(cls, filter_dict, update):
        cls.user_download_history.update_one(filter_dict, update, True)

    @classmethod
    def insert_data(cls, collection, filename):
        print "inserting data........."
        c = cls.user_download_history
        if collection == "app_info":
            c = cls.app_info

        fin = open(filename, 'r')
        for line in fin:
            print line
            item = json.loads(line)

            print item

            c.insert(item)



