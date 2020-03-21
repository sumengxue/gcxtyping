from tkinter import *
import tkinter.ttk as ttk 
import tkinter.font as tkFont
import pdb
import os
import re
from io import StringIO

from config import *

selectWindow = Tk()

normalFont = tkFont.Font(family=fontName,
                         size=fontSize)
charWidth = int(normalFont.measure('a')*1.25)
realFontSize = fontSize * 2
x_inputPointer = 0
y_inputPointer = 0

def entry(arg):
    global normalFont
    fileName = arg + '.txt'

    article = open(fileName, 'r').read()
    articlePointer = 0
    selectWindow.destroy()
    typeWindow = Tk()
    windowWidth = 2*margin + x_size*charWidth
    windowHeight = 2*margin + y_size*(2*realFontSize) + (y_size-1)*padding
    typeWindow.geometry("{}x{}".format(windowWidth, windowHeight))

    referenceArray = []
    y_pointer = 0

    for i in range(y_size):
        x_pointer = 0
        lineBuffer = []
        finish = False
        while True:
            character = article[articlePointer]
            articlePointer += 1
            if character == ' ':
                spacePosition = x_pointer
            x_pointer += 1
            if character == '\n':
                break
            if character == '':
                finish = True
            lineBuffer.append(character)
            if x_pointer == x_size:
                if article[articlePointer] != ' ':
                    for i in range(x_pointer-spacePosition):
                        lineBuffer.pop()
                    articlePointer -= (x_pointer-spacePosition-1)
                    break
                break
        referenceArray.append(''.join(lineBuffer).strip()+' ')
        if(finish):
            break

    referenceWidgetArray = []
    x_position = margin
    y_position = margin
    for i in range(min(y_size, len(referenceArray))):
        textWidget = Text(typeWindow, font="Consolas",
                          height=realFontSize,padx=4,pady=0)
        textWidget.insert(INSERT, referenceArray[i])
        textWidget.config(state=DISABLED)
        textWidget.place(relx=x_position/windowWidth,
                         rely=y_position/windowHeight,
                         relwidth=charWidth*x_size/windowWidth,
                         relheight=realFontSize/windowHeight)
        y_position += realFontSize * 2 + padding
        referenceWidgetArray.append(textWidget)

    inputArray = [StringVar() for i in range(min(y_size, len(referenceArray)))]
    inputWidgetArray = []
    x_position = margin
    y_position = margin + realFontSize
    for i in range(min(y_size, len(referenceArray))):
        inputWidget = Label(typeWindow, font="Consolas",
                            textvariable=inputArray[i],
                            anchor='w', justify='left')
        inputWidget.place(relx=x_position/windowWidth,
                          rely=y_position/windowHeight,
                          relwidth=charWidth*x_size/windowWidth,
                          relheight=realFontSize/windowHeight)
        y_position += realFontSize *2 + padding
        inputWidgetArray.append(inputWidget)

    def keyListener(event):
        global x_inputPointer
        global y_inputPointer
        tempString = inputArray[y_inputPointer].get()
        inputArray[y_inputPointer].set(tempString+event.char)
        referenceWidget = referenceWidgetArray[y_inputPointer]
        if re.match('[0-9a-zA-Z]', event.char) != None and event.char != referenceArray[y_inputPointer][x_inputPointer]:
            referenceWidget.tag_add('ERR', '{}.{}'.format(1, x_inputPointer))
            referenceWidget.tag_config('ERR', foreground='White', background="Black")
        x_inputPointer += 1
        if x_inputPointer == len(referenceArray[y_inputPointer]):
            x_inputPointer = 0
            y_inputPointer += 1

    typeWindow.bind("<Key>", keyListener)

    def BackSpaceListener(event):
        global x_inputPointer
        global y_inputPointer
        referenceWidget = referenceWidgetArray[y_inputPointer]
        referenceWidget.tag_add('NOR', '{}.{}'.format(1, x_inputPointer-1))
        referenceWidget.tag_config('NOR', foreground='Black', background='White')
        if x_inputPointer != 0:
            tempString = inputArray[y_inputPointer].get()[0:-1]
            inputArray[y_inputPointer].set(tempString)
            x_inputPointer -= 1
        else:
            inputArray[y_inputPointer].set('')
            y_inputPointer -= 1
            x_inputPointer = len(referenceArray[y_inputPointer])
    typeWindow.bind("<BackSpace>", BackSpaceListener)
    def nullfunc(event):
        pass
    typeWindow.bind("<Shift_L>", nullfunc)
        

for fileName in os.listdir():
    if fileName.find('.') != -1 and fileName.split('.')[1] == 'txt':
        articleName = fileName.split('.')[0]
        selectButton = ttk.Button(selectWindow,text=articleName,
                              command=lambda arg=articleName:entry(arg))
        selectButton.pack(fill=X)

mainloop()
