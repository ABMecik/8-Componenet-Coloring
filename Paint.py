import tkinter
from tkinter.colorchooser import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import Image, ImageTk, ImageTransform, ImageQt
import PIL
import random

# Author: Artun Burak Meçik
# Since: 03.03.2018
# Version: 2.0

#Create basic gui with size of 800x600
window = Tk() #Define basic gui interface
window.iconbitmap(r'.\\buttons\\title.ico') #Program gui icon
window.title("Paint") #Program name
window.geometry("800x600") #Gui start size
window.configure(background='white') #Gui default background color

# ***************Global Operators********************
#global variables

choosenColor=(0,0,0) #Standard selected color
backColor=(0,0,0) #Undo and redo, color saver
img = Label(window) #Define basic image board on window
openedImage=None #Opened image
#Images width and height
rowSize=0
columnSize=0
pix=None #Opened image as a pixel map
labelValue=None #Opened image as a labeled map according to siyah beyaz pixel map
pixelValue=None #Black and white pixel map
#Undo and redo veriables
undoColor = [] #Color
undoX = [] #X coordinate
undoY = [] #Y coordinate
undoType=[] #Undo type
undoOldLabel=[] #Old label value
undoNewLabel=[] #New label value
redoColor = []
redoX = []
redoY = []
redoType=[]
redoOldLabel=[]
redoNewLabel=[]
operation=(0, 0, 0) #Operation code, example : (0, 0, 1) -> color fill
#choosenColor RGB values
colorR=0
colorG=0
colorB=0
brushSize=1 #Color brush size
labelCount = 2 #Label count

defImg = ImageTk.PhotoImage(file= ".\\buttons\\logo.png") #Mef University logo
img.config(image=defImg)
img.image = defImg
img.place(x=160, y=60) #Set images [0][0] -> first pixel coordinate


# ***************MENU OPERATION********************

def openFile(): #Read image file
    reset() #On top-up images, delete the previous image
    openFileFormats = (("all files", "*.*"), ("png files", "*.png"), ("gif files", "*.gif"), ("jpeg files", "*.jpg")) #File formats for easy search
    path = askopenfilename(parent = window, filetypes = openFileFormats) #Basic file pick gui
    fp = open(path, "rb") #Read file as a byte map
    global openedImage
    openedImage = Image.open(fp) #Byte map to images
    imageProcess()

def imageProcess():
    global pix
    pix = openedImage.load() #Images to pixel map
    global rowSize,columnSize
    rowSize,columnSize=openedImage.size #Get images width and height
    print(rowSize,columnSize)
    for i in range(rowSize):
        for j in range(columnSize):
            pix[i,j] = cleanNoise(pix[i,j]) # Clean gray pixels -> Black/White image
            if (i == 0) or (j == 0) or (i == rowSize-1) or (j == columnSize-1):
                pix[i, j] = (0, 0, 0) #Frames with formal black


    global pixelValue
    pixelValue = [[0 for x in range(columnSize)] for y in range(rowSize)] #Set pixelValue sizes

    for i in range(1,rowSize-1):
        for j in range(1,columnSize-1):
            pixelValue[i][j]=convertToBinary(pix[i, j]) #Give value to pixels -> White:1 and Black:0

    global labelValue
    labelValue = [[0 for x in range(columnSize)] for y in range(rowSize)] #Set labelValue sizes

    for i in range(rowSize):
        for j in range(columnSize):
            labelValue[i][j] = 0 #Be 0 to all label array values

    #4-C labeling - WORK
    #for i in range(1, rowSize - 1):
    #    for j in range(1, columnSize - 1):
    #        if pixelValue[i][j] == 1:
    #            if pixelValue[i - 1][j] == 1 and pixelValue[i][j - 1] == 1:
    #                if labelValue[i - 1][j] == labelValue[i][j - 1]:
    #                    labelValue[i][j] = labelValue[i][j - 1]
    #                else:
    #                    labelValue[i][j] = labelValue[i - 1][j]
    #                    for t in range(0, i + 1):
    #                       for k in range(0, j + 1):
    #                           if labelValue[t][k] == labelValue[i][j - 1]:
    #                               labelValue[t][k] = labelValue[i - 1][j]
    #           elif pixelValue[i - 1][j] == 1 or pixelValue[i][j - 1] == 1:
    #               if pixelValue[i - 1][j] == 1:
    #                   labelValue[i][j] = labelValue[i - 1][j]
    #               else:
    #                   labelValue[i][j] = labelValue[i][j - 1]
    #           else:
    #               labelValue[i][j] = labelCount
    #               labelCount += 1
    #       else:
    #           labelValue[i][j] = 1


    global labelCount
    # 8-C labeling
    #The labels of non-black faces are evaluate, which first attach importance to the ethics of the left after the top.
    #1111-0111-1011-1101-1110-1100-1010-1001-0110-0101-0011-1000-0100-0010-0001-0000
    for i in range(1, rowSize - 1):
        for j in range(1, columnSize - 1):
            #Help to understand:
            #leftPixel = pixelValue[i][j - 1]
            #upLeftPixel = pixelValue[i - 1][j - 1]
            #upPixel = pixelValue[i - 1][j]
            #upRightPixel = pixelValue[i - 1][j + 1]
            #locationPixel = pixelValue[i][j]
            #leftLabel = labelValue[i][j - 1]
            #upLeftLabel = labelValue[i - 1][j - 1]
            #upLabel = labelValue[i - 1][j]
            #upRightLabel = labelValue[i - 1][j + 1]
            #locationLabel = labelValue[i][j]

            if pixelValue[i][j] == 1:
                if (pixelValue[i][j - 1] == 1) or (pixelValue[i - 1][j - 1] == 1) or (pixelValue[i - 1][j] == 1) or (pixelValue[i - 1][j + 1] == 1):

                    #4-1***************************************************************
                    if (pixelValue[i][j - 1] == 1) and (pixelValue[i - 1][j - 1] == 1) and (pixelValue[i - 1][j] == 1) and (pixelValue[i - 1][j + 1] == 1):
                        if labelValue[i][j - 1] == labelValue[i - 1][j - 1] == labelValue[i - 1][j] == labelValue[i - 1][j + 1]:
                            labelValue[i][j] = labelValue[i - 1][j - 1]
                        else:
                            labelValue[i][j] = labelValue[i - 1][j - 1]
                            for t in range(0, i + 1):
                                for k in range(0, columnSize - 1):
                                    if labelValue[t][k] == labelValue[i][j - 1]:
                                        labelValue[t][k] = labelValue[i - 1][j - 1]
                                    elif labelValue[t][k] == labelValue[i - 1][j]:
                                        labelValue[t][k] = labelValue[i - 1][j - 1]
                                    elif labelValue[t][k] == labelValue[i - 1][j + 1]:
                                        labelValue[t][k] = labelValue[i - 1][j - 1]

                    #3-1***************************************************************
                    elif (pixelValue[i][j - 1] == 0) and (pixelValue[i - 1][j - 1] == 1) and (pixelValue[i - 1][j] == 1) and (pixelValue[i - 1][j + 1] == 1):
                        if labelValue[i - 1][j - 1] == labelValue[i - 1][j] == labelValue[i - 1][j + 1]:
                            labelValue[i][j] = labelValue[i - 1][j - 1]
                        else:
                            labelValue[i][j] = labelValue[i - 1][j - 1]
                            for t in range(0, i + 1):
                                for k in range(0, columnSize - 1):
                                    if labelValue[t][k] == labelValue[i - 1][j]:
                                        labelValue[t][k] = labelValue[i - 1][j - 1]
                                    elif labelValue[t][k] == labelValue[i - 1][j + 1]:
                                        labelValue[t][k] = labelValue[i - 1][j - 1]

                    elif (pixelValue[i][j - 1] == 1) and (pixelValue[i - 1][j - 1] == 0) and (pixelValue[i - 1][j] == 1) and (pixelValue[i - 1][j + 1] == 1):
                        if labelValue[i][j - 1] == labelValue[i - 1][j] == labelValue[i - 1][j + 1]:
                            labelValue[i][j] = labelValue[i - 1][j]
                        else:
                            labelValue[i][j] = labelValue[i - 1][j]
                            for t in range(0, i + 1):
                                for k in range(0, columnSize - 1):
                                    if labelValue[t][k] == labelValue[i][j - 1]:
                                        labelValue[t][k] = labelValue[i - 1][j]
                                    elif labelValue[t][k] == labelValue[i - 1][j + 1]:
                                        labelValue[t][k] = labelValue[i - 1][j]

                    elif (pixelValue[i][j - 1] == 1) and (pixelValue[i - 1][j - 1] == 1) and (pixelValue[i - 1][j] == 0) and (pixelValue[i - 1][j + 1] == 1):
                        if labelValue[i][j - 1] == labelValue[i - 1][j - 1] == labelValue[i - 1][j + 1]:
                            labelValue[i][j] = labelValue[i - 1][j - 1]
                        else:
                            labelValue[i][j] = labelValue[i - 1][j - 1]
                            for t in range(0, i + 1):
                                for k in range(0, columnSize - 1):
                                    if labelValue[t][k] == labelValue[i][j - 1]:
                                        labelValue[t][k] = labelValue[i - 1][j - 1]
                                    elif labelValue[t][k] == labelValue[i - 1][j + 1]:
                                        labelValue[t][k] = labelValue[i - 1][j - 1]

                    elif (pixelValue[i][j - 1] == 1) and (pixelValue[i - 1][j - 1] == 1) and (pixelValue[i - 1][j] == 1) and (pixelValue[i - 1][j + 1] == 0):
                        if labelValue[i][j - 1] == labelValue[i - 1][j - 1] == labelValue[i - 1][j]:
                            labelValue[i][j] = labelValue[i - 1][j - 1]
                        else:
                            labelValue[i][j] = labelValue[i - 1][j - 1]
                            for t in range(0, i + 1):
                                for k in range(0, columnSize - 1):
                                    if labelValue[t][k] == labelValue[i][j - 1]:
                                        labelValue[t][k] = labelValue[i - 1][j - 1]
                                    elif labelValue[t][k] == labelValue[i - 1][j]:
                                        labelValue[t][k] = labelValue[i - 1][j - 1]

                    #2-1***************************************************************
                    elif (pixelValue[i][j - 1] == 1) and (pixelValue[i - 1][j - 1] == 1) and (pixelValue[i - 1][j] == 0) and (pixelValue[i - 1][j + 1] == 0):
                        if labelValue[i][j - 1] == labelValue[i - 1][j - 1]:
                            labelValue[i][j] = labelValue[i - 1][j - 1]
                        else:
                            labelValue[i][j] = labelValue[i - 1][j - 1]
                            for t in range(0, i + 1):
                                for k in range(0, columnSize - 1):
                                    if labelValue[t][k] == labelValue[i][j - 1]:
                                        labelValue[t][k] = labelValue[i - 1][j - 1]

                    elif (pixelValue[i][j - 1] == 1) and (pixelValue[i - 1][j - 1] == 0) and (pixelValue[i - 1][j] == 1) and (pixelValue[i - 1][j + 1] == 0):
                        if labelValue[i][j - 1] == labelValue[i - 1][j]:
                            labelValue[i][j] = labelValue[i - 1][j]
                        else:
                            labelValue[i][j] = labelValue[i - 1][j]
                            for t in range(0, i + 1):
                                for k in range(0, columnSize - 1):
                                    if labelValue[t][k] == labelValue[i][j - 1]:
                                        labelValue[t][k] = labelValue[i - 1][j]

                    elif (pixelValue[i][j - 1] == 1) and (pixelValue[i - 1][j - 1] == 0) and (pixelValue[i - 1][j] == 0) and (pixelValue[i - 1][j + 1] == 1):
                        if labelValue[i][j - 1] == labelValue[i - 1][j + 1]:
                            labelValue[i][j] = labelValue[i - 1][j + 1]
                        else:
                            labelValue[i][j] = labelValue[i - 1][j + 1]
                            for t in range(0, i + 1):
                                for k in range(0, columnSize - 1):
                                    if labelValue[t][k] == labelValue[i][j - 1]:
                                        labelValue[t][k] = labelValue[i - 1][j + 1]

                    elif (pixelValue[i][j - 1] == 0) and (pixelValue[i - 1][j - 1] == 1) and (pixelValue[i - 1][j] == 1) and (pixelValue[i - 1][j + 1] == 0):
                        if labelValue[i - 1][j - 1] == labelValue[i - 1][j]:
                            labelValue[i][j] = labelValue[i - 1][j - 1]
                        else:
                            labelValue[i][j] = labelValue[i - 1][j - 1]
                            for t in range(0, i + 1):
                                for k in range(0, columnSize - 1):
                                    if labelValue[t][k] == labelValue[i - 1][j]:
                                        labelValue[t][k] = labelValue[i - 1][j - 1]

                    elif (pixelValue[i][j - 1] == 0) and (pixelValue[i - 1][j - 1] == 1) and (pixelValue[i - 1][j] == 0) and (pixelValue[i - 1][j + 1] == 1):
                        if labelValue[i - 1][j - 1] == labelValue[i - 1][j + 1]:
                            labelValue[i][j] = labelValue[i - 1][j - 1]
                        else:
                            labelValue[i][j] = labelValue[i - 1][j - 1]
                            for t in range(0, i + 1):
                                for k in range(0, columnSize - 1):
                                    if labelValue[t][k] == labelValue[i - 1][j + 1]:
                                        labelValue[t][k] = labelValue[i - 1][j - 1]

                    elif (pixelValue[i][j - 1] == 0) and (pixelValue[i - 1][j - 1] == 0) and (pixelValue[i - 1][j] == 1) and (pixelValue[i - 1][j + 1] == 1):
                        if labelValue[i - 1][j] == labelValue[i - 1][j + 1]:
                            labelValue[i][j] = labelValue[i - 1][j]
                        else:
                            labelValue[i][j] = labelValue[i - 1][j]
                            for t in range(0, i + 1):
                                for k in range(0, columnSize - 1):
                                    if labelValue[t][k] == labelValue[i - 1][j + 1]:
                                        labelValue[t][k] = labelValue[i - 1][j]

                    #1-1***************************************************************
                    elif (pixelValue[i][j - 1] == 1) and (pixelValue[i - 1][j - 1] == 0) and (pixelValue[i - 1][j] == 0) and (pixelValue[i - 1][j + 1] == 0):
                        labelValue[i][j] = labelValue[i][j - 1]
                    elif (pixelValue[i][j - 1] == 0) and (pixelValue[i - 1][j - 1] == 1) and (pixelValue[i - 1][j] == 0) and (pixelValue[i - 1][j + 1] == 0):
                        labelValue[i][j] = labelValue[i - 1][j - 1]
                    elif (pixelValue[i][j - 1] == 0) and (pixelValue[i - 1][j - 1] == 0) and (pixelValue[i - 1][j] == 1) and (pixelValue[i - 1][j + 1] == 0):
                        labelValue[i][j] = labelValue[i - 1][j]
                    elif (pixelValue[i][j - 1] == 0) and (pixelValue[i - 1][j - 1] == 0) and (pixelValue[i - 1][j] == 0) and (pixelValue[i - 1][j + 1] == 1):
                        labelValue[i][j] = labelValue[i - 1][j + 1]

                else:
                    labelValue[i][j] = labelCount
                    labelCount += 1
            else:
                labelValue[i][j] = 1

            print(labelValue[i][j], end='')#Print label map
        print("")




    for j in range(1,columnSize - 1):
        for i in range(1, rowSize - 1):
            print(pixelValue[i][j], end='')#Print w/b pixel map
        print("")

    #Set/update and print image
    render = ImageTk.PhotoImage(openedImage)
    img.config(image=render)
    img.image = render
    img.update()
    print("img size:","height size=",rowSize,"and width size=",columnSize)

def convertToBinary(Value):
    #Create w/b pixel map - binary map
    if len(Value) == 4:
        r, g, b, op = Value #opacity
    else:
        r, g, b = Value

    average = (r + g + b) / 3

    if average == 255:
        return 1
    else:
        return 0

def cleanNoise(Value):
    #Clean gray pixel according to RGB average
    global isImgOpened
    if len(Value) == 4: #opacity
        r, g, b, op = Value
    else:
        r, g, b = Value

    average = (r + g + b) / 3

    if average > 200:
        return 255, 255, 255
    else:
        return 0, 0, 0


def saveFile():
    #File save
    global openedImage
    saveFileFormats = (("png files", "*.png"), ("all files", "*.*"))
    output = asksaveasfile(mode = 'wb', parent =window, filetypes = saveFileFormats, title = 'Export File', defaultextension = '.png')#Default save type *.png
    openedImage.save(output)

def addPast(x,y,type): #Mouse click coordinates and process type
    #Save process to past -> undo veriables
    global pix
    global undoColor
    global undoX
    global undoY
    global labelValue
    global undoType
    global undoOldLabel
    global undoNewLabel

    if len(pix[x,y]) == 4:
        r,g,b,opa=pix[x,y]
    else:
        r,g,b=pix[x,y]

    undoColor.append((r, g, b))
    undoX.append(x)
    undoY.append(y)
    undoOldLabel.append(labelValue[x][y])
    undoNewLabel.append(labelCount)
    undoType.append(type)
    print("History ", "x=", x, "y=", y, " and color=", choosenColor)

def undo():#undo
    global undoColor
    global undoX
    global undoY
    global redoColor
    global redoX
    global redoY
    global labelValue
    global openedImage
    global img
    global pix
    global choosenColor
    global redoColor
    global redoX
    global redoY
    global undoType
    global undoOldLabel
    global redoType
    global redoOldLabel
    global undoNewLabel
    global redoNewLabel

    if len(undoX) > 0:

        if undoType[len(undoX) - 1] == 1: #undo typing for fill color
            print("undo", "type=", undoType[len(undoX) - 1], "x=", undoX[len(undoX) - 1], "y=", undoY[len(undoX) - 1],
                  " and color=", undoColor[len(undoX) - 1])

            #take last process infos.
            unX = undoX[len(undoX) - 1]
            unY = undoY[len(undoX) - 1]
            choosenColor = undoColor[len(undoX) - 1]
            unT = undoType[len(undoX) - 1]
            unOL = undoOldLabel[len(undoX) - 1]
            unNL = undoNewLabel[len(undoX) - 1]

            #Save veriables to redo
            redoX.append(unX)
            redoY.append(unY)

            if len(pix[unX, unY]) == 4:
                r, g, b, opa = pix[unX, unY]
            else:
                r, g, b = pix[unX, unY]

            redoColor.append((r, g, b))
            redoType.append(unT)
            redoOldLabel.append(unOL)
            redoNewLabel.append(unNL)

            #Paint images as a info according to undo veriables
            paintProcess(unX,unY)

            #Delete used undo veriables
            undoX = undoX[:-1]
            undoY = undoY[:-1]
            undoColor = undoColor[:-1]
            undoType = undoType[:-1]
            undoOldLabel = undoOldLabel[:-1]
            undoNewLabel = undoNewLabel[:-1]


        elif undoType[len(undoX) - 1] == 2: #undo typing for color brush

            start=undoNewLabel[len(undoX) - 1]
            while undoNewLabel[len(undoX) - 1] == start:#Try/go while label count change -> label count change after evety process
                print("undo", "type=", undoType[len(undoX) - 1], "x=", undoX[len(undoX) - 1], "y=", undoY[len(undoX) - 1],
                      " and color=", undoColor[len(undoX) - 1], "Old label value=", undoOldLabel[len(undoX) - 1], "and label value=", undoType[len(undoX) - 1])

                # take last process infos.
                unX = undoX[len(undoX) - 1]
                unY = undoY[len(undoX) - 1]
                choosenColor = undoColor[len(undoX) - 1]
                unT = undoType[len(undoX) - 1]
                unOL = undoOldLabel[len(undoX) - 1]
                unNL = undoNewLabel[len(undoX) - 1]

                # Save veriables to redo
                redoX.append(unX)
                redoY.append(unY)

                if len(pix[unX, unY]) == 4:
                    r, g, b, opa = pix[unX, unY]
                else:
                    r, g, b = pix[unX, unY]

                redoColor.append((r, g, b))
                redoType.append(unT)
                redoOldLabel.append(unOL)
                redoNewLabel.append(unNL)

                #Paint images as a info according to veriables
                pix[unX, unY] = choosenColor
                openedImage.putpixel((unX, unY), choosenColor)
                labelValue[unX][unY]=unOL

                # Delete used undo veriables
                undoX = undoX[:-1]
                undoY = undoY[:-1]
                undoColor = undoColor[:-1]
                undoType = undoType[:-1]
                undoOldLabel = undoOldLabel[:-1]
                undoNewLabel = undoNewLabel[:-1]
            #update image
            updateImg()

        choosenColor = backColor

def redo(): # reverse the undo
    global undoColor
    global undoX
    global undoY
    global redoColor
    global redoX
    global redoY
    global labelValue
    global openedImage
    global img
    global pix
    global choosenColor
    global undoType
    global undoOldLabel
    global redoType
    global redoOldLabel
    global undoNewLabel
    global redoNewLabel

    if len(redoX) > 0:
        if redoType[len(redoX) - 1] == 1:  # redo typing for fill color
            print("redo", "type=", redoType[len(redoX) - 1], "x=", redoX[len(redoX) - 1], "y=", redoY[len(redoX) - 1], " and color=", redoColor[len(redoX) - 1])

            reX=redoX[len(redoX) - 1]
            reY=redoY[len(redoX) - 1]
            choosenColor=redoColor[len(redoX) - 1]
            reT=redoType[len(redoX) - 1]
            reOL=redoOldLabel[len(redoX) - 1]
            reNL=redoNewLabel[len(redoX) - 1]

            if len(pix[reX, reY]) == 4:
                r, g, b, opa = pix[reX, reY]
            else:
                r, g, b = pix[reX, reY]

            undoX.append(reX)
            undoY.append(reY)
            undoColor.append((r, g, b))
            undoType.append(reT)
            undoOldLabel.append(reOL)
            undoNewLabel.append(reNL)

            paintProcess(reX, reY)

            redoX= redoX[:-1]
            redoY= redoY[:-1]
            redoColor= redoColor[:-1]
            redoType=redoType[:-1]
            redoNewLabel=redoNewLabel[:-1]
            redoOldLabel=redoOldLabel[:-1]

        elif redoType[len(redoX) - 1] == 2: # redo typing for color brush
            start = redoNewLabel[len(redoX) - 1]
            while redoNewLabel[len(redoX) - 1] == start:
                print("redo", "type=", redoType[len(redoX) - 1], "x=", redoX[len(redoX) - 1], "y=", redoY[len(redoX) - 1], " and color=", redoColor[len(redoX) - 1], "Old label value=", redoOldLabel[len(redoX) - 1], "and label value=", redoType[len(redoX) - 1])

                reX = redoX[len(redoX) - 1]
                reY = redoY[len(redoX) - 1]
                choosenColor = redoColor[len(redoX) - 1]
                reT = redoType[len(redoX) - 1]
                reOL = redoOldLabel[len(redoX) - 1]
                reNL = redoNewLabel[len(redoX) - 1]

                if len(pix[reX, reY]) == 4:
                    r, g, b, opa = pix[reX, reY]
                else:
                    r, g, b = pix[reX, reY]

                undoX.append(reX)
                undoY.append(reY)
                undoColor.append((r, g, b))
                undoType.append(reT)
                undoOldLabel.append(reOL)
                undoNewLabel.append(reNL)

                redoX = redoX[:-1]
                redoY = redoY[:-1]
                redoColor = redoColor[:-1]
                redoType = redoType[:-1]
                redoNewLabel = redoNewLabel[:-1]
                redoOldLabel = redoOldLabel[:-1]

                pix[reX, reY] = choosenColor
                openedImage.putpixel((reX, reY), choosenColor)
                labelValue[reX][reY] = reOL

            updateImg()

        choosenColor = backColor


def cleanThePicture():#Clean image and past
    #For clean picture go undo while past become empty then clean the past
    global undoColor
    global undoX
    global undoY
    global redoColor
    global redoX
    global redoY
    global undoOldLabel
    global undoType
    global redoOldLabel
    global redoType
    global operation
    global undoNewLabel
    global redoNewLabel
    for t in range(0, len(undoX)):
        undo()
    undoColor.clear()
    undoX.clear()
    undoY.clear()
    redoColor.clear()
    redoX.clear()
    redoY.clear()
    undoType.clear()
    undoOldLabel.clear()
    undoNewLabel.clear()
    redoNewLabel.clear()
    redoType.clear()
    redoOldLabel.clear()



def reset(): #Reset all the global veriables
    global choosenColor
    global backColor
    global img
    global openedImage
    global rowSize
    global columnSize
    global pix
    global labelValue
    global pix
    global undoColor
    global undoX
    global undoY
    global redoColor
    global redoX
    global redoY
    global brushSize
    global undoNewLabel
    global undoOldLabel
    global undoType
    global redoNewLabel
    global redoOldLabel
    global redoType
    global operation
    global colorR
    global colorB
    global colorG
    global labelCount
    global undoNewLabel
    global redoNewLabel
    undoNewLabel.clear()
    redoNewLabel.clear()
    labelCount = 2
    operation = (0, 0, 0)
    colorR = 0
    colorG = 0
    colorB = 0
    brushSize = 1
    choosenColor = (0, 0, 0)
    backColor = (0, 0, 0)
    openedImage = None
    rowSize = 0
    columnSize = 0
    pix = None
    labelValue = None
    undoColor.clear()
    undoX.clear()
    undoY.clear()
    undoType.clear()
    undoOldLabel.clear()
    undoNewLabel.clear()
    redoColor.clear()
    redoX.clear()
    redoY.clear()
    redoType.clear()
    redoOldLabel.clear()
    redoNewLabel.clear()
    img.config(image='')
    img.configure(image='')
    img.image=None
    img.update()
    selectedColor.configure(background='black')  # print kit bg
    selectedColor.update()
    refreshRGBScale() #Refresh gui rgb screen

def updateImg():#Add new image and update from window
    render = ImageTk.PhotoImage(openedImage)
    img.configure(image=render)
    img.image = render
    img.update()

def randomPaint():
    global labelCount
    global pix
    global rowSize
    global columnSize
    global pixelValue
    global labelValue
    global openedImage
    global choosenColor
    for t in range(0, labelCount+1):
        r = random.randint(0, 255) #return random integer between 0-255
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        global colorR
        global colorG
        global colorB
        colorR = r
        colorG = g
        colorB = b
        choosenColor = (r,g,b)
        refreshRGBScale()
        print(colorR, colorG, colorB)
        for j in range(1, columnSize - 1):
            for i in range(1, rowSize - 1):
                if (labelValue[i][j] == t) and (pixelValue[i][j] != 0):
                    #print("succes")
                    addPast(i, j, 1)  # Add process to past/history
                    paintProcess(i, j)
                    t += 1

    choosenColor = colorR, colorG, colorB
    colorX = '#%02x%02x%02x' % (r, g, b)  # RGB to full color hex/name
    selectedColor.configure(background=colorX)
    selectedColor.update()
    refreshRGBScale()
    updateImg()


#****************OPERATIONS***************
#Operate and route according to selection
def colorFillOn():
    global operation
    operation = (0, 0, 1)
    print(operation)
def colorPickerOn():
    global operation
    operation = (0, 1, 0)
    print(operation)
def colorBrushOn():
    global operation
    operation = (0, 1, 1)
    print(operation)

# ***************MENU********************

menu = Menu(window)#Simple file, edit and operation menu
window.config(menu = menu)

fileMenu = Menu(menu)
menu.add_cascade(label = "File", menu = fileMenu)
fileMenu.add_command(label ="Open", command = openFile, accelerator="Ctrl+O")
fileMenu.add_command(label ="Save", command = saveFile, accelerator="Ctrl+S")
fileMenu.add_separator()
fileMenu.add_command(label ="Exit", command = window.destroy, accelerator="Ctrl+Q")

editMenu = Menu(menu)
menu.add_cascade(label = "Edit", menu = editMenu)
editMenu.add_command(label ="Undo", command = undo, accelerator="Ctrl+Z")
editMenu.add_command(label ="Redo", command = redo, accelerator="Ctrl+Y")
editMenu.add_command(label ="Clean Picture", command = cleanThePicture)
editMenu.add_command(label ="Reset", command = reset)

operationMenu = Menu(menu)
menu.add_cascade(label = "Operation", menu = operationMenu)
operationMenu.add_command(label ="Color Fill", command = colorFillOn)
operationMenu.add_command(label ="Color Picker", command = colorPickerOn)
operationMenu.add_command(label ="Color Brush", command = colorBrushOn)
operationMenu.add_command(label ="Paint Random", command = randomPaint)

# ***************KIT********************

kit = Frame(window, bd = 5, relief = SUNKEN, bg='white')#Some usefull buttons for user. Bottom button set.

addImg = Button(kit, text = "Add Img", borderwidth=1, command = openFile) #Define and config basic button on kit
addImgImg = ImageTk.PhotoImage(file= ".\\buttons\\open_folder.png") #Read image for button
addImg.config(image=addImgImg) #Set button image
addImg.image = addImgImg #Set Button image
addImg.pack(side = LEFT, padx = 2, pady = 2) #Set and pack button from kit

tundo = Button(kit, text = "Undo", borderwidth=1, command = undo)
tundoImg = ImageTk.PhotoImage(file= ".\\buttons\\undo.png")
tundo.config(image=tundoImg)
tundo.image = tundoImg
tundo.pack(side = LEFT, padx = 2, pady = 2)

tredo = Button(kit, text = "Redo", borderwidth=1, command = redo)
tredoImg = ImageTk.PhotoImage(file= ".\\buttons\\redo.png")
tredo.config(image=tredoImg)
tredo.image = tredoImg
tredo.pack(side = LEFT, padx = 2, pady = 2)



def getColor():
    curColor = askcolor() #Default ask color gui
    print (curColor)
    #Full folor info to RBG with type of regex
    color = str(curColor)
    start = color.index("((")
    stop = color.index("),")
    color = color[(start):stop]
    color = color[2:len(color)]
    r, g, b = color.split(",")
    global colorR
    global colorG
    global colorB
    colorR=int(float(r))
    colorG=int(float(g))
    colorB=int(float(b))
    global choosenColor     #//((r,g,b),#fffffdf)
    print(colorR,colorG,colorB)
    choosenColor =colorR,colorG,colorB
    global backColor
    backColor = choosenColor
    print("choosenColor is :", choosenColor)
    selectedColor.configure(background=curColor[1])#print kit bg
    selectedColor.update()
    print(curColor[1])
    refreshRGBScale() #Refresh gui rgb screen

selColor = Button(kit, text='Select Color', borderwidth=1, command=getColor)
selColorImg = ImageTk.PhotoImage(file= ".\\buttons\\select_color.png")
selColor.config(image=selColorImg)
selColor.image = selColorImg
selColor.pack(side= LEFT, padx=2, pady=2)

colorPicker = Button(kit, text='Color Picker', borderwidth=1, command=colorPickerOn)
colorPickerImg = ImageTk.PhotoImage(file= ".\\buttons\\color_picker.png")
colorPicker.config(image=colorPickerImg)
colorPicker.image = colorPickerImg
colorPicker.pack(side= LEFT, padx=2, pady=2)

colorFill = Button(kit, text='Color Fill', borderwidth=1, command=colorFillOn)
colorFillImg = ImageTk.PhotoImage(file= ".\\buttons\\color_fill.png")
colorFill.config(image=colorFillImg)
colorFill.image = colorFillImg
colorFill.pack(side= LEFT, padx=2, pady=2)

colorBrush = Button(kit, text='Color Picker', borderwidth=1, command=colorBrushOn)
colorBrushImg = ImageTk.PhotoImage(file= ".\\buttons\\color_brush.png")
colorBrush.config(image=colorBrushImg)
colorBrush.image = colorBrushImg
colorBrush.pack(side= LEFT, padx=2, pady=2)

selectedColor = Label(kit, bd = 1, relief = SUNKEN)
selectedColor.configure(background='black')
selectedColor.pack(side= LEFT, padx=2, pady=2, ipady=7, ipadx=14)

kit.pack(side = TOP, fill = X) #Set and pack kit

#*****************COLOR TABLE*************************
#easy color choose for interface

colorTab = Label(window) #Define gui color table border/label
fpCT = open(file= ".\\buttons\\color_table.png", mode = "rb") #Color table image
openedColorTabImg = Image.open(fpCT)
colorTabRender = ImageTk.PhotoImage(openedColorTabImg)
colorTab.config(image=colorTabRender) #Put image to label
colorTab.image = colorTabRender
colorTab.place(x=0, y=50) #Set place of color tab on window
colorTabPix = openedColorTabImg.load()

def pickColorFromTable(event): #Color pick from table
    #Get cliecked pixels color and set choosenColor.
    global colorTabPix
    global choosenColor
    x=event.x
    y=event.y
    if len(colorTabPix[x,y]) == 4:
        r,g,b,opa=colorTabPix[x,y]
    else:
        r,g,b=colorTabPix[x,y]
    global colorR
    global colorG
    global colorB
    colorR = r
    colorG = g
    colorB = b
    global choosenColor
    print(colorR, colorG, colorB)
    choosenColor = colorR, colorG, colorB
    colorX = '#%02x%02x%02x' % (r,g,b) #RGB to full color hex/name
    selectedColor.configure(background=colorX)
    selectedColor.update()
    refreshRGBScale() #Refresh gui rgb screen

colorTab.bind("<Button-1>", pickColorFromTable)

#*****************RGB SCALE****************
def refreshRGBScale(): #Refresh gui rgb screen
    global colorB
    global colorG
    global colorR
    global rScale
    global gScale
    global bScale
    rScale.set(value=colorR)
    gScale.set(value=colorG)
    bScale.set(value=colorB)
    rScale.update()
    gScale.update()
    bScale.update()

def updateR(val): #Update R value -> RGB
    global colorB
    global colorG
    global colorR
    global choosenColor
    colorR=val
    r = int(colorR)
    g = int(colorG)
    b = int(colorB)

    choosenColor = r, g, b
    colorX = '#%02x%02x%02x' % (r, g, b)
    selectedColor.configure(background=colorX) #Set kit color visual
    selectedColor.update() #Update kit color

def updateG(val):
    global colorB
    global colorG
    global colorR
    global choosenColor
    colorG = val
    r = int(colorR)
    g = int(colorG)
    b = int(colorB)

    choosenColor = r, g, b
    colorX = '#%02x%02x%02x' % (r, g, b)
    selectedColor.configure(background=colorX)
    selectedColor.update()

def updateB(val):
    global colorB
    global colorG
    global colorR
    global choosenColor
    colorB = val
    r = int(colorR)
    g = int(colorG)
    b = int(colorB)

    choosenColor = r,g,b
    colorX = '#%02x%02x%02x' % (r,g,b)
    selectedColor.configure(background=colorX)
    selectedColor.update()

rgbScale = Frame(window, background='white', relief = SUNKEN) #Define fram for RGB scales
rScale = Scale(rgbScale, orient=HORIZONTAL, bg='red', length=150, sliderlength=10, from_=0, to=255, command=updateR) #R scale 0-255
rScale.pack()#Pack scale to frame

gScale = Scale(rgbScale, orient=HORIZONTAL, bg='green', length=150, sliderlength=10, from_=0, to=255, command=updateG)
gScale.pack()

bScale = Scale(rgbScale, orient=HORIZONTAL, bg='blue', length=150, sliderlength=10, from_=0, to=255, command=updateB)
bScale.pack()

rgbScale.place(x=0,y=310)#pack frame

# ***************CLICK********************
#Mouse left click process
def leftClickImg(event):
    global labelCount
    labelCount += 1
    global operation
    if operation == (0, 0, 1):
        global past
        global pixelValue
        print(event.x, event.y)
        if pixelValue[event.x][event.y] != 0:
            addPast(event.x, event.y, 1)#Add process to past/history
            paintProcess(event.x, event.y) #Call process
    elif operation == (0, 1, 0):
        if pixelValue[event.x][event.y] != 0:
            colorPicker(event.x, event.y)
    elif operation == (0, 1, 1):
        paintWithBrush(event)

def colorPicker(x,y):
    #Read color from image, Same method with color table.
    global choosenColor
    global pix
    if len(pix[x,y]) == 4:
        r,g,b,opa=pix[x,y]
    else:
        r,g,b=pix[x,y]
    global colorR
    global colorG
    global colorB
    colorR = r
    colorG = g
    colorB = b
    global choosenColor
    print(colorR, colorG, colorB)
    choosenColor = colorR, colorG, colorB
    colorName = '#%02x%02x%02x' % (r,g,b)
    selectedColor.configure(background=colorName)
    selectedColor.update()
    refreshRGBScale()


def paintProcess(x,y):
    #Paint all the label which is has same label value with clicked pixel except black labels.
    global choosenColor
    for j in range(1,columnSize - 1):
        for i in range(1, rowSize - 1):
            if (labelValue[i][j] == labelValue[x][y]) and (pixelValue[x][y] != 0):
                pix[i,j] = choosenColor
                openedImage.putpixel((i, j), choosenColor)
    updateImg()


img.bind("<Button-1>", leftClickImg)

def paintWithBrush(event):
    # Paint alabel with size of brush size
    if operation == (0, 1, 1):
        global pix
        global choosenColor
        global openedImage
        global labelValue
        global labelCount
        global pixelValue
        x=event.x
        y=event.y
        for i in range(0,brushSize):
            for j in range(0, brushSize):
                addPast((x + i), (y + j), 2)#Add to history process
                pix[(x + i), (y + j)] = choosenColor
                openedImage.putpixel(((x + i), (y + j)), choosenColor) #Set pixels color

                addPast((x - i), (y - j), 2)
                pix[(x - i), (y - j)] = choosenColor
                openedImage.putpixel(((x - i), (y - j)), choosenColor)

                addPast((x - i), (y + j), 2)
                pix[(x - i), (y + j)] = choosenColor
                openedImage.putpixel(((x - i), (y + j)), choosenColor)

                addPast((x + i), (y - j), 2)
                pix[(x + i), (y - j)] = choosenColor
                openedImage.putpixel(((x + i), (y - j)), choosenColor)

                if choosenColor == (0,0,0): #If color black set pixel and label valuse acording to basic black pixel values
                    labelValue[x + i][y + j] = 1
                    labelValue[x - i][y - j] = 1
                    labelValue[x - i][y + j] = 1
                    labelValue[x + i][y - j] = 1
                    pixelValue[x + i][y + j] = 0
                    pixelValue[x - i][y - j] = 0
                    pixelValue[x - i][y + j] = 0
                    pixelValue[x + i][y - j] = 0
                else: #Else set label value
                    labelValue[x + i][y + j] = labelCount
                    labelValue[x - i][y - j] = labelCount
                    labelValue[x - i][y + j] = labelCount
                    labelValue[x + i][y - j] = labelCount

        updateImg()


img.bind('<B1-Motion>', paintWithBrush)#while left click pressed

#*********************RESIZE****************************
#Mouse whell process
def mouseWhellOperation(event):
    if operation == (0, 0, 0):
        imgResize(event)
    if operation == (0, 1, 1):
        setBrushSize(event)

def setBrushSize(event):#Set brush size
    global brushSize
    if (event.num == 5 or event.delta == -120) and (brushSize > 1):#Mouse whell down move
        brushSize -= 1
    elif (event.num == 4 or event.delta == 120):#Mouse whell up move
        brushSize += 1
    else:
        print("do nothing")



def imgResize(event):#Set image size
    global openedImage
    global rowSize
    global columnSize

    cleanThePicture()

    if event.num == 5 or event.delta == -120:
        rowSize = int(rowSize / 1.5)
        columnSize = int(columnSize / 1.5)
    elif event.num == 4 or event.delta == 120:
        rowSize = int(rowSize * 1.5)
        columnSize = int(columnSize * 1.5)
    else:
        print("do nothing")

    openedImage = openedImage.resize((rowSize, columnSize), Image.ANTIALIAS)#Resize process for PIL.Image
    imageProcess()


img.bind("<MouseWheel>", mouseWhellOperation)
# ***************KEYBOARD SHORTCUT********************
#Keyboard short cut process

def ctrlz(self):
    print(self)
    undo()

window.bind("<Control-z>", ctrlz)#Keyboard Case Sensitive z-Z
window.bind("<Control-Z>", ctrlz)

def ctrls(self):
    print(self)
    saveFile()

window.bind("<Control-s>", ctrls)
window.bind("<Control-S>", ctrls)

def ctrlq(self):
    print(self)
    sys.exit()

window.bind("<Control-q>", ctrlq)
window.bind("<Control-Q>", ctrlq)

def ctrlo(self):
    print(self)
    openFile()

window.bind("<Control-o>", ctrlo)
window.bind("<Control-O>", ctrlo)

def ctrly(self):
    print(self)
    redo()

window.bind("<Control-y>", ctrly)
window.bind("<Control-Y>", ctrly)

# ***********************************

#End of window
window.mainloop()
