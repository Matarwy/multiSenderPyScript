import json
from telegram import Bot

# Load JSON file containing user data
with open('users.json') as f:
    data = json.load(f)

with open('config.json', 'r') as f:
    config = json.load(f)
    botToken = config['botToken']
    groupID = config['groupID']
    channelID = config['channelID']
    RefAirdropAmount = config['RefAirdropAmount']
    AirdropAmount = config['AirdropAmount']

new_data = []
# Initialize Telegram bot
bot = Bot(botToken)

# Check if user is a member of group or channel
print(f"Checking {len(data)} users")
for member in data:
    try:
        checkgroup = bot.get_chat_member(groupID, member['userId'])
        checkchannel = bot.get_chat_member(channelID, member['userId'])
        check = True
        if checkgroup["status"] == "left":
            print(f"User {member['name']} is not a member of the group")
            check = False
        else:
            if checkchannel["status"] == "left":
                print(f"User {member['name']} is not a member of the Channel")
                check = False
            else:
                for othermember in data:
                    if member['bep20'] == othermember['bep20']:
                        if member['userId'] != othermember['userId']:
                            print(f"User {member['name']} has the same Bep20 address as {othermember['name']}")
                            check = False
                            break
        if check:
            new_data.append(member)
    except Exception as e:
        print(e)

print(f"Total users: {len(new_data)}")

# Write new data to file
with open('usersnew.json', 'w') as f:
    for member in new_data:
        check = True
        for othermember in new_data:
            if member['ref'] == str(othermember['userId']):
                member['amount'] = RefAirdropAmount
                check = False
                break
        if check:
            member['amount'] = AirdropAmount
    json.dump(new_data, f)

