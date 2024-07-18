#   ===================
#   Notes: create_index
#       input_file bitmap index string::
#       output_path output bitmap file string::
#       sorted is a boolean value that specifies whether your data will be sorted.
#       16 bits
#       head 4 bits == [’cat’, ’dog’, ’turtle’, ’bird’]  
#           so ex cat is 1000
#       body 10 bits == [1,100] groups of 10 left to right  buckets are 1 to 10, 11 to 20 etc
#           so ex 2 is (1 foloowed by 9 bits 0)
#       tail 2 bits == [True, False]
#           so ex false is 01
#   ==============================================

def create_index(input_file, output_path, sorted):
#   open file path 
    fileInput = open(input_file, 'r')

#   get filename
    parsed_input_file = input_file.split("/")
    fileName = parsed_input_file[len(parsed_input_file)-1]
    
#   check if sorted file or not
    if(sorted == True):
        fileName = fileName + "_sorted"

#   open new file to put data in given path
    output_path = output_path + fileName
    fileOutput = open(output_path,"w")

#   for each line in file
    for line in fileInput:   
        
#       get string//then split by comma// finally clear old string

        stringInput = line
        parsedString = stringInput.split(",")
        
#       reset 
        stringInput = ""
        bitmapString = ""

#       head
#       [’cat’, ’dog’, ’turtle’, ’bird’]  
        if(parsedString[0] == "cat"):
            bitmapString = bitmapString + "1000"
        elif(parsedString[0] == "dog"):
            bitmapString = bitmapString + "0100"
        elif(parsedString[0] == "turtle"):
            bitmapString = bitmapString + "0010"
        elif(parsedString[0] == "bird"):
            bitmapString = bitmapString + "0001"

#       body
        if 0 < int(parsedString[1]) and int(parsedString[1]) <= 10:#  100000
            bucketAge = 1
        elif 10 < int(parsedString[1]) and int(parsedString[1]) <= 20:# 0100000
            bucketAge = 2
        elif 20 < int(parsedString[1]) and int(parsedString[1]) <= 30:# 00100000
            bucketAge = 3
        elif 30 < int(parsedString[1]) and int(parsedString[1]) <= 40:
            bucketAge = 4
        elif 40 < int(parsedString[1]) and int(parsedString[1]) <= 50:
            bucketAge = 5
        elif 50 < int(parsedString[1]) and int(parsedString[1]) <= 60:
            bucketAge = 6
        elif 60 < int(parsedString[1]) and int(parsedString[1]) <= 70:
            bucketAge = 7
        elif 70 < int(parsedString[1]) and int(parsedString[1]) <= 80:
            bucketAge = 8
        elif 80 < int(parsedString[1]) and int(parsedString[1]) <= 90:
            bucketAge = 9
        elif 90 < int(parsedString[1]) and int(parsedString[1]) <= 100:# 000000000001
            bucketAge = 10 

#       create bit and store in bitmapString
        bitAgeString = ""
        for i in range(10):
            if(bucketAge == (i+1)):
                bitAgeString = bitAgeString + "1"
            else:
                bitAgeString = bitAgeString + "0"

        bitmapString = bitmapString + bitAgeString

#       tail adopted yeah or nay
        if(parsedString[2] == "True\n"):
            bitmapString = bitmapString + "10"
        else:
            bitmapString = bitmapString + "01"     
    
#       output to file
        fileOutput.write(bitmapString + "\n")

    fileInput.close()
    fileOutput.close()
#   ===================

#   =====================
#   Notes: compress_index
#       compresses files functions outputRunsZeroes, outputRunsOnes, outputLiteral
#       helps with reading code  
#       def compress_index(bitmap_index, output_path, compression_method, word_size):
#       bitmapindex = file
#       outputpath = path we output file we create too
#       compression method = to WAH or BBC or PLWAH
#       word size = the compression wordSize important for WAH
#   ==========================================================

def outputRunsZeroes(zeroRuns,turnToBinary):
#   set to Runs and set of type 0
    compressedString = "10"
#   set rest to count for rest of string 0wordSIzeb
    compressedString = compressedString + format(zeroRuns, turnToBinary)
#   write to file
    return compressedString
    
def outputRunsOnes(oneRuns, turnToBinary):
#   set to Runs and set of type 1
    compressedString = "11"
#   set rest to count for rest of string
    compressedString = compressedString + format(oneRuns, turnToBinary)
#   write to file
    return compressedString

def outputLiteral(firstBit, word_size, currentFeed):
#   set to Runs and set of type 1
    compressedString = "0" + firstBit
    i = word_size-2
    encodingPtr = 1
    
    while(i!=0):
        compressedString = compressedString + currentFeed[encodingPtr]
        encodingPtr = encodingPtr + 1
        i = i-1
                            
    return compressedString

def compress_index(bitmap_index, output_path, compression_method, word_size):

#   ===========================
#   OPEN FILES INPUT AND OUTPUT
#   open file path and read it
    fileinput = open(bitmap_index, 'r')
    lines = fileinput.readlines()
    
#   get filename
    parsed_input_file = bitmap_index.split("/")
    bitmap_index = parsed_input_file[len(parsed_input_file)-1]

#   BBC
    if(compression_method == "BBC"):
#       open a file with ending file_compressionMethod_wordSize
        compressionName_file = bitmap_index + "_" + compression_method
        output_path = output_path + compressionName_file
        fileOutput =  open(output_path, 'w')
#       ====================================

#   =======
#   FOR WAH
    if(compression_method == "WAH"):
        
#       open a file with ending file_compressionMethod_wordSize
        compressionName_file = bitmap_index + "_" + compression_method + "_" + str(word_size)
        output_path = output_path + compressionName_file
        fileOutput =  open(output_path, 'w')
#       ====================================

#       y do u do dis to me
        totalRUNS =0
        totalLiterals =0
        
#       vars for traversing columns 
        bitmapIndexSize = 16
        column = 0 
        
#       checking if last row
        maxLines = len(lines)
        currentLine =0

#       input and output buffers
        currentFeed = ""
        compressedString = ""
        
#       check for runs var assume true to start
        potRun = True
        
#       reading feed "chunk"
        encodingPtr =0

    #   VARS for run count to binary
        tailCount = word_size-2#accounts for head 11 or 00
        turnToBinary = "0" + str(tailCount) + "b"
        zeroRuns = 0
        oneRuns =0
        
#       POWER FUNCTION and get max runs
        base = 2
        exponent = word_size-2
        result = 1
        for powermyFunction in range(1, exponent+1):
            result = base*result


        maxRuns = result - 1

#       TRAVERSE COLUMNS
#       for each column in the file col output 0 to 15
        for column in range(bitmapIndexSize):
#           start new feed at new col
            currentFeed = ""
            currentLine = 0
            
            for line in lines:
#               get column and increment rowLine
                currentFeed = currentFeed + line[column]
                currentLine = currentLine + 1
                
#               CASE IF ON LAST LINE or GOT WORDSIZE -1 
                if ((currentLine == maxLines) or (len(currentFeed) == (word_size-1))):

#                   assume true to begin with
                    potRun = True
                    firstBit = currentFeed[0]                        

#                   CHECK FOR RUNS
                    if (len(currentFeed) != (word_size-1)):
                        potRun = False
                
                    else: 
#                       read chunk 
                        i = word_size-1
                        encodingPtr = 0# read first one already
                        while(i!=0):
                            if(firstBit != currentFeed[encodingPtr]):
                                potRun = False
                                
                            encodingPtr = encodingPtr + 1  
                            i = i-1
                   
#                   ADD TO RUNS/OUTPUT OR OUTPUTRUNS/ENCODE LITERAL/PAD IF END
                        
#                   if first bit is 1 add to 1Runs 
                    if(firstBit == '1' and potRun == True):
                        oneRuns = oneRuns + 1
                        
#                       check if too many runs 
                        if (oneRuns == maxRuns):
                            compressedString = outputRunsOnes(oneRuns, turnToBinary)
                            fileOutput.write(compressedString)
                            compressedString = ""
                            oneRuns = 0
                                                   
#                       check for old runs output and reset
                        if (zeroRuns > 0):
                            compressedString = outputRunsZeroes(zeroRuns, turnToBinary)
                            fileOutput.write(compressedString)
                            compressedString = ""
                            zeroRuns = 0
                            
#                   else if first bit is 0 add 
                    elif(firstBit == '0' and potRun == True):
                        zeroRuns = zeroRuns + 1
                        
#                       check if too many runs 
                        if (zeroRuns == maxRuns):
                            compressedString = outputRunsZeroes(zeroRuns, turnToBinary)
                            fileOutput.write(compressedString)
                            compressedString = ""
                            zeroRuns = 0
                            
#                       check for old runs output and reset
                        if (oneRuns > 0):
                            compressedString = outputRunsOnes(oneRuns, turnToBinary)
                            fileOutput.write(compressedString)
                            compressedString = ""
                            oneRuns = 0

#                   else its a literal 
                    else:
                        
#                       check for old runs output and reset
                        if (zeroRuns > 0):
                            compressedString = outputRunsZeroes(zeroRuns, turnToBinary)
                            fileOutput.write(compressedString)
                            compressedString = ""
                            zeroRuns = 0
                            
                        if (oneRuns > 0):
                            compressedString = outputRunsOnes(oneRuns, turnToBinary)
                            fileOutput.write(compressedString)
                            compressedString = ""
                            oneRuns = 0
                            
#                       CASE OF NOT FULL WORD PAD
                        if(len(currentFeed)!=(word_size-1)):
#                           get number of needed 0's  for padding
                            OldcurrentFeedSize = len(currentFeed)
                            padZeros = word_size - OldcurrentFeedSize - 1# acc for -1 for literal
                            
                            for sendOff in range(padZeros):
                                currentFeed = currentFeed + "0"

#                       outputLiteral and clear compressed
                        compressedString = outputLiteral(firstBit, word_size, currentFeed) 
                        fileOutput.write(compressedString)
                        compressedString = ""

                    currentFeed = ""
#               ND OF BIG CHUNK OR ENDLINE STATEMENT
#               ====================================

#           END OF COL CLEAR OLD RUNS and go to next line 
            if (zeroRuns > 0):
                compressedString = outputRunsZeroes(zeroRuns, turnToBinary)
                fileOutput.write(compressedString)
                compressedString = ""
                zeroRuns = 0
                            
            if (oneRuns > 0):
                compressedString = outputRunsOnes(oneRuns, turnToBinary)
                fileOutput.write(compressedString)
                compressedString = ""
                oneRuns = 0
                
            fileOutput.write("\n")
                    
#   END OF WAH
#   ==========
    
    
#   ====================
#   CLOSE FILES AND DONE 
    fileOutput.close()
    fileinput.close()    
    
#Def compress_index
#   ==============