__author__ = 'zhengyiwang'

import time
from pymongo import MongoClient
from dataservice import DataService
import os

def main():
    start = time.clock()
    try:
        #get MongoDB client and set it in DataService
        client = MongoClient('localhost', 27017)
        DataService.init(client)

        f_app = '../../data/app_info.json'
        f_history = '../../data/user_download_history.json'
        print f_history
        print f_app


        DataService.insert_data("app_info", f_app)
        DataService.insert_data("", f_history)


    except Exception as e:
        print(e)
    finally:
        #clean up
        if 'client' in locals():
            client.close()
        end = time.clock()
        print end - start

if __name__ == "__main__":
    main()


