import random
import string
from tkinter.messagebox import showinfo

from PIL import Image
from customtkinter import *

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title('Impiccato')
        self.geometry('840x480')
        set_appearance_mode('dark')
        set_default_color_theme('blue')
        self.iconbitmap('assets/hangman.ico')

        self.alphabet = list(string.ascii_lowercase)
        self.vowels = list('aeiou')
        self.consonants = sorted(list(set(self.alphabet) - set(self.vowels)))

        self.label_font = CTkFont(family='Segoe UI', size=22, weight='bold')
        self.font_os = CTkFont('Segoe UI', 22, 'normal', overstrike=True)

        self.letters_guessed = []

        self.tries = StringVar(self, '7')

        self.plus = CTkImage(Image.open('assets/plus.png'), Image.open('assets/plus_white.png'), size=(20, 20))
        self.dash = CTkImage(Image.open('assets/dash.png'), Image.open('assets/dash_white.png'), size=(20, 20))

        self.word_frame = CTkFrame(self, width=680, height=20)
        self.word_frame.grid(row=0, column=0, padx=20, pady=40, sticky='new')

        self.prove = CTkLabel(self, font=self.label_font, textvariable=self.tries, text_color='#caf0f8')
        self.prove.grid(row=0, column=1, padx=5, pady=40, sticky='new')

        self.letters_frame = CTkFrame(self, width=680, height=150)
        self.letters_frame.grid(row=1, column=0, padx=20, pady=40, sticky='new')
        self.try_word_entry = CTkEntry(self, width=680, height=40, font=self.label_font,
                                       text_color='#caf0f8', placeholder_text='Indovina la parola (vinci o perdi)')
        self.try_word_entry.grid(row=2, column=0, padx=20, pady=40, sticky='new')
        self.try_word_btn = CTkButton(self, text='Prova', fg_color='#023e8a', text_color='#caf0f8',
                                      command=self.try_word, font=self.label_font, width=60, height=35)
        self.try_word_btn.grid(row=2, column=1, padx=5, pady=40, sticky='new')
        self.bind('<Return>', self.try_word)
        with open('wordlists.txt') as f:
            self.words = f.readlines()
        self.regenerate_word()
        self.alphabet_btns = []
        row = 1
        col = 0
        for letter in sorted(list(self.alphabet)):
            if col == 11:
                col = 0
                row += 1

            l = CTkButton(self.letters_frame, width=30, height=30, text=letter, font=self.label_font,
                          command=lambda l=letter: self.try_letter(l), fg_color='transparent', text_color='#caf0f8')
            self.alphabet_btns.append(l)
            l.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
            self.bind(l, lambda l: self.try_letter(l))
            col += 1

    def try_letter(self, letter):
        if letter in self.word:
            indexes = [i for i, x in enumerate(self.word) if x == letter]
            for i in indexes:
                self.alphabet_btns[self.alphabet.index(letter)].configure(state='disabled',
                                                                          font=self.font_os, text_color='#969798')
                self.letters[i].configure(text=letter, image='')
                self.letters_guessed.append(letter)
                self.update()
            if sorted(list(set(self.letters_guessed))) == sorted(list(set(self.word))):
                showinfo('Parola indovinata!', f'Hai indovinato tutte le lettere!')
                self.regenerate_word()
                self.tries.set('7')
        else:
            self.alphabet_btns[self.alphabet.index(letter)].configure(state='disabled',
                                                                      font=self.font_os, text_color='#969798')
            self.tries.set(value=str(int(self.tries.get()) - 1))
            if self.tries.get() == '0':
                showinfo('Tentativi finiti!', f'Non hai indovinato entro i limiti!\nHai perso!')
                self.regenerate_word()
                self.tries.set('7')

    def try_word(self, event=None):
        word = self.try_word_entry.get()
        if self.word == word:
            showinfo('Parola indovinata!', f'Hai indovinato la parola {self.word} correttamente!')
            self.regenerate_word()
            self.tries.set('7')
        else:
            showinfo('Parola sbagliata!', f'Hai sbagliato la parola!\nHai perso!')
            self.regenerate_word()
            self.tries.set('7')

    def regenerate_word(self):
        self.word = random.choice(self.words)
        self.word = self.word.replace(self.word[-1], '')
        self.letters = []
        for i, l in enumerate(self.word):
            letter = CTkLabel(self.word_frame, width=40, height=40, text='',
                              image=self.plus if l in self.vowels else self.dash,
                              font=self.label_font, text_color='#caf0f8')
            self.letters.append(letter)
            letter.grid(row=0, column=i, sticky='nwe', padx=5, pady=5)

if __name__ == '__main__':
    app = App()
    app.mainloop()
