import bapi
import json
import pathlib

## Load Authorization Info ##
authPath = pathlib.Path(__file__).resolve(
).parent.parent.joinpath('config', 'auth.json')

with authPath.open() as f:
    authDict = json.loads(f.read())
    f.close()

## Load Script Config ##
configPath = pathlib.Path(__file__).resolve(
).parent.parent.joinpath('config', 'config.json')

with configPath.open() as f:
    configDict = json.loads(f.read())
    f.close()

## Load Item Definitions ##
itemDefsPath = pathlib.Path(__file__).resolve(
).parent.parent.joinpath('data', 'DestinyInventoryItemLiteDefinition-cb4bec6f-e2b6-4f44-8593-cfd0255b89f2.json')

with itemDefsPath.open(encoding="utf-8") as f:
    itemDefsDict = json.loads(f.read())
    f.close()

responsePath = pathlib.Path(__file__).resolve(
).parent.parent.joinpath('config', 'response.json')

## Refresh Tokens ##
new_tokens = json.loads(bapi.request_new_tokens(
    authorization=authDict).content)

authDict['access_token'] = new_tokens['access_token']
authDict['refresh_token'] = new_tokens['refresh_token']

with authPath.open('w') as f:
    json.dump(authDict, f)

## Request Ada-1 Inventory ##
adaDict = json.loads(bapi.request_ada_inventory(
    config=configDict, authorization=authDict).content)

with responsePath.open('w') as f:
    responsePath = json.dump(adaDict, f)

## Pull Hashes and Translate ##
adaHashList = list()
for i in adaDict['Response']['sales']['data']:
    adaHashList.append(adaDict['Response']['sales']['data'][i]['itemHash'])

adaModList = list()
for i in adaHashList:
    if itemDefsDict[str(i)]['itemType'] == 19:
        modInfo = {
            'collections_hash': itemDefsDict[str(i)]['collectibleHash'],
            'name': itemDefsDict[str(i)]['displayProperties']['name'],
            'icon': itemDefsDict[str(i)]['displayProperties']['icon']
        }
        adaModList.append(modInfo)

## Write Mod Information to JSON file ##
modPath = pathlib.Path(__file__).resolve(
).parent.parent.joinpath('output', 'mods.json')

with modPath.open('w') as f:
    json.dump(adaModList, f)
    f.close()
