import sys
import math
from OnlineMusic import online_music, online_music_reverse
from EuclideanDistanceScore import calculateSimilarItems


def getRecommendations(music_data, itemSimilarityScores, user):
    userRatings = music_data[user] 
    totalScore = {}
    totalScoresProd = {}
    for (item, rating) in userRatings.items():    # looping all the rated items by user(rows)
        for (simScore, item2) in itemSimilarityScores[item]:   
            #only taking items not rated by user
            if item2 in userRatings: continue;

            totalScore.setdefault(item2, 0)
            totalScore[item2] += simScore   #total score

            totalScoresProd.setdefault(item2, 0)
            totalScoresProd[item2] += simScore * rating #total score*rating

    rankings = [(totalScoresProd[item]/totalScore[item], item) for item in totalScore.keys()]
    rankings.sort()
    rankings.reverse()
    return rankings

# generating similarity scores implemented in previous article
similarItems = calculateSimilarItems(online_music, 10) 
print(getRecommendations(online_music, similarItems, 'Donald'))