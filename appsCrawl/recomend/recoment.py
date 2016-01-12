__author__ = 'zhengyiwang'

from pymongo import MongoClient
from dataservice import DataService
import operator
import math
import time

class Helper(object):
    @classmethod
    def cosine_similarity(cls, app_list1, app_list2):
        #print "calcuating cosine similarity"
        return float(cls.__count_match(app_list1, app_list2))/(math.sqrt(len(app_list2)*len(app_list1)))

    @classmethod
    def __count_match(cls, list1, list2):
        #print "count match"
        count = 0
        for element in list1:
            if element in list2:
                count += 1
        return count


def calculate_top_5(app, user_download_history):
    #create a dict to store each app and its similarity to this app
    app_similary = {}

    for apps in user_download_history:
        #calculate similarity

        similarity = Helper.cosine_similarity([app], apps)
        for other in apps:
            if app_similary.has_key(other):
                app_similary[other] += similarity
            else:
                app_similary[other] = similarity

    #there could be app without related apps, which means not in any download history
    if not app_similary.has_key(app):
        return

    app_similary.pop(app)
    sorted_tops = sorted(app_similary.items(), key = operator.itemgetter(1), reverse = True)
    top_5_app = []
    count = 0
    for item,sim in sorted_tops:
        count += 1

        top_5_app.append(item)
        if count >= 5:
            break

    print "top 5 for  " + app + " is \t" + str(top_5_app)

    #store in MongoDB
    DataService.update_app_info({'app_id':app},{'$set':{'top_5_app':top_5_app}})

def top_5_for_user(userid, all_history):
    #print all_history
    print "caluate top 5 for user"

    user_download_history = all_history[userid]
    #print user_download_history

    list_similarity = {}
    for id in all_history.keys():
        similarity = Helper.cosine_similarity(user_download_history, all_history[id])
        #print "good here"
        list_similarity[id] = similarity

    list_similarity.pop(userid)
    print "sort all lists"
    sorted_tops = sorted(list_similarity.items(), key = operator.itemgetter(1), reverse = True)
    print sorted_tops

    print "top apps in top 10 lists"
    apps_in_top_list = {}
    for i in range(10):
        if i >= len(sorted_tops):
            break
        list = all_history[sorted_tops[i][0]]
        print "top 10 lists---------"
        print list
        for app in list:
            if app in apps_in_top_list.keys():
                apps_in_top_list[app] += 1
            else:
                apps_in_top_list[app] = 1
    print "sort top apps"
    sorted_apps = sorted(apps_in_top_list.items(), key = operator.itemgetter(1), reverse = True)
    count = 0
    top_5_app = []
    print "select top 5 "
    for item,sim in sorted_apps:
        count += 1

        top_5_app.append(item)
        if count >= 5:
            break

    print "top 5 for  " + str(userid) + " is \t" + str(top_5_app)
    DataService.update_user_info({'user_id':userid},{'$set':{'top_5_app':top_5_app}})

def recomend_for_user():
    start = time.clock()

    try:
        #get MongoDB client and set it in DataService
        client = MongoClient('localhost', 27017)
        DataService.init(client)
        all_userinfo = DataService.retrieve_user_download_history()

        for userid in all_userinfo.keys():
            top_5_for_user(userid, all_userinfo)

    except Exception as e:
        print(e)
    finally:
        #clean up
        if 'client' in locals():
            client.close()
        end = time. clock()
        print "time spend is ---------------    "
        print str(end - start)



def related_apps():
    start = time.clock()

    try:
        #get MongoDB client and set it in DataService
        client = MongoClient('localhost', 27017)
        DataService.init(client)
        all_apps = DataService.retrieve_app_info()

        user_download_history = DataService.retrieve_user_download_history()
        for app in all_apps.keys():
            calculate_top_5(app, user_download_history.values())
    except Exception as e:
        print(e)
    finally:
        #clean up
        if 'client' in locals():
            client.close()
        end = time. clock()
        print "time spend is ---------------    "
        print str(end - start)

if __name__ == "__main__":
    recomend_for_user()




