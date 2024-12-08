import re

#ایجاد آرایه دوبعدی
def initializeBlocks(blocks=[],ROW=5,COL=5) :
    for i in range (ROW) :
        col = [];
        for i in range (COL) :
            col.append("")
        

        blocks.append(col)    

#چاپ آرایه
def printArray(arr=[]):
    for i in range(len(arr)) :
        for j in  range (len(arr[0])) :
            print (arr[i][j],end=' ')
        print('\n')
#قرار دادن کلمات به روش افقی در ارایه
def setHorizontalValues (i,j,x1,x2,blocks=[[]],values=[]) :
    
    length = x2-x1+1
    
    if len(values) != length :
        raise Exception("length of values not equal to range of x1 and x2")
    valuesIndex = 0
    for k in range (length) :
        blocks[i][k+j] = values[valuesIndex]    
        valuesIndex  += 1
#گرفتن کلمات به صورت افقی
def getHorizontalValues (i,j,x1,x2,blocks=[[]]) :
    
    values = []
    
    length = x2-x1+1

   
    for k in range (length) :
       values.append( blocks[i][k+j])   
      
    return values     

#قرار دادن کلمات به روش عمودی در ارایه
def setVerticalValues (i,j,y1,y2,blocks=[[]],values=[]) :
    
    length = y2-y1+1
    
    if len(values) != length :
        raise Exception("length of values not equal to range of x1 and x2")
    valuesIndex = 0
    for k in range (length) :
        blocks[k+i][j] = values[valuesIndex]    
        valuesIndex  += 1 
#گرفتن کلمات به صورت عموذی
def getVerticalValues (i,j,y1,y2,blocks=[[]]) :
    
    length = y2-y1+1
    
    values = []

    for k in range (length) :
        values.append(blocks[k+i][j])

    return values
  
  #گرفتن  ابتدا و انتهای بین دو (# #) در آرایع به صورت افقی  

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

#گرفتن  ابتدا و انتهای بین دو (# #) در آرایع به صورت عموددی  

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


#سرجچ در آرایه  input 
#با یک ریجکس خاص
def searchInArray (regex="",input=[]):
    output = []
    for i in range(len(input)):
        x = re.search(regex,input[i])
        
        if x :
            output.append(input[i])
    return output

#گرفتن ریجکس آن سطر برای هندل کردن کلمات مناسب آن سطر
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

#گرفتن ریجکس آن ستون برای هندل کردن کلمات مناسب آن ستون
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

#به درست آوردن کلمات مناسب یک سطر
#روس به این شکل کلمه باید مناسب آن سطر انتخاب شده باشه
#بع ازای هر حرف باید با ستون خود هم هماهنک باشع
def getHorizontalWordCandidate(i,j,blocks=[[]],input=[]):
    
    leftIndex,rightIndex = getHorizontalRangeIndex(i,j,blocks)
    horizontalRegex = getHorizontalRegexValid(i,j,blocks)
    horizontalValidWords = searchInArray(horizontalRegex,input)
    
    #گرفتن مفادیر مناسب هر سطح
    lastValues = getHorizontalValues(i,leftIndex,leftIndex,rightIndex,blocks)
    candidateWords = []
    #بع ازای هرکلمه
    for idx in range(len(horizontalValidWords)) :
        isCandidate = True
        values = [char for char in horizontalValidWords[idx]]

        #ست کردن آن
        setHorizontalValues(i,leftIndex,leftIndex,rightIndex,blocks,values)

        length = rightIndex - leftIndex + 1
        #چک کردن آیا با ستون هماهنک هست هر حرف یا نه
        for k in range(length) :
            upper,bottom = getVerticalRangeIndex(i,k+leftIndex,blocks)
            if upper == bottom :
                continue
            verticalRegex = getVerticalRegexValid(i,k+leftIndex,blocks)
            if (len(searchInArray(verticalRegex,input)) == 0) :
                isCandidate = False
                break
        #اضافع به لیست کلمات قابل انتخاب
        if isCandidate :
            candidateWords.append(horizontalValidWords[idx])
    
    setHorizontalValues(i,leftIndex,leftIndex,rightIndex,blocks,lastValues)
    return candidateWords   


#مثل بالا فقط بزعکس
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
#گرفتن ایندکس بعدی  پر نشده
def getNextIndex (i,j,blocks=[[]]):
    for i in range(len(blocks)) :
        for j in  range (len(blocks[0])) :
            
            if (blocks[i][j] == '-'):
                return (i,j)
    
    return (-1,-1)
   
#گرفتن تعداد ستون ها پر نشده
def getCount (i,j,blocks=[[]]):
    count = 0
    for i in range(len(blocks)) :
        for j in  range (len(blocks[0])) :
            
            if (blocks[i][j] == '-'):
                count +=1  
    return count    
   
#حل جدول    
#جدول یا به حالت افقی حل می شود با عمودی
def crossWordSolver(i,j,blocks=[[]],input=[],count=20) :
    
    #جدول به طرز کامل پر شده است
    if count == 0 :

        return True
    #به ازای هر کلمه ای که می توان در سطر افقی گزاشت
    for word in getHorizontalWordCandidate(i,j,blocks,input) :
        
         leftIndex,rightIndex = getHorizontalRangeIndex(i,j,blocks) 
         values = [char for char in word]
         
         # به دست آوردن مقادیر جاگزاری شده
         changedValues = []
         for chgVal in range(rightIndex - leftIndex + 1 ):
             if blocks[i][leftIndex + chgVal] == '-' :
                changedValues.append((i,leftIndex+chgVal))
         
         #اضافه کردن کلمه
         
         setHorizontalValues(i,leftIndex,leftIndex,rightIndex,blocks,values)  
         #محاسبه ی اندازع واقعی کلمات تغییر کرده 
         realLength = len(changedValues)
         #گرفتن حفره خالی بعدی که مسیله حل نشده
         x,y = getNextIndex(i,j,blocks)  
         #به دست آوردن نعداد خانه های پر نشده
         count = count - realLength
         #حل مسیله برای خانه بعدی بع صورت بازگشتی
         check = crossWordSolver(x,y,blocks,input,count) 
         #نشان دادن جواب در صورت پیدا شدن
         if (check) :
             return True
         

         #اضافه کردن خانه به درخت در صورت شکسته خوردن در حل مسیله
         count += realLength
        #برگردادن جدول بع حالت قبل و امتحان حالت ها ی دیگر
         for (l,m) in changedValues :
             blocks[l][m] = '-'
    

    #شبیه بالا برای حل جدول به صورت عمودی
    for word in getVerticalWordCandidate(i,j,blocks,input) :
        
         bottom,upper = getVerticalRangeIndex(i,j,blocks) 
         values = [char for char in word]
         
         changedValues = []
         for chgVal in range(upper - bottom + 1 ):
             if blocks[bottom + chgVal][j] == '-' :
                changedValues.append((bottom+chgVal,j))
         
         setVerticalValues(bottom,j,bottom,upper,blocks,values)   
         
         realLength =len(changedValues)
         x,y = getNextIndex(i,j,blocks)  
         
         count = count - realLength
         check = crossWordSolver(x,y,blocks,input,count) 
         
         if (check):
             return True
         

         
         count += realLength
         for (l,m) in changedValues :
             blocks[l][m] = '-'
         
         

    return False


ROW,COL = (5,5)
input = ["drat","rat","bat","cat","at","arc","this","that","can", "atm"]

blocks = [
          ['-','-','-','-','#'],
          ['-','-','-','#','-'],
          ['-','-','-','#','-'],
          ['-','#','#','#','-'],
          ['#','-','-','-','-'],
        ]


# blocks = [
#           ['#','-','-','-','#'],
#           ['-','-','-','#','-'],
#           ['-','-','-','#','-'],
#           ['-','#','#','#','-'],
#           ['#','-','-','#','-'],
#         ]



# blocks = [
#           ['-','-','-','#','#'],
#           ['-','#','-','#','-'],
#           ['-','-','-','#','-'],
#           ['#','#','#','#','-'],
#           ['#','-','-','-','-'],
#         ]


count = getCount(0,0,blocks)

(i,j) = getNextIndex(0,0,blocks)
#حل مسیله
cehck = crossWordSolver(i,j,blocks,input,count)
printArray(blocks)
if cehck == False :
    print("Not found")