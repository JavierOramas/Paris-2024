from multiprocessing import Pool            
from time import sleep
import pandas as pd
from typing import List, Tuple
from team import Team
from game import Football
from field import Field
from team import Team

import json
from group import Group


class Tournament:

    def load_groups(self):
        
        data = {}
        with open("groups.json", 'r') as f:
            # load json file
            data = json.load(f)

        groups = []
        for g in data.keys():
            teams = data[g]
            groups.append(Group(g,teams))
            # break
            
        return groups

    def __init__(self) -> None:
        groups = self.load_groups()
        self.groups = groups
        self.group_winners = []
        self.teams_8th = []
        self.teams_4th = []
        self.matches = []
        self.teams = []


    def play_match_group(self,match,g):
        zones = [
        "Defense Left",
        "Defense Center",
        "Defense Right",

        "Midfield Left",
        "Midfield Center",
        "Midfield Right",

        "Attack Left",
        "Attack Center",
        "Attack Right"
        ]
        field = Field("f1", 3, 3, zones)
        
        team1 = Team(match[0], field.field)
        team2 = Team(match[1], field.field)

        Pros = []
        match = {
            team1.team_name: 0,
            team2.team_name: 0
        }

        game = Football(team1, team2, field, 90)
        result = game.play()
        if type(result) is tuple:
            g.Tie(result[0])
            g.Tie(result[1])
        else:
            g.Winner(result)

    def play_game(self, match):
        zones = [
        "Defense Left",
        "Defense Center",
        "Defense Right",

        "Midfield Left",
        "Midfield Center",
        "Midfield Right",

        "Attack Left",
        "Attack Center",
        "Attack Right"
        ]
        field = Field("f1", 3, 3, zones)
        # print(match)
        team1 = Team(match[0], field.field)
        team2 = Team(match[1], field.field)

        # Pros = []
        # match = {
        #     team1.team_name: 0,
        #     team2.team_name: 0
        # }

        game = Football(team1, team2, field, 90)
        result = game.play()
        # print(result)
        if type(result) is tuple:
            # print("draw, re-playing")
            result = self.play_game((team1.team_name, team2.team_name))
            return result
        else:
            return result

    def run_group_games(self, group:Group):
        matches = group.get_matches() 
        while len(matches) > 0:
            match = matches.pop()
            # p.map(self.play_match_group, [match,group])
            # p.apply_async(self.play_match_group, args=(match,group))
            self.play_match_group(match,group)
            
        return (group.get_groups_classifications(),group.name)
    
    def run_games(self, matches):
        teams = []
        with Pool(12) as p:
            teams.append(p.map(self.play_game, matches))
        # for match in matches:
        #     teams.append(self.play_game(match))
            # p.join()
        return teams
    
    def run(self):
        
        print("\n\nStarting tournament\n\n", end='\r')
        # # for group in self.groups:
        # with Pool(12) as p:
        #     self.group_winners.append(p.map(self.run_group_games, self.groups))
        # self.group_winners = self.group_winners[0]
        # # print(self.group_winners)
        # # sort group winners by second element
        # self.group_winners.sort(key=lambda x: x[1])
        #     # p.join()
        #         # self.group_winners.append(self.run_group_games(group))

        # print("\n\nGroup games finished\n\n", end='\r')
        # print(self.group_winners)
        # 8th Finals
        # self.group_winners[0] = 
        self.matches = [
                        ('netherlands', 'usa'), # 49
                        ('argentina', 'australia'), # 50
                        ('england', 'senegal'), # 51
                        ('france', 'poland'), # 52
                        
                        ('japan', 'croatia'), # 53
                        ('brazil', 'south-korea'), # 54
                        ('morocco', 'spain'), # 55
                        ('portugal', 'switzerland')] # 56
        
        self.teams_8th = self.run_games(self.matches)[0]
        print("\n\n8th Finals finished\n\n", end='\r')
        # Quarter Finals
        
        self.matches = [
            (self.teams_8th[0].team_name,self.teams_8th[1].team_name),
            (self.teams_8th[2].team_name,self.teams_8th[3].team_name),
            (self.teams_8th[4].team_name,self.teams_8th[5].team_name),
            (self.teams_8th[6].team_name,self.teams_8th[7].team_name),
        ] 
        
        self.teams_4th = self.run_games(self.matches)[0]
        print("\n\nQuarter Finals finished\n\n", end='\r')
        # Semi Finals
        self.matches = [
            (self.teams_4th[0].team_name,self.teams_4th[1].team_name),
            (self.teams_4th[2].team_name,self.teams_4th[3].team_name)
        ]
        
        final_teams = self.run_games(self.matches)[0]
        # print(final_teams)
        third = []
        for t in self.teams_4th:
            if not (t.team_name in [t1.team_name for t1 in final_teams]):
                # print(t.team_name)
                third.append(t)
        
        print("\n\nSemi Finals finished\n\n", end='\r')
        # Final
        winner = self.play_game((final_teams[0].team_name,final_teams[1].team_name)) 
        if winner.team_name == final_teams[0].team_name:
            second = final_teams[1]
        else:
            second = final_teams[0]
            
        third = self.play_game((third[0].team_name,third[1].team_name))

        # print("Classified teams", [item for t in self.group_winners for item in t])
        print("8th Finals teams",   [t.team_name for t in self.teams_8th])
        print("4th Finals teams",   [t.team_name for t in self.teams_4th])

        print("Third Place: ", third.team_name)
        print("Second Place: ", second.team_name)
        print("Winner: ", winner.team_name)
        return [],self.teams_8th,self.teams_4th,self.matches,final_teams,winner
        