import operator
from Crawler import crawler
from DataAccess import dataAccess

class searchEngine:
    def __init__(self, database):
        self.database = database

    #to search text at webpages
    def search(self, searchText):
        #spliting text to get words
        words = searchText.split(' ')
        n = len(words)
        searchQuery = 'select url.Link'
        #[,u0.Location, u1.Location ..]
        selectQuery = [',u{}.Location'.format(i) for i in range(n)]
        #[(UrlWordLocation u0, u0), (UrlWordLocation u1, u1) ..]
        wordLocationJoinQuery = [('UrlWordLocation u{}'.format(i), 'u{}'.format(i)) for i in range(n)]
        #[(Word w0, w0), (Word w1, w1) ..]
        wordQuery = [('Word w{}'.format(i), 'w{}'.format(i)) for i in range(n)]

        #generating select part
        for i in range(n):
            searchQuery += selectQuery[i]

        searchQuery += ' from '
        #generating inner join with wordLocationJoinQuery
        for i in range(len(words)):
            if i == 0:
                searchQuery += wordLocationJoinQuery[i][0]
            else:
                searchQuery += ' inner join '
                searchQuery += wordLocationJoinQuery[i][0]
                searchQuery += ' on ' + wordLocationJoinQuery[i][1] + '.urlid = ' + wordLocationJoinQuery[i - 1][1] + '.urlid'
        #generating inner join with words
        for i in range(len(words)):
            columnMatch = wordLocationJoinQuery[i][1] + '.WordId = ' + wordQuery[i][1] + '.id'
            searchQuery += ' inner join ' + wordQuery[i][0]
            searchQuery += ' on ' + columnMatch
        #generating inner join with url
        searchQuery += ' inner join url on u0.UrlId = url.id where '
        #generating where part
        for i in range(len(words)):
            searchQuery += wordQuery[i][1] + '.word like \'' + words[i] + '\''
            if i != len(words) - 1:
                searchQuery += ' and '

        dataAcc = dataAccess(self.database)
        #executing query
        data = dataAcc.selectCommand(searchQuery)
        return data
    
    #crawl a website
    def crawlWebsite(self, domain):
        url = 'http://www.' + domain
        crawlerObj = crawler(self.database)
        crawlerObj.crawl(url, domain)

    def wordFrequencyScore(self, rows):
        resultDict = dict([(row[0], 0) for row in rows])
        for row in rows:
            resultDict[row[0]] += 1
        return resultDict

    def documentLocationScore(self, rows):
        resultDict = dict([(row[0], 100000) for row in rows])
        for row in rows:
            sumRowLocation = sum([row[i] for i in range(1, len(row))])
            if sumRowLocation < resultDict[row[0]]:
                resultDict[row[0]] = sumRowLocation
        return resultDict

    def wordDistanceScore(self, rows):
        if(len(rows) < 3):
            return dict([(row[0], 0) for row in rows])
        else:
            resultDict = dict([(row[0], 100000) for row in rows])
            for row in rows:
                wordDistance = sum([abs(row[i] - row[i-1]) for i in range(2, len(row))])
                if wordDistance < resultDict[row[0]]:
                    resultDict[row[0]] = wordDistance
        return resultDict

    def linkTextScore(self, rows, words):
        resultDict = dict([(row[0], 0) for row in rows])
        access = dataAccess(self.database)
        for word in words:
            ranks = access.selectCommand('SELECT u.Link, pr.Rank FROM LinkWords lw \
            inner join url u on lw.linkid = u.id \
            inner join PageRank pr on u.id = pr.urlid \
            inner join Word w on w.id = lw.wordid \
            where word like \'{0}\''.format(word))
            if len(ranks) > 0:
                for row in resultDict.items():
                    for rank in ranks:
                        if rank[0] == row[0]:
                            resultDict[rank[0]] = rank[1]
        return resultDict

    def normalizeScore(self, scores, preferSmall):
        maxNumber = max([row[1] for row in scores.items()])
        if preferSmall:
            for score in scores.items():
                scores[score[0]] = (maxNumber-score[1])/maxNumber
                return score.sort()
        else:
            for score in scores.items():
                scores[score[0]] = score[1]/maxNumber
                return scores.sort()

    def calculatePageRank(self, iterations=20):
        access = dataAccess(self.database)
        #Resetting rank to 1
        access.executeCommand('DELETE FROM PageRank', None)
        access.executeCommand('INSERT INTO PageRank(UrlId, Rank) SELECT Id, 1 FROM Url', None)
        for i in range(iterations):
            print('Iteration ',i)
            urlIds = access.selectCommand('SELECT Id FROM Url')
            for urlId in urlIds:
                #Minimum rank
                pageRank = 0.15
                #Which pages link to current page
                fromUrlIds = access.selectCommand('SELECT DISTINCT FromId FROM Link WHERE ToId=%d'%urlId)
                for fromUrlId in fromUrlIds:
                    #Rank of page
                    rank = access.selectCommand('SELECT Rank FROM PageRank WHERE UrlId=%d'%fromUrlId)
                    #Total links on page
                    numberOfLinks = access.selectCommand('SELECT COUNT(*) FROM Link WHERE FromId=%d'%fromUrlId)
                    #Calculation
                    pageRank += 0.85 * rank[0][0]/numberOfLinks[0][0]
                #Storing rank
                access.executeCommand('UPDATE PageRank SET Rank={0} WHERE UrlId={1}'.format(pageRank,urlId[0]), None)

    def sortResultsByPageRank(self, rows):
        access = dataAccess(self.database)
        #Distinct results
        resultDict = dict([(row[0], 0) for row in rows])
        for result in resultDict.items():
            #getting rank of each page
            pageRank = access.selectCommand('SELECT Rank from Url u INNER JOIN PageRank pr on u.Id = pr.UrlId WHERE u.Link like \'%s\''%result[0])
            resultDict[result[0]] = pageRank[0][0]
        #Sorting based on rank
        sortedResult = sorted(resultDict.items(), key=operator.itemgetter(1), reverse=True)
        return sortedResult

searchEng = searchEngine('D:\\SearchEngine.db')
#searchEng.crawlWebsite('practiceselenium.com')
results = searchEng.search('tea')
#scores = searchEng.linkTextScore(results, 'tea'.split(' '))
#searchEng.normalizeScore(scores, False)
sortedResultsByPageRank = searchEng.sortResultsByPageRank(results)
print(sortedResultsByPageRank)
#searchEng.calculatePageRank()
