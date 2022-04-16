import bapi
import json
import pathlib
import argparse

## Handle Command Line Arguments
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-b", "--bungie", help="Bungie Name 'ABCD#1234'")
parser.add_argument("-d", "--discord", help = "Discord Unique ID")
args = vars(parser.parse_args())

bungiename = args['bungie']
discordID = args['discord']

## Load Authorization ##
authPath = pathlib.Path(__file__).resolve(
).parent.parent.joinpath('config', 'auth.json')

with authPath.open() as f:
    authDict = json.loads(f.read())
    f.close()

## Request User Info ##
new_user = bapi.request_bungie_user(bungiename=bungiename, authorization=authDict)

user_data = {
        "discord_id": discordID,
        "destiny_membership_id" : new_user['destinyMemberships'][0]['membershipId'],
        "destiny_membership_type" : str(new_user['destinyMemberships'][0]['membershipType']),
        "bungie_name": bungiename
    }

## Write User Information to JSON file ##
memberDataPath = pathlib.Path(__file__).resolve(
).parent.parent.joinpath('output', 'memberData.json')

with memberDataPath.open() as f:
    users = json.load(f)

users.append(user_data)
with memberDataPath.open('w') as f:
    json.dump(users, f)
    f.close()