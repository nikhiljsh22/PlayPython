import re

class classifier:
    def __init__(self, categoryThreshold):
        #Holds features like {'money': {'good':1,'bad':2}}
        self.featureCategoryCount = {}
        #Holds category like {'good':5,'bad':8}
        self.categoryCount = {}
        #Holds category threshold like {'good':1,'bad':3}
        self.categoryThreshold = categoryThreshold


    #Breaks document and returns features
    def getFeatures(self, text):
        splitter  = re.compile('\\W*')
        words = [word.lower() for word in splitter.split(text) if len(word) > 2 and len(word) < 20]

        return dict([(word, 1) for word in words])

    #Adds new feature
    def addFeature(self, feature, category):
        self.featureCategoryCount.setdefault(feature, {})
        self.featureCategoryCount[feature].setdefault(category, 0)
        #Incrementing feature's category value
        self.featureCategoryCount[feature][category] += 1

    #Adds new category
    def addCategory(self, category):
        self.categoryCount.setdefault(category, 0)
        #Incrementing category's value
        self.categoryCount[category] += 1

    #trains our algorithm
    def trainClassifier(self, text, category):
        features = self.getFeatures(text)
        for feature in features:
            self.addFeature(feature, category)

        self.addCategory(category)

    #Calculats probability
    def simpleProbability(self, feature, category):
        if feature not in self.featureCategoryCount or \
            category not in self.featureCategoryCount[feature] or \
            self.featureCategoryCount[feature][category] == 0:
            return 0;
        else:
            # Probability = Number of favorable outcomes/Total number of possible outcomes
            return float(self.featureCategoryCount[feature][category]) / float(self.categoryCount[category])

    #Calculates weighted probability
    def weightedProbability(self, feature, category, weight=1.0, assumedProbability=0.5):
        probability = self.simpleProbability(feature, category)

        #Number of times feature appeared in all categories
        total = sum([self.featureCategoryCount[feature][cat] \
                     if feature in self.featureCategoryCount \
                     and cat in self.featureCategoryCount[feature] else 0 \
            for cat in self.categoryCount])

        return float(weight * assumedProbability + total * probability)/float(weight+total)

    #Calculates document|category probability Pr(document|category)
    def documentProbability(self, text, category):
        features = self.getFeatures(text)

        docProbability = 1
        #Multiply all feature probability in a category
        for feature in features:
            docProbability *= self.weightedProbability(feature, category)

        return docProbability

    #Calculates category|document probability Pr(category|document) = Pr(document|category) * Pr(category)/Pr(document)
    def categoryProbability(self, text, category):
        docProb = self.documentProbability(text, category)
        catProb = float(self.categoryCount[category] if category in self.categoryCount else 0)/float(sum([self.categoryCount[cat] for cat in self.categoryCount.keys()]))
        #Ignoring Pr(document) since it will become constant accross categories in same document
        return docProb*catProb

    #Classifies a document
    def classify(self, text, default='unknown'):
        probabilities = {}
        max = 0
        for cat in self.categoryCount.keys():
            probabilities[cat] = self.categoryProbability(text, cat)
            if(probabilities[cat] > max):
                max = probabilities[cat]
                bestCat = cat

        for cat in probabilities.keys():
            if cat != bestCat:
                if probabilities[cat]*self.categoryThreshold[bestCat] > probabilities[bestCat]:
                    return default
        return bestCat


threshold = {'good':1,'bad':3}
obj = classifier(threshold)
#Training algorithm
obj.trainClassifier('You won 100000$', 'bad')
obj.trainClassifier('Your credit card worth limit 5 lacs has been dispatched', 'bad')
obj.trainClassifier('Lifetime Free Membership', 'bad')
obj.trainClassifier('An over-due inheritance claim!!!', 'bad')
obj.trainClassifier('Get instant personal loan with zero paper work', 'bad')
obj.trainClassifier('Security alert', 'good')
obj.trainClassifier('Search job', 'good')
obj.trainClassifier('Latest news', 'good')
obj.trainClassifier('Javascript Framework Challenge', 'good')
obj.trainClassifier('Save 30% on new orders', 'good')
obj.trainClassifier('You won quiz', 'good')

print(obj.weightedProbability('quiz', 'good'))

print(obj.classify('You won 20000$'))
print(obj.classify('credit card offer'))
print(obj.classify('personal loan'))
print(obj.classify('Get instant personal loan with zero paper work'))
