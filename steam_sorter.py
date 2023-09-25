import requests
import pandas as pd

USER_API_KEY = 'INSERT STEAM API KEY'
USER_STEAM_ID = 'INSERT STEAM ID'

api = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
res = requests.get(url=api)
dict = res.json()['applist']['apps']
data_clean = {}
for game in dict:
    data_clean[game['appid']] = game['name']

def get_name(id):
    return data_clean[id]

def get_score(id):
    data = requests.get(f'https://store.steampowered.com/appreviews/{id}?json=1').json()['query_summary']
    score = data['total_positive']/data['total_reviews']
    return score

user_url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={USER_API_KEY}&steamid={USER_STEAM_ID}&format=json'
user_game_data = requests.get(url=user_url).json()

games_owned_id = []
for result in user_game_data['response']['games']:
    games_owned_id.append(result['appid'])

my_games_and_user_scores = {}
for game_id in games_owned_id:
    try:
        my_games_and_user_scores[get_name(game_id)] = get_score(game_id)
    except:
        pass

df = pd.DataFrame(my_games_and_user_scores.items(), columns=('Game', 'User Score'))
df.sort_values(by=('User Score'), inplace=True, ascending=False)

df.to_csv('~/Desktop/mygames.csv')