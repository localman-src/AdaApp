import requests
import json


def get_bapi(
        endpoint,
        headers_,
        body="",
        querystring="",
        anchor="https://www.bungie.net/Platform/"):

    uri = anchor + endpoint
    return requests.get(uri, headers=headers_, params=querystring, data=body)


def post_bapi(
        endpoint,
        headers_,
        body="",
        querystring="",
        anchor="https://www.bungie.net/Platform/"):

    uri = anchor + endpoint
    return requests.post(uri, headers=headers_, data=body, params=querystring)


def request_manifest(endpoint_="Destiny2/Manifest/"):
    return get_bapi(endpoint=endpoint_, headers_="")


def request_new_tokens(authorization):
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

    return post_bapi(endpoint="App/OAuth/Token/", headers_=headers, body=body_)


def request_ada_inventory(config, authorization):
    endpoint = "Destiny2/3/Profile/" + \
        config['membershipID'] + "/Character/" + \
        config['characterID'] + "/Vendors/" + config['ada_hash']
    headers = {
        'X-API-KEY': authorization['X-API-KEY'],
        'Authorization': "Bearer " + authorization['access_token']
    }

    return get_bapi(endpoint=endpoint, headers_=headers, querystring={'components': '402'})


def request_bungie_user(bungiename, authorization):
    bungiePrefix = bungiename.split('#')[0]
    bungieSuffix = bungiename.split('#')[1]

    endpoint = "/User/Search/GlobalName/0/"

    headers = {
        "X-API-KEY": authorization["X-API-KEY"]
    }

    body = {
        "displayNamePrefix": bungiePrefix
    }

    response = json.loads(
        post_bapi(
            endpoint=endpoint,
            headers_=headers,
            body=json.dumps(body)).content)

    for r in response['Response']['searchResults']:
        if str(r['bungieGlobalDisplayNameCode']) == bungieSuffix:
            user = r

    return user

def request_user_collections(user, authorization):
    memberID = user['destiny_membership_id']
    memberType = user['destiny_membership_type']

    headers = {
        "X-API-KEY": authorization["X-API-KEY"]
    }
    
    endpoint = f'/Destiny2/{memberType}/Profile/{memberID}/'

    return get_bapi(endpoint=endpoint, headers_=headers, querystring={'components': '800'})