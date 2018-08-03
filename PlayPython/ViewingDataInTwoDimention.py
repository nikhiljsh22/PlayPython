import math
import random
from PIL import Image, ImageDraw, ImageFont

def getCoordinates(data, gradientRate=0.1):
    #number of data points given
    n = len(data)
    
    #initializing n random points in 2d
    randomPoints = [[random.random(), random.random()] for i in range(n)]
    randomDistance = [[0.0 for i in range(n)] for j in range(n)]
    lastError = None

    for k in range(1000):
        #calculating distance between random points
        for i in range(n):
            for j in range(n):
                #distance calculated between random points by √(x1-x2)^2 + (y1-y2)^2
                randomDistance[i][j] = math.sqrt(sum([pow(randomPoints[i][x] - randomPoints[j][x], 2) for x in range(len(randomPoints[i]))]))

        #how many gradient to move to reduce error, initializing to zero
        gradMoveBy = [[0.0, 0.0] for i in range(n)]
        totalError = 0.0
        #calculating how many gradient to move towards or far, based on given distance and random distance 
        for i in range(n):
            for j in range(n):
                if i == j: continue
                actualDist = data[i][j] # from given data
                randomDist = randomDistance[i][j] # calculated from randomly placed data points
                #calculating error percentage in distance (random-actual)/actual
                errorPercentage = (randomDist-actualDist)/actualDist
                #every point has to be moved away or move towards in propotion to error percentage
                gradMoveBy[i][0] += ((randomPoints[i][0] - randomPoints[j][0])/randomDist)*errorPercentage
                gradMoveBy[i][1] += ((randomPoints[i][1] - randomPoints[j][1])/randomDist)*errorPercentage
                totalError += abs(errorPercentage)

        print(totalError)
        if lastError and lastError < totalError: break
        lastError = totalError

        #correcting positions
        for i in range(n):
            randomPoints[i][0] -= gradientRate*gradMoveBy[i][0]
            randomPoints[i][1] -= gradientRate*gradMoveBy[i][1]
        
    return randomPoints

def draw2d(data,labels,jpeg='DataPoints2D.jpg'):
    img=Image.new('RGB',(2000,2000),(255,255,255))
    draw=ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 20)
    for i in range(len(data)):
        x=data[i][0]*500 #500 times of each point to see it clear in Image
        y=data[i][1]*500
        draw.text((x,y),labels[i],(0,0,0),font)
    img.save(jpeg,'JPEG')

#given data in array of array
data = [
    [0.0, 0.1, 0.4, 0.7],
    [0.1, 0.0, 0.8, 0.6],
    [0.4, 0.8, 0.0, 0.5],
    [0.7, 0.6, 0.5, 0.0]
    ]
#generated coordinates from random points
pointsOn2d = getCoordinates(data)
print("Created coordinates:")
print(pointsOn2d)
#creating image file
draw2d(pointsOn2d, ['A', 'B', 'C', 'D'])