import datetime
from firebase_config import ibaelia_db
from dateutil.parser import parse
import discord


def get_scores_by_id(user_id, guild, limit=10):
    all_scores = ibaelia_db.child("scores").order_by_child("time").get().val()
    if all_scores is None:
        return []
    list_scores = [score for score in list(all_scores.values()) if score["user_id"] == user_id][
                  ::-1][:limit]
    return list_scores


def get_scores_by_time(time, guild):
    final_scores = []
    all_scores = ibaelia_db.child("scores").order_by_child("score").get().val()
    if all_scores is None:
        return []
    list_scores = [score for score in list(all_scores.values()) if
                   score['time'].split(" ")[0] == time]
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
    week_array = [(today + datetime.timedelta(days=i)).date() for i in
                  range(-1 - today_date, 6 - today_date)]
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


def format_scoreboard_embed(embed, scores):
    digits = {4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}

    # I don't know if creating the discord.File object is necessary to get the icon url?
    crossword_icon = "crossword_images//crossword_icon.jpg"
    discord.File(crossword_icon, filename="image.jpg")
    embed = embed.set_thumbnail(url="attachment://image.jpg")

    # The first field will be the current leader shout out
    current_leader_name = "---------------:small_blue_diamond: CURRENT LEADER :small_blue_diamond:---------------"
    current_leader_value = "\n"
    leader = scores[0]["name"].split("#")[0]
    # Compute the number of tabs to offset the name by based on name length
    name_length = len(leader)
    num_tabs = round((42 - (name_length + 2)) / 4.)
    current_leader_value += "```ini\n>\u009b" * num_tabs
    current_leader_value += f"[{leader}]\u009b\u009b\u009b\u009b\u009b<```"
    # Add bottom border
    current_leader_value += "\n" + ("=" * 42)
    embed.add_field(name=current_leader_name, value=current_leader_value, inline=False)

    # Add blank field for spacing
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    # First place gets a special trophy as well
    time = f"```fix\n{scores[0]['score']}```\n"
    embed.add_field(name=f":first_place: \u009b{scores[0]['name']}", value=time,
                    inline=True)
    embed.add_field(name="\u200b \u200b \u200b :trophy:", value="\u200b", inline=True)

    for idx in range(len(scores)):
        if idx == 0:
            # Already did first place
            continue
        elif idx == 1:
            placement = ":second_place:"
            time = f"```python\n{scores[idx]['score']}```\n"
        elif idx == 2:
            placement = ":third_place:"
            time = f"```python\n{scores[idx]['score']}```\n"
        elif idx < 9:
            placement = f":{digits[idx + 1]}:"
            time = f"```{scores[idx]['score']}```\n"
        else:
            placement = f"{idx + 1}."
            time = f"```{scores[idx]['score']}```\n"

        # We use inline to shorten the code block width
        embed.add_field(name=f"{placement} \u009b{scores[idx]['name']}", value=time,
                        inline=True)
        # Add blank field for second column
        embed.add_field(name="\u200b", value="\u200b", inline=True)

    embed.timestamp = datetime.datetime.now()
    embed = embed.set_footer(text=f"uwu wowow {leader} senpai is so sugoiiii")

    # Footer image
    crossword_icon = "ibaelia_images//wow_irelia.jpg"
    discord.File(crossword_icon, filename="image.jpg")
    embed = embed.set_image(url="attachment://image.jpg")

    return embed
