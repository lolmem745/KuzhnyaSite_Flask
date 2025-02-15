import requests


# Функция для получения puuid аккаунта Riot
def get_account_puuid(name, tag, RIOT_API_KEY):
    url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={RIOT_API_KEY}'
    response = requests.get(url)
    return response.json()["puuid"]


# Функция для получения данных об аккаунте Лиги Легенд
def get_summoner_info_by_puuid(region, summoner_puuid, RIOT_API_KEY):
    url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{summoner_puuid}?api_key={RIOT_API_KEY}'
    response = requests.get(url)
    return response.json()


# Функция для получения данных о рейтинге пользователя в Лиге Легенд
def get_ranked_info(region, summoner_id, RIOT_API_KEY):
    url = f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={RIOT_API_KEY}'
    response = requests.get(url)
    return response.json()
#
# {
#     "id": "xPG-4aKh8lLHbhEmcqnng5piYfJizrOJpiOxbx_2axnsEbkq",
#     "accountId": "EBrPVOcppgzvRGbKdjfn96yAfTPS05x4Uh5ucQcF-CfEggN2nvDSofEv",
#     "puuid": "eBYfdTq6CAElRFRQWA9A1kAvHPWmW-0oHwSiP9AH6XntM4aArzYj6srybrI11P0aolGHxtzXg4ymFQ",
#     "profileIconId": 6770,
#     "revisionDate": 1739396496771,
#     "summonerLevel": 457
# }

# [
#     {
#         "leagueId": "c978a19b-3253-4672-9d4f-fce7fad4909c",
#         "queueType": "RANKED_SOLO_5x5",
#         "tier": "GOLD",
#         "rank": "II",
#         "summonerId": "xPG-4aKh8lLHbhEmcqnng5piYfJizrOJpiOxbx_2axnsEbkq",
#         "leaguePoints": 1,
#         "wins": 38,
#         "losses": 35,
#         "veteran": false,
#         "inactive": false,
#         "freshBlood": false,
#         "hotStreak": false
#     },
#     {
#         "leagueId": "fac2678b-60b2-4051-85b9-969ec9e38acf",
#         "queueType": "RANKED_FLEX_SR",
#         "tier": "EMERALD",
#         "rank": "III",
#         "summonerId": "xPG-4aKh8lLHbhEmcqnng5piYfJizrOJpiOxbx_2axnsEbkq",
#         "leaguePoints": 26,
#         "wins": 14,
#         "losses": 16,
#         "veteran": false,
#         "inactive": false,
#         "freshBlood": false,
#         "hotStreak": false
#     }
# ]