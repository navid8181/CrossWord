import re


def initializeBlocks(blocks=[],ROW=5,COL=5) :
    for i in range (ROW) :
        col = [];
        for i in range (COL) :
            col.append("")
        

        blocks.append(col)    

def printArray(arr=[]):
    for i in range(len(arr)) :
        for j in  range (len(arr[0])) :
            print (arr[i][j],end=' ')
        print('\n')

def setHorizontalValues (i,j,x1,x2,blocks=[[]],values=[]) :
    
    length = x2-x1+1
    
    if len(values) != length :
        raise Exception("length of values not equal to range of x1 and x2")
    valuesIndex = 0
    for k in range (length) :
        blocks[i][k+j] = values[valuesIndex]    
        valuesIndex  += 1

def getHorizontalValues (i,j,x1,x2,blocks=[[]]) :
    
    values = []
    
    length = x2-x1+1

   
    for k in range (length) :
       values.append( blocks[i][k+j])   
      
    return values     

def setVerticalValues (i,j,y1,y2,blocks=[[]],values=[]) :
    
    length = y2-y1+1
    
    if len(values) != length :
        raise Exception("length of values not equal to range of x1 and x2")
    valuesIndex = 0
    for k in range (length) :
        blocks[k+i][j] = values[valuesIndex]    
        valuesIndex  += 1 

def getVerticalValues (i,j,y1,y2,blocks=[[]]) :
    
    length = y2-y1+1
    
    values = []

    for k in range (length) :
        values.append(blocks[k+i][j])

    return values
    
def getHorizontalRangeIndex(i,j,blocks=[[]]):
    rightIndex = j
    leftIndex = j
    while   rightIndex < len(blocks[0]) and blocks[i][rightIndex] !='#' :
        rightIndex +=1
    
    while   leftIndex > 0 and blocks[i][leftIndex] !='#'  :
        leftIndex -=1        

    rightIndex = min (rightIndex,len(blocks[0])-1)
    leftIndex = max (leftIndex,0)
    
    if blocks[i][rightIndex] =='#' :
        rightIndex -= 1
    
    if blocks[i][leftIndex] =='#':
        leftIndex +=1
    
    return (leftIndex,rightIndex)

def getVerticalRangeIndex(i,j,blocks=[[]]):
        upperIndex = i
        bottomIndex = i
        
        while   upperIndex < len(blocks) and blocks[upperIndex][j] !='#' :
            upperIndex +=1
        
        while   bottomIndex > 0 and blocks[bottomIndex][j] !='#' :
            bottomIndex -=1
            
        upperIndex = min (upperIndex,len(blocks)-1)
        bottomIndex = max (bottomIndex,0)    
        
        if blocks[upperIndex][j] == '#':
            upperIndex -= 1
        if blocks[bottomIndex][j] == '#':
            bottomIndex +=1    
        
        return (bottomIndex,upperIndex)

def searchInArray (regex="",input=[]):
    output = []
    for i in range(len(input)):
        x = re.search(regex,input[i])
        
        if x :
            output.append(input[i])
    return output

def getHorizontalRegexValid(i,j,blocks=[[]]) :
    # for j
    left,right = getHorizontalRangeIndex(i,j,blocks)
    
    horizontalValidRegexValue = "^"
    for k in range(left,right+1,1) :
        if blocks[i][k] != '-' :
            horizontalValidRegexValue += blocks[i][k]
        else :
              horizontalValidRegexValue+='.'
    
    horizontalValidRegexValue +="$"            
    return  horizontalValidRegexValue 


def getVerticalRegexValid(i,j,blocks=[[]]) :
    # for j
    bottom,upper = getVerticalRangeIndex(i,j,blocks)
    
    verticalValidRegexValue = "^"
    for k in range(bottom,upper+1,1) :
        if blocks[k][j] != '-' :
            verticalValidRegexValue += blocks[k][j]
        else :
              verticalValidRegexValue+='.'
    
    verticalValidRegexValue +="$"                
    return  verticalValidRegexValue  


def getHorizontalWordCandidate(i,j,blocks=[[]],input=[]):
    
    leftIndex,rightIndex = getHorizontalRangeIndex(i,j,blocks)
    horizontalRegex = getHorizontalRegexValid(i,j,blocks)
    horizontalValidWords = searchInArray(horizontalRegex,input)
    
    lastValues = getHorizontalValues(i,leftIndex,leftIndex,rightIndex,blocks)
    candidateWords = []
    
    for idx in range(len(horizontalValidWords)) :
        isCandidate = True
        values = [char for char in horizontalValidWords[idx]]
    
        setHorizontalValues(i,leftIndex,leftIndex,rightIndex,blocks,values)

        length = rightIndex - leftIndex + 1
        
        for k in range(length) :
            upper,bottom = getVerticalRangeIndex(i,k+leftIndex,blocks)
            if upper == bottom :
                continue
            verticalRegex = getVerticalRegexValid(i,k+leftIndex,blocks)
            if (len(searchInArray(verticalRegex,input)) == 0) :
                isCandidate = False
                break
        
        if isCandidate :
            candidateWords.append(horizontalValidWords[idx])
    
    setHorizontalValues(i,leftIndex,leftIndex,rightIndex,blocks,lastValues)
    return candidateWords   



def getVerticalWordCandidate(i,j,blocks=[[]],input=[]):
    
    bottom,upper = getVerticalRangeIndex(i,j,blocks)
    verticalRegex = getVerticalRegexValid(i,j,blocks)
    verticalValidWords = searchInArray(verticalRegex,input)
    
    lastValues = getVerticalValues(bottom,j,bottom,upper,blocks)
    candidateWords = []
    
    for idx in range(len(verticalValidWords)) :
        isCandidate = True
        values = [char for char in verticalValidWords[idx]]
    
        setVerticalValues(bottom,j,bottom,upper,blocks,values)

        length = upper - bottom + 1    
        

        for k in range(length) :
            left,right = getHorizontalRangeIndex(k+bottom,j,blocks)
            if left == right :
                continue
            horizontalRegex = getHorizontalRegexValid(k+bottom,j,blocks)
            if (len(searchInArray(horizontalRegex,input)) == 0) :
                isCandidate = False
                break
        
        if isCandidate :
            candidateWords.append(verticalValidWords[idx])
    
    setVerticalValues(bottom,j,bottom,upper,blocks,lastValues)
    return candidateWords         
 
def getNextIndex (i,j,blocks=[[]]):
    for i in range(len(blocks)) :
        for j in  range (len(blocks[0])) :
            
            if (blocks[i][j] == '-'):
                return (i,j)
    
    return (-1,-1)
   

def getCount (i,j,blocks=[[]]):
    count = 0
    for i in range(len(blocks)) :
        for j in  range (len(blocks[0])) :
            
            if (blocks[i][j] == '-'):
                count +=1  
    return count    
    
def crossWordSolver(i,j,blocks=[[]],input=[],count=20) :
    
    if count == 0 :
        print("win")
        return
    
    for word in getHorizontalWordCandidate(i,j,blocks,input) :
        
         leftIndex,rightIndex = getHorizontalRangeIndex(i,j,blocks) 
         values = [char for char in word]
         setHorizontalValues(i,leftIndex,leftIndex,rightIndex,blocks,values)   
         realLength = rightIndex - j + 1
         x,y = getNextIndex(i,j,blocks)  
         
         
         crossWordSolver(x,y,blocks,input,count - realLength) 
         
         if count == 0 :
             return
         
         count += realLength
         values = ['-'] * realLength
         
         setHorizontalValues(i,j,1,realLength,blocks,values)   
    


    for word in getVerticalWordCandidate(i,j,blocks,input) :
        
         bottom,upper = getVerticalRangeIndex(i,j,blocks) 
         values = [char for char in word]
         
         setVerticalValues(bottom,j,bottom,upper,blocks,values)   
         
         realLength = upper - i + 1
         x,y = getNextIndex(i,j,blocks)  
         
         
         crossWordSolver(x,y,blocks,input,count - realLength) 
         
         if count == 0 :
             return
         
         count += realLength
         values = ['-'] * realLength
         
         setVerticalValues(i,j,1,realLength,blocks,values)     


    return


ROW,COL = (5,5)
input = ["drat","rat","bat","cat","at","arc","this","that","can"]

# blocks = [
#           ['-','-','-','-','#'],
#           ['-','-','-','#','-'],
#           ['-','-','-','#','-'],
#           ['-','#','#','#','-'],
#           ['#','-','-','-','-'],
#         ]


blocks = [
          ['-','-','-','#','#'],
          ['-','#','-','#','-'],
          ['-','-','-','#','-'],
          ['#','#','#','#','-'],
          ['#','-','-','-','-'],
        ]

#initializeBlocks(blocks,ROW,COL)
#setVerticalValues(0,0,0,3,blocks,['*',"*","*","*"])
#printArray(blocks)
#print(getHorizontalRangeIndex(1,0,blocks))
#print(getHorizontalRegexValid(0,0,blocks))
#print(getVerticalRegexValid(0,1,blocks))


#setHorizontalValues(0,0,0,3,blocks,['d','r','a','t'])
#print(getNextIndex(0,0,blocks))
#print(getHorizontalWordCandidate(0,3,blocks,input))
#print(getVerticalWordCandidate(4,4,blocks,input))
count = getCount(0,0,blocks)

crossWordSolver(0,0,blocks,input,count)
printArray(blocks)