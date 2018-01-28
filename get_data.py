import twitter
import sys
import os
import csv
import gzip
import copy
import cPickle as pickle
from config import *

def get_follower_list(username):
    # Return a list of user_ids that followed this username. Makes as many calls 
    # to the Twitter API as necessary (returns the full list of followers, not 
    # just the results of the first returned page).
     
    api = twitter.Api(consumer_key = consumer_key,
                      consumer_secret = consumer_secret,
                      access_token_key = access_token_key,
                      access_token_secret = access_token_secret,
                      sleep_on_rate_limit = True)

    return(api.GetFollowerIDs(screen_name = username))

def get_follower_info(user_id_list):
    # Return the account creation time for every user_id in user_id_list. The 
    # return format is a list of lists: [[user_id1, date1, n_tweets1], 
    # [user_id2, date2, n_tweets2], ...].
    
    api = twitter.Api(consumer_key = consumer_key,
                      consumer_secret = consumer_secret,
                      access_token_key = access_token_key,
                      access_token_secret = access_token_secret,
                      sleep_on_rate_limit = True)

    # Need to do it manually in chunks of 100 users, the API doesn't split the 
    # list. See this issue: https://github.com/bear/python-twitter/issues/523
    csize = 100
    res = []
    user_id_list_chunks = [user_id_list[i:i+csize] \
                           for i in range(0, len(user_id_list), csize)]

    for chunk in user_id_list_chunks:
        partial = api.UsersLookup(chunk)
        partial = [[user.id, copy.copy(user.created_at), user.statuses_count] for user in partial]
        res += partial

    return(res)


if __name__ == "__main__":

    username = sys.argv[1]
    print "Will get followers for {}".format(username)

    flist = get_follower_list(username)
    print "Obtained {} followers".format(len(flist))

    # Use cache for this. Many users will have repeated followers, no need to 
    # keep getting information for those, just use a local dictionary (and save 
    # it every time).
    if os.path.isfile("users_cache.pickle"):
        with open("users_cache.pickle", "r") as f_in:
            cache = pickle.load(f_in)
    else:
        cache = dict()

    need_info_list = [str(user_id) for user_id in flist if user_id not in cache]
    if len(need_info_list) > 10: # put a lower limit on this
        print "Need to get information from {} followers, rest in cache"\
                .format(len(need_info_list))

        new_users = get_follower_info(need_info_list)

        for new_user in new_users:
            cache[new_user[0]] = (new_user[1], new_user[2])
    else:
        print "Have all info in cache already"

    # Save dictionary after it's been updated
    with open("users_cache.pickle", "wb") as f_out:
        pickle.dump(cache, f_out)

    # Now simply save the CSV file for the requested user_name. Don't forget 
    # that the original `flist` array is ordered (the most recent follower comes 
    # first, so we can use this to add another column with the proper ordering).
    # Also, apparently some user_ids are not returned. Remove them from the 
    # original list.
    flist = [user_id for user_id in flist if user_id in cache]
    n_order = len(flist)
    with gzip.open("{}.csv.gz".format(username), "wb") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['id', 'created_at', 'statuses_count', 'order'])
        for user_id in flist:
            dd = cache[user_id]
            writer.writerow([user_id, dd[0], dd[1], n_order])
            n_order -= 1
