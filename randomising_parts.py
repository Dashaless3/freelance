# -*- coding: utf-8 -*-
"""
put into the input box more than 3 words
"""
script_name='randomising_halves.py'

#%% add modules

import sys
import tkinter
import re
import codecs
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.messagebox import *
import fileinput
import random 
import string

import numpy as np

TOKEN = '_ '
EOL = "++++."
COLUMNS_NEEDED = 6
DEFAULT_DELIM = "%%%%%%%%."

#%%
class Randomising_halves:

    def __init__(self):
        main_menu = Menu(root)
        root.config(menu=main_menu)
        first_menu = Menu(main_menu)
        
## somehow it works without self
        self.insert_text = Text(root, width=20, height=20, wrap=WORD)
        self.insert_text.grid(row=1, column=0, rowspan=6, sticky=N+S+E+W)
        self.label=Label(root, text="Insert text")
        self.label.grid(row=0, column=0)

        self.result_text = Text(root, width=35, height=20, wrap=WORD)
        self.result_text.grid(row=1, column=3, rowspan=6, sticky=N+S+E+W)
        self.label=Label(root, text="Result text")
        self.label.grid(row=0, column=3)

        self.ins_text_sentences=Button(root, text = "Randomise halves", command=self.process)
        self.ins_text_sentences.grid(row=8, column = 0)
        
        self.label=Label(root, text="Number of sentences")
        self.label.grid(row=0, column=4)
        self.num_sent = Text(root, width=10, height=1, wrap=WORD)
        self.num_sent.grid(row=1, column=4, sticky=N)

        self.label=Label(root, text="Number of columns")
        self.label.grid(row=1, column=4, sticky=S)
        self.num_col = Text(root, width=10, height=1, wrap=WORD)
        self.num_col.grid(row=2, column=4, sticky=N)

        self.var=0
        self.delimtr_on = Button(root, text="Indexing OFF", command = self.toggle)
        self.delimtr_on.grid(row=4, column=4, sticky=N)

        self.label=Label(root, text="Delimeter type")
        self.label.grid(row=2, column=4, sticky=S)
        self.delimtr = Text(root, width=10, height=1, wrap=WORD)
        self.delimtr.grid(row=3, column=4, sticky=N)
        self.delimtr.insert(END, DEFAULT_DELIM)

############################################################################################

    def toggle(self):
        self.var = 1 - self.var
        if self.var:
            self.delimtr_on.configure(text="Indexing ON")
        else:
            self.delimtr_on.configure(text="Indexing OFF")
    
    def getData(self):
        data = self.insert_text.get("1.0",END)
        delim = self.delimtr.get("1.0", END)
        all_texts = re.split(delim, data)
        for i in range(len(all_texts)):
            text = all_texts[i]
            all_sentences = re.split("[.!?]+[\’]?[\s\n]+", text)
            text_copy = text
            for j in range (len(all_sentences)):
                entry = all_sentences[j].strip(' \n')
                text_copy = text_copy.replace(entry, '')
                try:
                    ending = text_copy.split()[0]
                except IndexError:
                    ending = ''
                entry += ending
                text_copy = text_copy.replace(ending, '', 1).strip(' \n')
                all_sentences[j] = entry
            while '\n' in all_sentences:
                all_sentences.remove('\n')
            for j in range (len(all_sentences)):
                all_sentences[j] = all_sentences[j].strip()
                while all_sentences[j].find('\n') != -1:
                    ind = all_sentences[j].find('\n')
                    all_sentences[j] = all_sentences[j][:ind] + ' ' + all_sentences[j][ind+1:]
            while '' in all_sentences:
                all_sentences.remove('')
            while '.' in all_sentences:
                all_sentences.remove('.')
            all_texts[i] = all_sentences
        while [] in all_texts:
            all_texts.remove([])
        return all_texts

    def getText(self, data):
        numsent = self.num_sent.get("1.0",END)
        if numsent.isspace() or not numsent:
            numsent = str(len(data))
        numsent = int(numsent.strip())
        blocks = []
        s = len(data)
        while s - numsent > 0:
            blocks.append(data[:numsent])
            data = data[numsent:]
            s -= numsent
        blocks.append(data[:numsent])
        return blocks

    def print_no_indexing(self, data, columns, halves):
        for sentence in range(len(data)):
            line = ''
            for j in range(columns-1):
                line += halves[sentence][j] + '\t'
            line += halves[sentence][-1] + '\n'
            self.result_text.insert(END, line)
        EOF = (EOL+'\t')*columns
        self.result_text.insert(END, EOF[:-1] + '\n')

    def print_with_indexing(self, data, columns, halves, sentences_printed):
        for sentence in range(len(data)):
            line = str(sentences_printed+sentence+1) + ')' + '\t' + halves[sentence][0] + '\t'
            for j in range(1, columns-1):
                line += chr(65+sentence)*j + ')' + '\t' + halves[sentence][j] + '\t'
            line += chr(65+sentence)*(columns-1) + ')' + '\t' + halves[sentence][-1] + '\n'
            self.result_text.insert(END, line)
        EOF = (' ' + '\t' + EOL+'\t')*columns
        self.result_text.insert(END, EOF[:-1] + '\n')

    def randomise_1_text(self, data):
        if data == []:
            pass
        else:
            blocks = self.getText(data) # array of lists of sentences - blocks
            columns = self.num_col.get("1.0",END)
            if columns.isspace() or not columns:
                columns = 2
            columns = int(columns)            
            sentences_printed = 0
            for i in range(len(blocks)): # data = block
                data = blocks[i] # list of sentences in one block
                halves = [] # list of parts of sentences
                for sentence in range(len(data)):
                    halves.append([])
                    cur = data[sentence].split()
                    const = len(cur)
                    if const//columns == 0:
                        halves[sentence].append(' '.join(cur))
                        last_sym = re.split("[.!?]+", cur[-1])[-2]
                        if last_sym == '':
                            ending = cur[0]
                        else:
                            ending = cur[-1].split(last_sym)[-1]
                        for j in range (columns-1):
                            halves[sentence].append('_' + ending)
                    else:
                        for j in range (columns-1):
                            halves[sentence].append(' '.join(cur[:const//columns]))
                            cur = cur[const//columns:]
                        halves[sentence].append(' '.join(cur))
                halves = np.array(halves)
                for j in range(1, columns):
                    indexes = list(range(0, len(data)))
                    random.shuffle(indexes)
                    halves[:, j] = halves[indexes, j]
                if self.var:
                    self.print_with_indexing(data, columns, halves, sentences_printed)
                    sentences_printed += len(data)
                else:
                    self.print_no_indexing(data, columns, halves)

    def process(self):
        data = self.getData()
        columns = self.num_col.get("1.0",END)
        if columns.isspace() or not columns:
            columns = 2
        columns = int(columns)
        delim = self.delimtr.get("1.0", END).strip(' \n')
        if delim.isspace() or not delim:
            delim = DEFAULT_DELIM
        self.result_text.delete("1.0",END)
        for text in data:
            self.randomise_1_text(text)
            if self.var:
                EOF = (' ' + '\t' + delim + '\t')*columns
                self.result_text.insert(END, EOF[:-1] + '\n')
            else:
                EOF = (delim + '\t')*columns
                self.result_text.insert(END, EOF[:-1] + '\n')

root = Tk()
root.title("Half sentence randomizer")
r=Randomising_halves()
root.mainloop()
