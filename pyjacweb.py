# gui
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
# web scrap
import re
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


#username = input("whats your summoner id? \n")
# op.gg, wasted on league request
urlop = "https://na.op.gg/summoner/userName=" + username
urlwol = "https://wol.gg/stats/na/" + username + "/"
urlyour = "https://your.gg/na/profile/" + username
htmlop = requests.get(urlop).text
htmlwol = requests.get(urlwol).text
htmlyour = requests.get(urlyour).text
# beautiful Soup
soupop = BeautifulSoup(htmlop, 'html.parser')
soupwol = BeautifulSoup(htmlwol, 'html.parser')
soupyour = BeautifulSoup(htmlyour, 'html.parser')

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
    print(rank.find('div', {'class': 'RankType'}).text.strip())
    print(rank.find('div', {'class': 'TierRank'}).text.strip())

for rank in user_rank_flex:
    # tier type + tier flex
    print(rank.find('div', {'class': 'sub-tier__rank-type'}).text.strip())
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
world_rank = soupwol.select('#rank-world')
print(world_rank[0].text.strip().replace(" ", ""))

print('-------------------------------------')
print('Most played champion')
print('-------------------------------------')
print(most_played.find('div').get('title'))
most_played_kda = most_played.find('div', {'class': "PersonalKDA"}).find('div', {'class': 'KDAEach'}).select('span')
print('K ', most_played_kda[0].text, most_played_kda[1].text,'D ', most_played_kda[2].text, most_played_kda[3].text, 'A ', most_played_kda[4].text)

# 3 recent games but change number than boom more
user_games = soupop.select('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.RealContent > div > div.Content > div.GameItemList > div.GameItemWrap')

print('-------------------------------------')
print('recent 3 games summary')
print('-------------------------------------')
for i in range(3):
    print(user_games[i].find('div').get('data-game-result'))
    k = user_games[i].select('div.KDA > span.Kill')
    d = user_games[i].select('div.KDA > span.Death')
    a = user_games[i].select('div.KDA > span.Assist')
    print('K ', k[0].text, '/', 'D ', d[0].text, '/', 'A ', a[0].text)


print('-------------------------------------')
print('Your total game summary, S(best) ~ F(worst)')
print('-------------------------------------')
game_summary = soupyour.select('#profileGraphAll')
data = game_summary[0].get("data-json")
json_data = json.loads(data)
for i in range(len(json_data)):
    print(json_data[i]['label'], ': ', json_data[i]['grade'])