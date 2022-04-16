import requests
import json
import typing

auth = typing.NewType("Auth", dict[str, str])
userdata = typing.NewType("UserData", dict[str,list[dict[str,str]]])

def get(
        endpoint:str,
        headers_:dict[str,str],
        body:dict[str,str] = {},
        querystring:dict[str,str]={},
        anchor:str="https://www.bungie.net/Platform/"):

    uri = anchor + endpoint
    return requests.get(uri, headers=headers_, params=querystring, data=body)


def post(
        endpoint:str,
        headers_:dict[str,str],
        body:str ="",
        querystring:dict[str,str]={},
        anchor:str="https://www.bungie.net/Platform/"):

    uri = anchor + endpoint
    return requests.post(uri, headers=headers_, data=body, params=querystring)


def request_manifest(endpoint_:str="Destiny2/Manifest/"):
    return get(endpoint=endpoint_, headers_={})


def request_new_tokens(authorization:auth):
    headers = {
        'X-API-KEY': authorization['X-API-KEY']
    }

    body_ = {
        "Content-Type": "application/x-www-form-urlencoded",
        "grant_type": "refresh_token",
        "refresh_token": authorization['refresh_token'],
        "client_id": authorization['client_id'],
        'client_secret': authorization['client_secret']
    }

    return post(endpoint="App/OAuth/Token/", headers_=headers, body=body_)


def request_ada_inventory(config:dict[str,str], authorization:auth):
    membershipID:str = config['membershipID']
    characterID:str = config['characterID']
    adaHash:str = config['ada_hash']
    endpoint = f'Destiny2/3/Profile/{membershipID}/Character/{characterID}/Vendors/{adaHash}'
    
    headers = {
        'X-API-KEY': authorization['X-API-KEY'],
        'Authorization': "Bearer " + authorization['access_token']
    }

    return get(endpoint=endpoint, headers_=headers, querystring={'components': '402'})


def request_bungie_user(bungiename:str, authorization:auth) -> userdata:
    bungiePrefix = bungiename.split('#')[0]
    bungieSuffix = bungiename.split('#')[1]

    endpoint = "/User/Search/GlobalName/0/"

    headers = {
        "X-API-KEY": authorization["X-API-KEY"]
    }

    body = {
        "displayNamePrefix": bungiePrefix,
        "a": "b"
    }

    response = json.loads(
        post(
            endpoint=endpoint,
            headers_=headers,
            body=json.dumps(body)).content)
    print(body)
    print(response)
    user = userdata({})
    for r in response['Response']['searchResults']:
        if r['bungieGlobalDisplayNameCode'] == int(bungieSuffix):
            user = r

    return user

def request_user_collections(user:dict[str,str], authorization:auth):
    memberID:str = user['destiny_membership_id']
    memberType:str = user['destiny_membership_type']

    headers = {
        "X-API-KEY": authorization["X-API-KEY"]
    }
    
    endpoint = f'/Destiny2/{memberType}/Profile/{memberID}/'

    return get(endpoint=endpoint, headers_=headers, querystring={'components': '800'})