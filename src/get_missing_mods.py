import bapi
import json
import pathlib

## Load Authorization ##
authPath = pathlib.Path(__file__).resolve(
).parent.parent.joinpath('config', 'auth.json')

with authPath.open() as f:
    authDict = json.loads(f.read())
    f.close()

## Load User Info ##
userPath = pathlib.Path(__file__).resolve(
).parent.parent.joinpath('output', 'memberData.json')

with userPath.open() as f:
    userList = json.loads(f.read())
    f.close()

## Load Mod Sales ##
salePath = pathlib.Path(__file__).resolve(
).parent.parent.joinpath('output', 'mods.json')

with salePath.open() as f:
    saleList = json.loads(f.read())
    f.close()

## Request Collections ##
for u in userList:
    collections_request = bapi.request_user_collections(user=u, authorization=authDict)
    u['collections'] = json.loads(collections_request.content)['Response']['profileCollectibles']['data']['collectibles']

## Translate
for s in saleList:
    s['ping_list'] = list()
    for u in userList:
        if (userList[0]['collections'][str(s['collections_hash'])]['state'] % 2) == 1:
            s['ping_list'].append(u['discord_id'])
            u['discord_id']

## Write Sale/Ping Information to JSON file ##
pingsPath = pathlib.Path(__file__).resolve(
).parent.parent.joinpath('output', 'pings.json')

with pingsPath.open('w') as f:
    json.dump(saleList, f)
    f.close()