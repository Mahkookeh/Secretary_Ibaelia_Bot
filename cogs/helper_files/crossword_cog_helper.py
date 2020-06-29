import datetime
from firebase_config import ibaelia_db
from dateutil.parser import parse


def get_scores_by_id(user_id, guild, limit=10):
    all_scores = ibaelia_db.child("scores").order_by_child("time").get().val()
    if all_scores is None:
        return []
    list_scores = [score for score in list(all_scores.values()) if score["user_id"] == user_id][::-1][:limit]
    return list_scores

def get_scores_by_time(time, guild):
    final_scores = []
    all_scores = ibaelia_db.child("scores").order_by_child("score").get().val()
    if all_scores is None:
        return []
    list_scores = [score for score in list(all_scores.values()) if score['time'].split(" ")[0] == time]
    for score in list_scores:
        user = ibaelia_db.child("users").order_by_child("id").equal_to(score["user_id"]).get().val()
        user_vals = list(user.values())[0]
        if guild in user_vals['guilds']:
            final_scores.append(score)
    return final_scores


def check_date(time):
    correctDate = None
    try:
        year, month, day = map(int, time.split("-"))
        newDate = datetime.datetime(year, month, day)
        correctDate = True
    except ValueError:
        correctDate = False
    return correctDate


def get_current_week(time):
    today = parse(time)
    today_date = today.weekday()
    week_array = [(today + datetime.timedelta(days=i)).date() for i in range(-1 - today_date, 6 - today_date)]
    named_days_array = [day.strftime('%A') for day in week_array]
    week_dict = dict(zip(named_days_array, week_array))
    print(week_dict)
    return week_array



def push_score(user_id, username, score, time, guild):
    # get users
    # check time
    # if user not in users list, create new user
    # add to scores
    ids = add_user_to_database(user_id, username, guild)
    add_to_server(user_id, guild, ids)

    valid, prev_score = is_valid_score(user_id, username, score, time, guild)    
    if valid:
        new_score = {
            "user_id": user_id,
            "name": username,
            "score": score,
            "time": time,
            "guild": guild
        }
        ibaelia_db.child("scores").push(new_score)
    return [valid, prev_score]

def add_user_to_database(user_id, username, guild):
    all_users = ibaelia_db.child("users").get()  
    all_users_vals = all_users.val() 
    ids = []
    if all_users_vals:
        for user in all_users.each():
            ids.append(user.val()['id'])
    if user_id not in ids:
        new_user = {
            "id": user_id,
            "name": username,
            "guilds": [guild]
        }
        ibaelia_db.child("users").push(new_user)
    return ids

def add_to_server(user_id, guild, ids):    
    if user_id in ids:
        curr_user = ibaelia_db.child("users").order_by_child("id").equal_to(user_id).get()
        curr_user_vals = list(curr_user.val().values())[0]
        curr_user_key = curr_user.each()[0].key()
        if guild not in curr_user_vals['guilds']:
            guilds = curr_user_vals['guilds']
            guilds.append(guild)
            ibaelia_db.child("users").child(curr_user_key).update({'guilds': guilds})


def is_valid_score(user_id, username, score, time, guild):
    all_scores = ibaelia_db.child("scores").order_by_child("time").get().val()
    if all_scores is None:
        return [True, None]
    list_scores = [score for score in list(all_scores.values()) if score["user_id"] == user_id]
    for score in list_scores:
        if score['time'].split(" ")[0] == time.split(" ")[0]:
            return [False, score['score']]
    return [True, None]