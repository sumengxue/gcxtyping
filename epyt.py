import os
import re
from tkinter import *
from pdb import *

#### Article preparaion
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

#### Window Init
window = Tk()
text = Text(window, wrap=WORD, font=fontName+' '+fontSize)
text.insert(INSERT, article[0])
text.pack()

####

#### Tag Init
def TagInit():
    text.tag_add('left', '1.0', '1.0')
    text.tag_add('middle', '1.0', '1.1')
    text.tag_config('middle', foreground=middleFore,
                    background=middleBack)
    text.tag_add('right', '1.2', END)
    text.tag_config('right', foreground=rightFore,
                    background=rightBack)
    text.config(state=DISABLED)
TagInit()
####

#### Key listen
def Keylistener(event):
    global x_pointer
    global paragraph_pointer
    global x_length
    if(event.char != article[paragraph_pointer][x_pointer]):
        return
    text.config(state=NORMAL)
    text.tag_delete('left')
    text.tag_delete('middle')
    text.tag_delete('right')
    x_pointer += 1
    if x_pointer == x_length:
        text.delete('1.0',END)
        paragraph_pointer += 1
        if(paragraph_pointer == paragraph_limit - 1):
            exit(0)
        text.insert(INSERT, article[paragraph_pointer])
        x_length = len(article[paragraph_pointer])
        x_pointer = 0
        TagInit()
        return
    text.tag_add('left', '1.0','1.{}'.format(x_pointer))
    text.tag_config('left', foreground=leftFore, background=leftBack)
    text.tag_add('middle', '1.{}'.format(x_pointer), '1.{}'.format(x_pointer+1))
    text.tag_config('middle', foreground=middleFore, background=middleBack)
    text.tag_add('right', '1.{}'.format(x_pointer+1), END)
    text.tag_config('right', foreground=rightFore, background=rightBack)
    text.config(state=DISABLED)
window.bind('<Key>', Keylistener)

def nullfunc(event):
    pass
window.bind('<Shift_L>', nullfunc)
mainloop()
