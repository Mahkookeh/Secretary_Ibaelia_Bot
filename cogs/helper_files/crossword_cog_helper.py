import datetime
from firebase_config import ibaelia_db
from dateutil.parser import parse
import discord


def get_scores_by_id(user_id, guild, time, limit=7):
    dates = get_past_num_days(time, limit)[::-1]
    
    final_scores = {key:None for key in dates}

    all_scores = ibaelia_db.child("scores").order_by_child("time").get().val()
    if all_scores is None:
        return final_scores
    list_scores = [score for score in list(all_scores.values()) if score["user_id"] == user_id][::-1][:limit]
    print(list_scores)





    
    # Check if a score's date is in the date array
    # If so, add score to score list
    # If not, then add None to score list

    count = 0
    for score_idx in range(count, len(list_scores)):
        for date in dates:
            print(f"date: {date} | score date: {list_scores[score_idx]['time'].split(' ')[0]}")
            if list_scores[score_idx]["time"].split(" ")[0] == str(date):
                final_scores[date] = list_scores[score_idx]
                count += 1
                break
    print(final_scores)

    return final_scores


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


def get_past_num_days(time, num):
    today = parse(time)
    week_array = [(today + datetime.timedelta(days=i)).date() for i in range(num * -1, 0)]
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
    files = []
    digits = {4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}

    # I don't know if creating the discord.File object is necessary to get the icon url?
    crossword_icon = "crossword_images/crossword_icon.jpg"
    file = discord.File(crossword_icon, filename="crossword_icon.jpg")
    files.append(file)
    embed = embed.set_thumbnail(url="attachment://crossword_icon.jpg")

    # The first field will be the current leader shout out
    current_leader_name = "-------------------:small_blue_diamond: CURRENT LEADER :small_blue_diamond:-------------------"
    current_leader_value = "\n"
    if len(scores) != 0:
        leader = scores[0]["name"].split("#")[0]
        leader_fullname = scores[0]["name"]
    else:
        leader = "no_one"
        leader_fullname = "no_one#rip"
    # Compute the number of tabs to offset the name by based on name length
    name_length = len(leader)
    num_tabs = round((38 - (name_length + 2)) / 4.)
    current_leader_value += "```ini\n>" + "  " * num_tabs
    current_leader_value += f"[{leader}]" + "  " * num_tabs + "<```"
    # Add bottom border
    current_leader_value += "\n" + ("=" * 41)
    embed.add_field(name=current_leader_name, value=current_leader_value, inline=False)

    # Add blank field for spacing
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    # First place gets a special trophy as well
    if len(scores) != 0:
        time = f"```fix\n{scores[0]['score']}```\n"
    else:
        time = "```fix\ninfinity```\n"
    embed.add_field(name=f":first_place: \u2003{leader_fullname}", value=time,
                    inline=True)
    embed.add_field(name=":trophy:", value="\u200b", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)

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
        embed.add_field(name=f"{placement} \u2003{scores[idx]['name']}", value=time,
                        inline=True)
        # Add blank field for other columns
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)

    embed.timestamp = datetime.datetime.now()
    embed = embed.set_footer(text=f"uwu wowow {leader} senpai is so sugoiiii")

    # Footer image
    crossword_icon = "ibaelia_images/wow_irelia.jpg"
    file = discord.File(crossword_icon, filename="wow_irelia.jpg")
    files.append(file)
    embed = embed.set_image(url="attachment://wow_irelia.jpg")

    return files, embed
