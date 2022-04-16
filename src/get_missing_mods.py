import bapi
import json
import pathlib

rootDir = pathlib.Path(__file__).resolve().parent.parent

## Load Authorization ##
authPath = rootDir.joinpath('config', 'auth.json')

with authPath.open() as f:
    authDict = json.loads(f.read())
    f.close()

## Load User Info ##
userPath = rootDir.joinpath('output', 'memberData.json')
with userPath.open() as f:
    userList = json.loads(f.read())
    f.close()

## Load Mod Sales ##
salePath = rootDir.joinpath('output', 'mods.json')
with salePath.open() as f:
    saleList = json.loads(f.read())
    f.close()

## Request Collections ##
for u in userList:
    collections_request = bapi.request_user_collections(user=u, authorization=authDict)
    u['collections'] = json.loads(collections_request.content)['Response']['profileCollectibles']['data']['collectibles']

## Translate
for item in saleList:
    item['ping_list'] = list()
    for user in userList:
        if (userList[0]['collections'][str(item['collections_hash'])]['state'] % 2) == 1:
            item['ping_list'].append(user['discord_id'])

## Write Sale/Ping Information to JSON file ##
pingsPath = rootDir.joinpath('output', 'pings.json')

with pingsPath.open('w') as f:
    json.dump(saleList, f)
    f.close()