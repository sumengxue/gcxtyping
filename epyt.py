from tkinter import *

#### Article preparaion
import os
articleName = None
for fileName in os.listdir():
    if fileName.find('.') != -1 and fileName.split('.')[1] == 'txt':
        articleName = fileName
if articleName == None:
    print("Can't find article file.")
    exit(0)
article = open(articleName, 'r').read().split('\n')
x_pointer = 0
paragraph_pointer = 0
paragraph_limit = len(article)
x_length = len(article[paragraph_pointer])
####

#### Theme setting
from theme import *
leftFore = select_theme['leftFore']
leftBack = select_theme['leftBack']
middleFore = select_theme['middleFore']
middleBack = select_theme['middleBack']
rightFore = select_theme['rightFore']
rightBack = select_theme['rightBack']
####


### TagControl
def TagControl(position):
    global text
    text.tag_add('left', '1.0','1.{}'.format(position))
    text.tag_config('left', foreground=leftFore, background=leftBack)
    text.tag_add('middle', '1.{}'.format(position), '1.{}'.format(position+1))
    text.tag_config('middle', foreground=middleFore, background=middleBack, underline=True)
    text.tag_add('right', '1.{}'.format(position+1), END)
    text.tag_config('right', foreground=rightFore, background=rightBack)
####

#### Window Init
window = Tk()
text = Text(window, wrap=WORD, font=fontName+' '+fontSize,
            spacing2=int(fontSize), width=50)
text.insert(INSERT, article[0])
text.pack()
TagControl(0)
####


#### Counter Init
import time
timestampA = time.time()
####

#### Key listen
def Keylistener(event):
    global x_pointer
    global paragraph_pointer
    global x_length
    global counter_limit
    global counter_pointer
    global timestampA
    if(event.char != article[paragraph_pointer][x_pointer]):
        return
    window.title(str(int(x_pointer/(time.time() - timestampA)*60)))
    text.config(state=NORMAL)
    text.tag_delete('left')
    text.tag_delete('middle')
    text.tag_delete('right')
    x_pointer += 1
    if x_pointer == x_length:
        text.delete('1.0',END)
        paragraph_pointer += 1
        if(paragraph_pointer >= paragraph_limit):
            exit(0)
        text.insert(INSERT, article[paragraph_pointer])
        x_length = len(article[paragraph_pointer])
        x_pointer = 0
        TagControl(0)
        return
    TagControl(x_pointer)
    text.config(state=DISABLED)

def nullfunc(event):
    pass
####

#### Bind
window.bind('<Key>', Keylistener)
window.bind('<Shift_L>', nullfunc)
####

mainloop()
