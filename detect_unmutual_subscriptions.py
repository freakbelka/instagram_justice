import requests
import json
import urllib

# Get this from browser. Open www.instagram.com -> dev console -> network -> copy any request as curl
USER_ID = 1111  # user_id from curl
COOKIES = 'cookie: bla bla'  # cookies from curl

FOLLOWERS_HASH = 'c76146de99bb02f6415203be841dd25a'
FOLLOWING_HASH = 'd04b0a864b4b54837c0d870b0e77e076'

base_url = 'https://www.instagram.com/graphql/query/?query_hash={0}&variables={1}'
variables = {"id": USER_ID,
             "include_reel": True,
             "fetch_mutual": False,
             "first": 24}
headers = {
    'cookie': COOKIES
}


def get_users(query_hash, edge_name):
    url_main = base_url.format(query_hash, urllib.quote(json.dumps(variables)))
    response = json.loads(requests.get(url_main, headers=headers).content)

    edge_follow = response.get('data').get('user').get(edge_name)
    edges = edge_follow.get('edges')
    page_info = edge_follow.get('page_info')

    following = []

    while True:
        for edge in edges:
            following.append(edge.get('node').get('username'))

        if not page_info.get('has_next_page'):
            break

        end_cursor = page_info.get('end_cursor')
        after_variables = {"after": end_cursor}
        after_variables.update(variables)
        response = json.loads(
            requests.get(base_url.format(query_hash, urllib.quote(json.dumps(after_variables))),
                         headers=headers).content)
        edge_follow = response.get('data').get('user').get(edge_name)
        edges = edge_follow.get('edges')
        page_info = edge_follow.get('page_info')
    return following


users_for_unsubscribtion = []

i_follow = get_users(FOLLOWING_HASH, 'edge_follow')
followers = get_users(FOLLOWERS_HASH, 'edge_followed_by')

for f in i_follow:
    if f not in followers:
        users_for_unsubscribtion.append(f)

print users_for_unsubscribtion
