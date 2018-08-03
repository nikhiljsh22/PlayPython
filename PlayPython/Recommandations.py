import sys
import math
sys.path.append("Data")
from OnlineMusic import online_music
from EuclideanDistanceScore import euclidean_distnce

def gerRecommandations(music_data, person, similiraty=euclidean_distnce):
    sumScores = {}
    sumProducts = {}
    for other in music_data.keys():
        if other != person:
            score = similiraty(online_music, 'Donald', other)

            if score == 0: continue

            for item in online_music[other]:
                if item not in online_music[person] or online_music[person][item] == 0:
                    sumScores.setdefault(item, 0)
                    sumScores[item] += score
                    sumProducts.setdefault(item, 0)
                    sumProducts[item] += score * online_music[other][item]

    rankings = [(sumProducts[item]/sumScores[item], item) for item in sumScores]
    return rankings;

rankings = gerRecommandations(online_music, "Donald")
rankings.sort()
rankings.reverse()
print(rankings)