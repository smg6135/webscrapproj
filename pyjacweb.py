# gui
import tkinter as tk
from tkinter import Text, simpledialog
from tkinter import messagebox
import subprocess as sub

# web scrap
import re
import tkinter
from tkinter.constants import END
from tkinter import *
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

def helper(lst):
    newstr = ""
    for x in lst:
        newstr += x
        newstr += "\n"
    return newstr

def gui(tier, timespent, favchamp, matchhistory, gamesummary):
    top = Tk()
    top.geometry("800x800")
    lst = ['asdfasdf', 'ablabla', 'yesyes']
    tierstr = helper(tier)
    timestr = helper(timespent)
    mostplayedstr = helper(favchamp)
    historystr0 = helper(matchhistory[0])
    historystr1 = helper(matchhistory[1])
    historystr2 = helper(matchhistory[2])
    historystr3 = helper(matchhistory[3])
    historystr4 = helper(matchhistory[4])
    totalstr = helper(gamesummary)
    tierLabel = Label(top, text = "Current Tier (Solo/Flex)").place(x = 40, y = 0)

    tierLabel2 = Label(top, text = tierstr).place(x = 40, y = 30)

    timeLabel = Label(top, text = "Total time spent on League").place(x = 40, y = 420)

    timeLabel2 = Label(top, text = timestr).place(x = 40, y = 440)

    mostplayedLabel = Label(top, text = "Most played champion").place(x = 40, y = 250)

    mostplayedLabel2 = Label(top, text = mostplayedstr).place(x = 40, y = 270)

    historyLabel = Label(top,text = "Recent 5 games summary").place(x = 400, y = 0)

    historyLabel0 = Label(top, text = historystr0).place(x = 400, y = 20)
    historyLabel1 = Label(top, text = historystr1).place(x = 400, y = 170)
    historyLabel2 = Label(top, text = historystr2).place(x = 400, y = 320)
    historyLabel3 = Label(top, text = historystr3).place(x = 400, y = 470)
    historyLabel4 = Label(top, text = historystr4).place(x = 400, y = 620)

    totalLabel = Label(top, text = "Your total game summary, S(best) ~ F(worst)").place(x = 40, y = 600)

    totalLabel2 = Label(top, text = totalstr).place(x = 40, y = 620)

    top.mainloop()

def opgg(soupop):

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

    for rank in user_rank_solo:
        # tier type + tier solo
        solorank = rank.find('div', {'class': 'TierRank'}).text.strip()
        if(rank.find('div', {'class': 'TierRank'}).text.strip() != "Unranked"):
            soloLP = rank.select('div.TierInfo > span')[0].text.strip()
            soloWR = rank.select('div.TierInfo > span')[1].text.strip().replace('\n', ' ')

        print('\n')
    for rank in user_rank_flex:
        # tier type + tier flex
        flexrank = rank.find('div', {'class': 'sub-tier__rank-tier'}).text.strip()

    return ["Ranked Solo", solorank, soloLP, soloWR, "", "Ranked Flex", flexrank]

def wolgg(soupwol):
    spent_mins = soupwol.select('#time-minutes')[0].text
    spent_hours = soupwol.select('#time-hours')[0].text
    spent_days = soupwol.select('#time-days')[0].text
    return [spent_mins, spent_hours, spent_days]

def mostplayed(soupop):
    most_played = soupop.select('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div')[2].select('div')[1].select('div')[0].select('div')[0].select('div')[0]
    champ = most_played.find('div').get('title')
    most_played_kda = most_played.find('div', {'class': "PersonalKDA"}).find('div', {'class': 'KDAEach'}).select('span')
    kda = 'K ' + most_played_kda[0].text + most_played_kda[1].text + 'D '+ most_played_kda[2].text+ most_played_kda[3].text+ 'A '+ most_played_kda[4].text
    return [champ, kda]

def recentgames(soupop, soupblitz, soupyour):
    user_games = soupop.select('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.RealContent > div > div.Content > div.GameItemList > div.GameItemWrap')
    output = []
    for i in range(5):
        game = '~~~~~~~~~GAME '+ str(i+1) + ' ~~~~~~~~~'
        user_champ = soupop.select('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.RealContent > div > div.Content > div.GameItemList > div')
        champ = 'Champion played : '+ user_champ[i].select('div.ChampionName')[0].text.strip()

        # Role
        user_role = soupblitz.select('#scroll-view-main > div > div > div > div.ProfileLayout__ProfileColumns-sc-7b34zi-0.fJwYnF > div.ProfileLayout__ProfileRightCol-sc-7b34zi-2.kHtVCs.Columns__Column-sc-24rxii-1.kbeXNP > div > div.Inner-sc-7vmxjm-0.cpZSJT > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > div > div.profile_match-image > div > svg > title')[0].text
        role = 'Role : ' + user_role.replace("role-", "")

        # W or L
        status = "Game : " + user_games[i].find('div').get('data-game-result')
        k = user_games[i].select('div.KDA > span.Kill')
        d = user_games[i].select('div.KDA > span.Death')
        a = user_games[i].select('div.KDA > span.Assist')
        # KDA
        kdaratio = user_games[i].select('div.KDARatio > span.KDARatio')
        kda = 'KDA: '+ 'K '+ k[0].text+ '/'+ 'D '+ d[0].text+ '/'+ 'A '+ a[0].text+ ' = '+ kdaratio[0].text
        your_games = soupyour.select('body > div > div.container-fluid.page-body-wrapper > div > div > div.row.mt-3 > div.col-lg-8.col-12 > div.d-flex.flex-column.mt-3 > div')
        my_ratings = your_games[i].select('div.gg-ggx-box-on-matchlist > div.gg-ggx-on-matchlist')
        rating = 'My rating (0 ~ 10) : '+ my_ratings[0].text.strip()
        team_rating = 'Team rating (F ~ S) : ' + my_ratings[1].text.strip()
        lane_rating = 'Lane rating (1:9 FF ~ 9:1 GG) : ' + my_ratings[2].text.strip()
        output.append([game, champ, role, status, kda, rating, team_rating, lane_rating])
    return output

def summary(soupyour):
    game_summary = soupyour.select('#profileGraphAll')
    data = game_summary[0].get("data-json")
    json_data = json.loads(data)
    newlst = []
    for i in range(len(json_data)):
        newlst.append(json_data[i]['label'] + ': ' + json_data[i]['grade'])
    return newlst

if __name__ == '__main__':
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

    tier = opgg(soupop)
    timespent = wolgg(soupwol)
    favchamp = mostplayed(soupop)
    matchhistory = recentgames(soupop, soupblitz, soupyour)
    gamesummary = summary(soupyour)

    gui(tier, timespent, favchamp, matchhistory, gamesummary)
