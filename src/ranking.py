from typing import Dict, List
import re
from copy import deepcopy

class TeamScore:
    def __init__(self, score: int, name:str) -> None:
        self.score = score
        self.name = name

class Ranking:
    def __init__(self, data: List[Dict[str,int]]) -> None:
        self.data = deepcopy(data)

    def generate_ranking(self)-> List[Dict[int,str,str]]:
        """
        Generates the ranking based on the input of data into this class sorts the data and outputs it
        into the correct format for writing
        """
        struct_for_ranking = self._generate_struct_for_ranking()
        sorted_secondary_name = dict(sorted(struct_for_ranking.items(), key=lambda x: x[0]))
        sorted_struct = dict(sorted(sorted_secondary_name.items(), key=lambda x: x[1], reverse=True))
        result = self._convert_ranking_struct_to_writable_csv(sorted_struct)
        return result

    def _convert_ranking_struct_to_writable_csv(self, sorted_struct:Dict) -> List[Dict[int,str,str]]:
        """
        args: sorted_struct This struct is what will be used to write to a csv 
        returns
        """
        place = 1
        result = []
        for i, (k,v) in enumerate(sorted_struct.items()):
            score_string = f'{v} pt' if v == 1 else f'{v} pts'
            if len(result)>0:
                if result[i-1]['Score'] == v:
                    result.append({'Place':result[i-1]['Place'], 'Team':k, 'Score':score_string})
                    place +=1
                    continue
            if len(result) == 0:
                result.append({'Place': place, 'Team': k, 'Score': score_string})
                place += 1
            else:
                result.append({'Place': place, 'Team': k, 'Score': score_string})
                place +=1
        return result



    def _generate_struct_for_ranking(self):
        """
        Generates a dictionary for sorting capabilities as well as adding capabilites for scores
        """
        _internal_struct = {}
        for record in self.data:
            team_1, team_1_score, _ = re.split('(\d+)', record['Team 1 Score'])
            team_2, team_2_score, _ = re.split('(\d+)', record['Team 2 Score'])
            team_1 = TeamScore(int(team_1_score), team_1.strip())
            team_2 = TeamScore(int(team_2_score), team_2.strip())
           
            for ts in self._derive_points_awarded(team_1, team_2):
                if ts.name not in _internal_struct:
                    _internal_struct[ts.name] = ts.score
                else:
                    _internal_struct[ts.name] = _internal_struct[ts.name] + ts.score


        return _internal_struct

    def _derive_points_awarded(self, team1: TeamScore, team2: TeamScore):
        '''In this particular hockey league, 
        a tie between two teams is worth 1 point, a win is worth 3 points, 
        and a loss is worth 0 points. 

            If any teams have the same number of points,
            they are assigned the same ranking according to 
            [standard competition ranking](https://en.wikipedia.org/wiki/Ranking#Standard_competition_ranking_(%221224%22_ranking)),
            and they should be listed in alphabetical order.
 '''
        if team1.score == team2.score:
            return [TeamScore(1, team1.name), TeamScore(1,team2.name)]
        if team1.score > team2.score:
            return [TeamScore(3,team1.name), TeamScore(0,team2.name)]
        if team1.score < team2.score:
            return [TeamScore(3,team2.name),TeamScore(0,team1.name)]
