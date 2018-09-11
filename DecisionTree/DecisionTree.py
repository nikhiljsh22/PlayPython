class decisionNode:
    def __init__(self,col=-1,value=None,results=None,trueBranch=None,falseBranch=None):
        #column index on split happens
        self.col = col
        #column value on split happens
        self.value=value
        self.results = results
        #tree child if condition is true
        self.trueBranch = trueBranch
        #tree child if condition is false
        self.falseBranch = falseBranch


class decisionTree:
    
    #separating rows in two sets of rows
    def divideSet(self, rows, columnIndex, columnValue):
        splitFunction = None
        if isinstance(columnValue, int) or isinstance(columnValue, float):
            #condition for numeric data
            splitFunction = lambda row: row[columnIndex] >= columnValue
        else:
            #condition for string data
            splitFunction = lambda row: row[columnIndex] == columnValue

        #rows satisfy condition
        set1 = [row for row in rows if splitFunction(row)]
        #rows do not satisfy condition
        set2 = [row for row in rows if not splitFunction(row)]
        return set1,set2

    #unique data in result(usually last) column
    def uniqueResults(self, rows):
        results = {}
        for row in rows:
            #result is last column of a row i.e. 2BHK
            result = row[len(row)-1]
            results.setdefault(result, 0)
            results[result] += 1
        return results

    #calculates entropy of a group
    def entropy(self, rows):
        import math
        uniqueRes = self.uniqueResults(rows)
        entropy = 0
        for result in uniqueRes.values():
            p = float(result)/len(rows)
            #logrithm of base 2
            entropy -= p*math.log(p, 2)

        return entropy

    def buildTree(self, rows, entropyFun=entropy):
        if(len(rows) == 0):
            return
        current_entropy = entropyFun(rows)
        best_gain = 0
        best_criteria = None
        best_sets = None

        #leaving last column in calculation since it is result
        column_count = len(rows[0]) - 1
        for col in range(column_count):
            column_values = {}

            for row in rows:
                columnVal = row[col]
                #getting each unique value in that column
                column_values[columnVal] = 1

            for colVal in column_values:
                #try to split rows based on each column value
                set1,set2 = self.divideSet(rows, col, colVal)
                #calculate weighted average entropy of both sets
                avgEntropy = float(entropyFun(set1)*len(set1) + entropyFun(set2)*len(set2))/len(rows)
                #subtracting entropy of parent group from average entropy of 2 groups to calculate gain
                gain = current_entropy - avgEntropy
                #taking highest gain to choose split condition
                if(gain > best_gain and len(set1) > 0 and len(set2) > 0):
                    best_gain = gain
                    best_criteria = (col, colVal)
                    best_sets = (set1,set2)
        if(best_gain  > 0):
            #building tree
            trueBranch = self.buildTree(best_sets[0], self.entropy)
            falseBranch = self.buildTree(best_sets[1], self.entropy)
            return decisionNode(col=best_criteria[0],value=best_criteria[1], trueBranch=trueBranch, falseBranch=falseBranch)
        else:
            return decisionNode(results=self.uniqueResults(rows))

    #prints tree
    def printTree(self, tree, colNames, indent=''):
        if(tree.results != None):
            #print result
            print(indent + str(tree.results))
        else:
            #print node condition
            print(indent + str(colNames[tree.col]) +':'+ str(tree.value))
            #print true branch
            print(indent+'T->')
            self.printTree(tree.trueBranch, colNames, indent+'    ')
            #print false branch
            print(indent+'F->')
            self.printTree(tree.falseBranch, colNames, indent+'    ')

    #classify new users
    def classify(self, observation, tree):
        if(tree.results != None):
            return tree.results
        else:
            v=observation[tree.col]
            branch=None
            if(isinstance(v, int) or isinstance(v, float)):
                if(v>=tree.value):branch=tree.trueBranch
                else:branch=tree.falseBranch
            else:
                if(v==tree.value):branch=tree.trueBranch
                else:branch=tree.falseBranch
            return self.classify(observation,branch)


familyData = [
[1,30000,'Unmarried',1,'None'],
[2,50000,'Unmarried',1,'2BHK'],
[4,70000,'Married',3,'3BHK'],
[6,90000,'Married',3,'3BHK'],
[2,55000,'Married',2,'None'],
[4,55000,'Married',2,'3BHK'],
[3,60000,'Married',2,'2BHK'],
[1,35000,'Unmarried',1,'2BHK'],
[1,25000,'Unmarried',2,'1BHK'],
[6,95000,'Married',3,'4BHK'],
[6,85000,'Married',4,'4BHK'],
[4,50000,'Married',3,'3BHK'],
[3,50000,'Unmarried',3,'3BHK'],
[4,80000,'Married',3,'2BHK'],
[6,90000,'Married',2,'4BHK'],
[4,75000,'Married',3,'4BHK'],
[2,60000,'Married',2,'1BHK']
]
treeClass = decisionTree()
tree = treeClass.buildTree(familyData, treeClass.entropy)
#print the tree
treeClass.printTree(tree, ['Number of Members','Salary','Marital Status','Inquiries', 'Flat Type'])

print(treeClass.classify([2,40000,'Unmarried',1],tree))
print(treeClass.classify([1,10000,'Unmarried',1],tree))
print(treeClass.classify([6,80000,'Married',1],tree))
