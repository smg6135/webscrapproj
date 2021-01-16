# gui
import tkinter as tk
from tkinter import Text, simpledialog
from tkinter import messagebox
import subprocess as sub

# web scrap
import re
import tkinter
from tkinter.constants import END
import requests
import json
from bs4 import BeautifulSoup

class MyDialog(simpledialog.Dialog):
    def body(self, master):
        # create gui screen
        self.geometry("600x400")
        tk.Label(master, text="What is your summoner ID ?").grid(row=0)
        # user input entry
        self.e1 = tk.Entry(master)
        self.e1.grid(row=0, column=1)
        return self.e1 # initial focus 

    def apply(self):
        # returns the user input to us
        first = self.e1.get()
        self.result = first

# getting user input to username
root = tk.Tk()
root.withdraw()
user = MyDialog(root, "League Statistics Web Scrapper")
user.apply
username = user.result

# op.gg, wasted on league request
urlop = "https://na.op.gg/summoner/userName=" + username
urlwol = "https://wol.gg/stats/na/" + username + "/"
urlyour = "https://your.gg/na/profile/" + username
urlblitz = "https://blitz.gg/lol/profile/na1/" + username
htmlop = requests.get(urlop).text
htmlwol = requests.get(urlwol).text
htmlyour = requests.get(urlyour).text
htmlblitz = requests.get(urlblitz).text
# beautiful Soup
soupop = BeautifulSoup(htmlop, 'html.parser')
soupwol = BeautifulSoup(htmlwol, 'html.parser')
soupyour = BeautifulSoup(htmlyour, 'html.parser')
soupblitz = BeautifulSoup(htmlblitz, 'html.parser')

user_rank_solo = soupop.select('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo')
user_rank_flex = soupop.select('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.sub-tier')

while(user_rank_solo == []):
    print("User not found")
    username = input("whats your summoner id? \n")
    # op.gg request
    urlop = "https://na.op.gg/summoner/userName=" + username
    htmlop = requests.get(urlop).text
    # beautiful soup
    soupop = BeautifulSoup(htmlop, 'html.parser')
    user_rank_solo = soupop.select('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo')
    user_rank_flex = soupop.select('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.sub-tier')

print('-------------------------------------')
print('Current tier (solo/flex)')
print('-------------------------------------')

for rank in user_rank_solo:
    # tier type + tier solo
    print('Ranked Solo')
    print(rank.find('div', {'class': 'TierRank'}).text.strip())
    if(rank.find('div', {'class': 'TierRank'}).text.strip() != "Unranked"):
        print(rank.select('div.TierInfo > span')[0].text.strip())
        print(rank.select('div.TierInfo > span')[1].text.strip().replace('\n', ' '))

    print('\n')
for rank in user_rank_flex:
    # tier type + tier flex
    print('Ranked Flex')
    print(rank.find('div', {'class': 'sub-tier__rank-tier'}).text.strip())

most_played = soupop.select('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div')[2].select('div')[1].select('div')[0].select('div')[0].select('div')[0]


print('-------------------------------------')
print('Total time spent on Leauge')
print('-------------------------------------')


spent_mins = soupwol.select('#time-minutes')
print(spent_mins[0].text)
spent_mins = soupwol.select('#time-hours')
print(spent_mins[0].text)
spent_mins = soupwol.select('#time-days')
print(spent_mins[0].text)

print('-------------------------------------')
print('Most played champion')
print('-------------------------------------')
print(most_played.find('div').get('title'))
most_played_kda = most_played.find('div', {'class': "PersonalKDA"}).find('div', {'class': 'KDAEach'}).select('span')
print('K ', most_played_kda[0].text, most_played_kda[1].text,'D ', most_played_kda[2].text, most_played_kda[3].text, 'A ', most_played_kda[4].text)

# 3 recent games but change number than boom more
user_games = soupop.select('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.RealContent > div > div.Content > div.GameItemList > div.GameItemWrap')

print('-------------------------------------')
print('recent 5 games summary')
print('-------------------------------------')
for i in range(5):
    print('~~~~~~~~~GAME',i+1,'~~~~~~~~~')
    user_champ = soupop.select('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.RealContent > div > div.Content > div.GameItemList > div')
    print('Champion played : ', user_champ[i].select('div.ChampionName')[0].text.strip())

    # Role
    user_role = soupblitz.select('#scroll-view-main > div > div > div > div.ProfileLayout__ProfileColumns-sc-7b34zi-0.fJwYnF > div.ProfileLayout__ProfileRightCol-sc-7b34zi-2.kHtVCs.Columns__Column-sc-24rxii-1.kbeXNP > div > div.Inner-sc-7vmxjm-0.cpZSJT > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > div > div.profile_match-image > div > svg > title')[0].text
    print('Role : ', user_role.replace("role-", ""))

    # W or L
    print("Game : ", user_games[i].find('div').get('data-game-result'))
    k = user_games[i].select('div.KDA > span.Kill')
    d = user_games[i].select('div.KDA > span.Death')
    a = user_games[i].select('div.KDA > span.Assist')
    # KDA
    kdaratio = user_games[i].select('div.KDARatio > span.KDARatio')
    print('KDA: ', 'K ', k[0].text, '/', 'D ', d[0].text, '/', 'A ', a[0].text, ' = ', kdaratio[0].text)
    your_games = soupyour.select('body > div > div.container-fluid.page-body-wrapper > div > div > div.row.mt-3 > div.col-lg-8.col-12 > div.d-flex.flex-column.mt-3 > div')
    my_ratings = your_games[i].select('div.gg-ggx-box-on-matchlist > div.gg-ggx-on-matchlist')
    print('My rating (0 ~ 10) : ', my_ratings[0].text.strip())
    print('Team rating (F ~ S) : ', my_ratings[1].text.strip())
    print('Lane rating (1:9 FF ~ 9:1 GG) : ', my_ratings[2].text.strip())



print('-------------------------------------')
print('Your total game summary, S(best) ~ F(worst)')
print('-------------------------------------')
game_summary = soupyour.select('#profileGraphAll')
data = game_summary[0].get("data-json")
json_data = json.loads(data)
for i in range(len(json_data)):
    print(json_data[i]['label'], ': ', json_data[i]['grade'])

