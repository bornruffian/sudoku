import os
import sys
from sets import Set
import math

class Tree(object):
   def __init__(self, s):
      self.parent = None
      self.child = []      
      self.row = None
      self.col = None
      self.first = None
      self.second = None
      self.points = s
   def getRoot(self):
      if self.parent != None:
         return self.parent.getRoot()
      else:
         return self
   def checkParents(self, row, col):
      if self.row != row or self.col != col:      
         if self.parent != None:
            return self.parent.checkParents(row,col)
         else:
            return 1
      else:
         return 0
   def addChild(self, row, col, first, second):
      #if (row, col) not in self.points:
      if self.checkParents(row,col):
         #print 'Adding child ' + str(row) + ',' + str(col) + ' first=' + str(first)
         self.child.append(Tree(self.points))
         self.child[-1].parent = self
         self.child[-1].row = row
         self.child[-1].col = col      
         self.child[-1].first = first
         self.child[-1].second = second
         self.points.add((row,col))
         return 1
      else:
         return 0
      
      
class ColoredTree(object):
   def __init__(self, s):
      self.parent = None
      self.child = []      
      self.row = None
      self.col = None
      self.points = s
      self.color = 0
   def getRoot(self):
      if self.parent != None:
         return self.parent.getRoot()
      else:
         return self
   def checkParents(self, row, col):
      if self.row != row or self.col != col:      
         if self.parent != None:
            return self.parent.checkParents(row,col)
         else:
            return 1
      else:
         return 0
   def addChild(self, row, col):
      if (row,col) not in self.points:
         #print 'Adding child ' + str(row) + ',' + str(col) 
         self.child.append(ColoredTree(self.points))
         self.child[-1].parent = self
         self.child[-1].row = row
         self.child[-1].col = col  
         if self.color == 0:
            self.child[-1].color = 1
         else:
            self.child[-1].color = 0         
         self.points.add((row,col))
         return 1
      else:
         return 0
            
   

def column(matrix, i):
    return [row[i] for row in matrix]

def useDeductionBlock(grid, r, c, num, candidates):
   num_eliminated = 0
   if num not in findExcludes(grid, r, c):
      row_block = 0      
      if r >= 3 and r < 6:
         row_block = 3
      if r >= 6:
         row_block = 6
         
      col_block = 0      
      if c >= 3 and c < 6:
         col_block = 3
      if c >= 6:
         col_block = 6 
      
      blankCount = 0
      excludeCount = 0
      for row in range(row_block,row_block + 3):
         for col in range(col_block,col_block + 3):
            if grid[row][col] == -1 and (row != r or col != c):
               blankCount += 1
               cannot = findExcludes(grid, row, col)
               if num in cannot:
                  excludeCount += 1
      
      if blankCount == excludeCount and blankCount > 0:
         print 'Setting [' + str(r) + ',' + str(c) + '] to ' + str(num) + ' via block'
         grid[r][c] = num
         candidates[r][c] = []     
         num_eliminated = 1
         
   return num_eliminated         
      
def useDeductionRow(grid, r, c, num, candidates):
   num_eliminated = 0
   if num not in findExcludes(grid, r, c):
      blankCount = 0
      excludeCount = 0
      
      # loop across row (use all columns)
      for col in range(9):
         if grid[r][col] == -1 and (col != c):
            blankCount += 1
            cannot = findExcludes(grid, r, col)            
            if num in cannot:
               excludeCount += 1
      
      if blankCount == excludeCount and blankCount > 0:
         print 'Setting [' + str(r) + ',' + str(c) + '] to ' + str(num) + ' via row'
         grid[r][c] = num  
         candidates[r][c] = []
         num_eliminated = 1
         
   return num_eliminated

def useDeductionCol(grid, r, c, num, candidates):
   num_eliminated = 0
   if num not in findExcludes(grid, r, c):
      blankCount = 0
      excludeCount = 0
      
      for row in range(9):
         if grid[row][c] == -1 and (row != r):
            blankCount += 1     
            cannot = findExcludes(grid, row, c)
            if num in cannot:
               excludeCount += 1
      
      if blankCount == excludeCount and blankCount > 0:
         print 'Setting [' + str(r) + ',' + str(c) + '] to ' + str(num) + ' via col'
         grid[r][c] = num    
         candidates[r][c] = [] 
         num_eliminated = 1
         
   return num_eliminated         
            
def findExcludes(grid, r, c):
   cannotBe = []
   
   # check row
   for row in range(9):
      if grid[row][c] != -1:
         cannotBe.append(grid[row][c])

   # check col
   for col in range(9):
      if grid[r][col] != -1:
         cannotBe.append(grid[r][col])
      
   # check block
   row_block = 0      
   if r >= 3 and r < 6:
      row_block = 3
   if r >= 6:
      row_block = 6
      
   col_block = 0      
   if c >= 3 and c < 6:
      col_block = 3
   if c >= 6:
      col_block = 6  
        
   for row in range(row_block,row_block + 3):
      for col in range(col_block,col_block + 3):
         if grid[row][col] != -1:
            cannotBe.append(grid[row][col])
      
   return set(cannotBe)

def removePairs(candidates):   
   for row in range(9):
      for col in range(9):
         if len(candidates[row][col]) == 2:
            for r in range(9):
               if r != row and set(candidates[r][col]) == set(candidates[row][col]):
                  for r2 in range(9):
                     if r2 != r and r2 != row:
                        for val in candidates[row][col]:
                           if val in candidates[r2][col]:
                              candidates[r2][col].remove(val)
            for c in range(9):
               if c != col and set(candidates[row][c]) == set(candidates[row][col]):
                  for c2 in range(9):
                     if c2 != c and c2 != col:
                        for val in candidates[row][col]:
                           if val in candidates[row][c2]:
                              candidates[row][c2].remove(val) 
   
def removeTriples(candidates):   
   for row in range(9):
      for col in range(9):
         if len(candidates[row][col]) == 3:
            count = 0
            for r in range(9):              
               if r != row and set(candidates[r][col]).issubset(set(candidates[row][col])) and len(set(candidates[r][col])) > 0:
                  count += 1
            if count >= 2:               
               for r2 in range(9):
                  if not set(candidates[r2][col]).issubset(set(candidates[row][col])):
                     for val in candidates[row][col]:
                        if val in candidates[r2][col]:
                           print 'Remove ' + str(val) + ' from [' + str(r2) + '][' + str(col) + '] via col triple ' + str(candidates[row][col]) + ' at [' + str(row) + ',' + str(col) + ']'
                           candidates[r2][col].remove(val)
            count = 0
            for c in range(9):              
               if c != col and set(candidates[row][c]).issubset(set(candidates[row][col])) and len(set(candidates[row][c])) > 0:
                  count += 1
            if count >= 2:
               for c2 in range(9):
                  if not set(candidates[row][c2]).issubset(set(candidates[row][col])):
                     for val in candidates[row][col]:
                        if val in candidates[row][c2]:
                           print 'Remove ' + str(val) + ' from [' + str(row) + '][' + str(c2) + '] via row triple ' + str(candidates[row][col]) + ' at [' + str(row) + ',' + str(col) + ']'
                           candidates[row][c2].remove(val)  

def uniqueCandidates(grid, candidates):
   for row in range(9):
      for col in range(9):
         for c in candidates[row][col]:
            unique_candidate = 1
            for col2 in range(9):
               if col2 != col and c in candidates[row][col2]:
                  unique_candidate = 0
                  break;
            if unique_candidate == 1:
               print 'Unique candidate ' + str(c) + ' at row ' + str(row) + ', col ' + str(col)
               grid[row][col] = c
               candidates[row][col] = []         
               return
            
                           
def lineBoxReduction(candidates, rows=1):
   for rb in range(3):
      for cb in range(3):
         row_block = rb * 3            
         col_block = cb * 3
         
         row_candidates = [[] for x in range(3)]
         other_candidates = [[] for x in range(3)]
         i = 0
         for row in range(row_block,row_block+3):      
            for col in range(col_block,col_block+3): 
               for val in candidates[row][col]:
                  if val not in row_candidates[i]:
                     row_candidates[i].append(val) 
            for col in range(9):
               if col not in range(col_block,col_block+3):
                  for val in candidates[row][col]:
                     if val not in other_candidates[i]:
                        other_candidates[i].append(val)
            i += 1
         
         for r in range(3):
            for val in row_candidates[r]:
               if val not in other_candidates[r]:
                  for r2 in range(3):
                     if r2 != r:
                        if val in row_candidates[r2] and val in other_candidates[r2]:
                           for c in range(col_block,col_block+3):
                              if val in candidates[row_block+r2][c]:
                                 if rows == 1:
                                    print 'Remove ' + str(val) + ' from [' + str(row_block+r2) + ',' + str(c) + '] via linebox (row) at [' + str(row_block+r) + ',' + str(c) + ']'   
                                 else:
                                    print 'Remove ' + str(val) + ' from [' + str(row_block+r2) + ',' + str(c) + '] via linebox (col) at [' + str(row_block+r) + ',' + str(c) + ']'         
                                 candidates[row_block+r2][c].remove(val) 

def rootCandidates(tree, candidates):
   if tree.parent != None:
      return rootCandidates(tree.parent, candidates)
   else:
      return candidates[tree.row][tree.col]

def coveredBy(row, col, row2, col2):
   minR = int(math.floor(row / 3) * 3)
   maxR = int(math.floor(row / 3) * 3) + 3
   minC = int(math.floor(col / 3) * 3)
   maxC = int(math.floor(col / 3) * 3) + 3
   if (row == row2) or (col == col2) or (row2 in range(minR,maxR) and col2 in range(minC,maxC)):
      return 1
   else:
      return 0
                                 
def dfs(tree, row, col, candidates):
   
   if tree.second == tree.getRoot().first:
      
      common_candidate = tree.second
      
      # Should remove if cell is covered by both ends of chain
      for r in range(9):
         for c in range(9):
            if coveredBy(tree.getRoot().row,tree.getRoot().col,r,c) and coveredBy(tree.row,tree.col,r,c) and (common_candidate in candidates[r][c]) and tree.checkParents(r,c):
               print 'XY Chain: root = ' + str(tree.getRoot().row) + ',' + str(tree.getRoot().col) + ', end = ' + str(tree.row) + ',' + str(tree.col)
               print 'Removing common candidate ' + str(common_candidate) + ' from ' + str(r) + ',' + str(c)
               candidates[r][c].remove(common_candidate)      
               
   if len(tree.child) > 0:
         for i in range(len(tree.child)):
            dfs(tree.child[i], row, col, candidates)              
                
def printTree(t):   
   for c in t.child:
      print '[' + str(t.row) + ',' + str(t.col) + '] ' + str(c.row) + '->' + str(c.col)
      printTree(c)
                
def createTree(tree, candidates, row, col): 
   for col2 in range(9):
      if (col2 != col):
         if (len(candidates[row][col2]) == 2):
            if (tree.second in candidates[row][col2]):
               other_candidate = list(set(candidates[row][col2]) - set([tree.second]))[0]
               if tree.addChild(row, col2, tree.second, other_candidate) == 1:
                  createTree(tree.child[-1], candidates, row, col2)
   for row2 in range(9):
      if row2 != row and len(candidates[row2][col]) == 2 and tree.second in candidates[row2][col]:
         other_candidate = list(set(candidates[row2][col]) - set([tree.second]))[0]
         if tree.addChild(row2, col, tree.second, other_candidate) == 1:
            createTree(tree.child[-1], candidates, row2, col)               
   minR = int(math.floor(row / 3)*3)
   maxR = int(math.floor(row / 3)*3 + 3)
   minC = int(math.floor(col / 3)*3)
   maxC = int(math.floor(col / 3)*3 + 3)
   for r in range(minR, maxR):
      for c in range(minC, maxC):
         if (r != row or c != col) and len(candidates[r][c]) == 2 and tree.second in candidates[r][c]:
            other_candidate = list(set(candidates[r][c]) - set([tree.second]))[0]
            if tree.addChild(r, c, tree.second, other_candidate) == 1:
               createTree(tree.child[-1], candidates, r, c)               
                                 
def xyChain(candidates):
   for row in range(9):
      for col in range(9):
         if len(candidates[row][col]) == 2:
            for candidate in candidates[row][col]:
               #print 'Creating tree at ' + str(row) + ',' + str(col) + ' ' + str(candidate)
               s = Set() # Stores pairs of points
               t = Tree(s)
               t.row = row
               t.col = col               
               t.points.add((row,col))
               t.first = candidate
               t.second = list(set(candidates[row][col]) - set([candidate]))[0]
               createTree(t, candidates, row, col)                      
               
               #print '===='            
               #print 'DFS of tree for [' + str(row) + '][' + str(col) + ']:'
               dfs(t, row, col, candidates)
               #print '===='
               #break
 
def twiceInRow(candidates, row, col, candidate):
   count = 1
   for c in range(9):
      if c != col:
         if candidate in candidates[row][c]:
            potential_return = (row,col,row,c)
            count = count + 1
   if count == 2:
      return potential_return
   else:
      return []
      
def twiceInCol(candidates, row, col, candidate):
   count = 1
   for r in range(9):
      if r != row:
         if candidate in candidates[r][col]:
            potential_return = (row,col,r,col)
            count = count + 1
   if count == 2:
      return potential_return
   else:
      return []

def twiceInUnit(candidates, row, col, candidate):
   count = 1
   minR = int(math.floor(row / 3)*3)
   maxR = int(math.floor(row / 3)*3 + 3)
   minC = int(math.floor(col / 3)*3)
   maxC = int(math.floor(col / 3)*3 + 3)   
   for r in range(minR, maxR):
      for c in range(minC, maxC):
         if c != col or r != row:
            if candidate in candidates[r][c]:
               potential_return = (row, col, r, c)
               count = count + 1
   if count == 2:
      return potential_return
   else:
      return []        

def createColoredTree(tree, candidates, candidate):
   p = twiceInRow(candidates, tree.row, tree.col, candidate)
   if p:
      tree.addChild(p[2],p[3])
   p = twiceInCol(candidates, tree.row, tree.col, candidate)
   if p:
      tree.addChild(p[2],p[3])
   p = twiceInUnit(candidates, tree.row, tree.col, candidate)
   if p:
      tree.addChild(p[2],p[3])      

   for c in tree.child:
      createColoredTree(c,candidates,candidate)
  
def seesOne(tree, row, col):
   if coveredBy(tree.row, tree.col, row, col) and tree.color == 1:
      return 1
   
   for c in tree.child:
      if seesOne(c, row, col) == 1:
         return 1
      
   return 0
      
def seesZero(tree, row, col):
   if coveredBy(tree.row, tree.col, row, col) and tree.color == 0:
      return 1
   
   for c in tree.child:
      if seesZero(c, row, col) == 1:
         return 1

   return 0
  
def seesTwoColors(tree, row, col):
   if (seesOne(tree, row, col) == 1) and (seesZero(tree, row, col) == 1):
      return 1
   else:
      return 0      

def printColoredTree(t):
   print '[' + str(t.row) + ',' + str(t.col) + '] ' + str(t.color)
   for c in t.child:
      printColoredTree(c)
      
def simpleColoring(candidates):
   for row in range(9):
      for col in range(9):
         for candidate in candidates[row][col]:         
            treePoints = Set()
            t = ColoredTree(treePoints)
            t.row = row
            t.col = col
            t.points.add((row,col))
            #print 'Creating colored tree, candidate = ' + str(candidate) + ' at ' + str(row) + ',' + str(col)
            createColoredTree(t, candidates, candidate)            
            for r in range(9):
               for c in range(9):
                  if ((r,c) not in t.points) and (candidate in candidates[r][c]) and seesTwoColors(t, r, c):
                     if not twiceInRow(candidates, r, c, candidate) and not twiceInCol(candidates, r, c, candidate) and not twiceInUnit(candidates, r, c, candidate):
                        printColoredTree(t)
                        print 'Removing ' + str(candidate) + ' from ' + str(r) + ',' + str(c) + ' via coloring'
                        candidates[r][c].remove(candidate)
                        return
            #return
         #checkUncovered(candidates, candidate, s)
            
                                 
def eliminateEasyOnes(grid, candidates):
   num_eliminated = 0
   for i in range(9):
      for j in range(9):                         
         cannotBe = findExcludes(grid, i, j)
         for val in cannotBe:
            if val in candidates[i][j]:
               candidates[i][j].remove(val)       
         if grid[i][j] == -1 and len(candidates[i][j]) == 1:        
            print 'Setting [' + str(i) + ',' + str(j) + '] to ' + str(candidates[i][j][0]) + ' via candidates'
            grid[i][j] = candidates[i][j][0]
            candidates[i][j] = []
            num_eliminated += 1
            return num_eliminated
         for num in range(1,10):            
            if grid[i][j] == -1:                  
               if num not in cannotBe and len(cannotBe) == 8:
                  print 'Setting [' + str(i) + ',' + str(j) + '] to ' + str(num) + ' via exclude'                  
                  grid[i][j] = num 
                  candidates[i][j] = []
                  num_eliminated += 1
                  return num_eliminated
            
            if grid[i][j] == -1:
               num_eliminated += useDeductionBlock(grid, i, j, num, candidates)
            
            if grid[i][j] == -1:
               num_eliminated += useDeductionRow(grid, i, j, num, candidates)
            
            if grid[i][j] == -1:
               num_eliminated += useDeductionCol(grid, i, j, num, candidates)
   return num_eliminated
                                 
def printGrid(grid):
   for row in range(9):
      if row == 3 or row == 6:
         print '----------------------'
      for col in range(9):
         if grid[row][col] != -1:         
            sys.stdout.write(str(grid[row][col]))
         else:
            sys.stdout.write('_')
            
         if col == 2 or col == 5:
            sys.stdout.write(' |')                 
            
         if col >= 8:
            sys.stdout.write('\n')
         else:
            sys.stdout.write(' ')

def printCandidates(candidates):
   for row in range(9):
      if row == 3 or row == 6:
         print '----------------------'
      for col in range(9):
         if candidates[row][col] != []:         
            sys.stdout.write(str(len(candidates[row][col])))
         else:
            sys.stdout.write('_')
         
         if col == 2 or col == 5:
            sys.stdout.write(' |')         
            
         if col >= 8:
            sys.stdout.write('\n')
         else:
            sys.stdout.write(' ')

   for row in range(9):
      for col in range(9):
         print '[' + str(row) + '][' + str(col) + '] = ' + str(candidates[row][col])
            
def createGrid():
   grid = [[-1 for x in range(9)] for x in range(9)] 
   
   grid[0][2] = 6
   grid[0][3] = 8
   grid[0][6] = 9
   grid[1][0] = 9
   grid[1][4] = 2
   grid[2][0] = 1
   grid[2][1] = 2
   grid[2][2] = 5
   grid[2][7] = 8
   grid[3][1] = 9
   grid[3][4] = 1
   grid[3][5] = 6
   grid[4][0] = 5
   grid[4][8] = 7
   grid[5][3] = 2
   grid[5][5] = 8
   grid[6][1] = 3
   grid[6][6] = 4
   grid[6][7] = 1
   grid[6][8] = 2
   grid[7][4] = 7
   grid[8][2] = 4
   grid[8][5] = 3
   grid[8][6] = 8
   
   candidates = [[[] for x in range(9)] for x in range(9)]
   for i in range(9):
      for j in range(9):
         if grid[i][j] == -1:
            candidates[i][j] = range(1,10)
   
   # additional
   #grid[0][1] = 7
   #grid[0][5] = 1
   #grid[0][7] = 2
   #grid[0][8] = 5
   #grid[3][3] = 7
   #grid[3][8] = 8
   #grid[4][7] = 6
   #grid[5][4] = 5
   #grid[7][3] = 4
   #grid[7][5] = 2
   #grid[8][0] = 2
   #grid[8][1] = 5
   #grid[8][3] = 1
   #grid[8][7] = 7
   
   # guess
   #grid[5][0] = 6
   #grid[5][2] = 7
   #grid[4][6] = 1
   return grid,candidates
            
def createEmptyGrid():
   grid = [[-1 for x in range(9)] for x in range(9)] 
   
   candidates = [[[] for x in range(9)] for x in range(9)]
   for i in range(9):
      for j in range(9):
         if grid[i][j] == -1:
            candidates[i][j] = range(1,10)
   
   return grid,candidates   
   
def rotateClockwise(grid):
   rotated = [[] for x in range(len(grid))]
   for col in range(len(grid[0])):
      for row in range(len(grid))[::-1]:
         rotated[col].append(grid[row][col])
   return rotated
   
def rotateCounterClockwise(grid):
   rotated = [[] for x in range(len(grid))]
   for col in range(len(grid[0]))[::-1]:
      for row in range(len(grid)):
         rotated[col].append(grid[row][col])
   rotated2 = [row for row in rotated[::-1]]
   return rotated2

def solveGrid(grid):
   [_, candidates] = createEmptyGrid()
   
   print '1 = continue'
   print '0 = exit'
   cmd = raw_input("Enter move: ") 
   
   printGrid(grid)
   while cmd != '0':   
      if eliminateEasyOnes(grid, candidates) > 0:
         print 'Easy methods solved >= 1 square'
      else:  
         removePairs(candidates)
         removeTriples(candidates)
         lineBoxReduction(candidates)
         tempCandidates = rotateClockwise(candidates)
         lineBoxReduction(tempCandidates, 0)      
         candidates = rotateCounterClockwise(tempCandidates)
         xyChain(candidates)
         # removes candidate 5 from [8][8]
         uniqueCandidates(grid, candidates)
         #tempCandidates = rotateClockwise(candidates)
         #tempGrid = rotateClockwise(grid)
         #uniqueCandidates(tempGrid, tempCandidates)
         #grid = rotateCounterClockwise(tempGrid)
         #candidates = rotateCounterClockwise(tempCandidates)
         
         # Need simple coloring to remove some candidates
         # before large chain can set [1,2] to 8
         simpleColoring(candidates)
      
      printGrid(grid)
      count = 0
      for i in range(9):
         count += grid[i].count(-1)
      print str(count) + ' remaining tiles'
      cmd = raw_input("Enter move: ")
   
   #s = Set() # Stores pairs of points
   #t = Tree(s)
   #t.row = 0
   #t.col = 0       
   #t.points.add((0,0))
   #t.first = 3
   #t.second = list(set(candidates[0][0]) - set([3]))[0]
   #createTree(t, candidates, 0, 0)   
   #printTree(t)
   
   printGrid(grid)   
   #print '\nNum Candidates:'
   #printCandidates(candidates)
     
   
def runDemo():
   [grid, candidates] = createGrid()
   
   print '1 = continue'
   print '0 = exit'
   cmd = raw_input("Enter move: ") 
   
   printGrid(grid)
   while cmd != '0':   
      if eliminateEasyOnes(grid, candidates) > 0:
         print 'Easy methods solved >= 1 square'
      else:  
         removePairs(candidates)
         removeTriples(candidates)
         lineBoxReduction(candidates)
         tempCandidates = rotateClockwise(candidates)
         lineBoxReduction(tempCandidates, 0)      
         candidates = rotateCounterClockwise(tempCandidates)
         xyChain(candidates)
         # removes candidate 5 from [8][8]
         uniqueCandidates(grid, candidates)
         #tempCandidates = rotateClockwise(candidates)
         #tempGrid = rotateClockwise(grid)
         #uniqueCandidates(tempGrid, tempCandidates)
         #grid = rotateCounterClockwise(tempGrid)
         #candidates = rotateCounterClockwise(tempCandidates)
         
         # Need simple coloring to remove some candidates
         # before large chain can set [1,2] to 8
         simpleColoring(candidates)
      
      printGrid(grid)
      count = 0
      for i in range(9):
         count += grid[i].count(-1)
      print str(count) + ' remaining tiles'
      cmd = raw_input("Enter move: ")
   
   #s = Set() # Stores pairs of points
   #t = Tree(s)
   #t.row = 0
   #t.col = 0       
   #t.points.add((0,0))
   #t.first = 3
   #t.second = list(set(candidates[0][0]) - set([3]))[0]
   #createTree(t, candidates, 0, 0)   
   #printTree(t)
   
   printGrid(grid)   
   print '\nNum Candidates:'
   printCandidates(candidates)
   

if __name__ == "__main__":
   rumDemo()