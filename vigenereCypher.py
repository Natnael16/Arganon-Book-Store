import random
import string
from tkinter import *
from turtle import back


class Vigenere:
    def __init__(self) -> None:
        letters = string.ascii_letters + string.digits + string.punctuation + " "
        # letters = "qwertyuiopasdfghjklzxcvbnmABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890-=[]\;',./~!@#$%^&*()_+{}|:<>? "
        size = len(letters)
        self.row_dict = {letter: index for index, letter in enumerate(
            random.sample(letters, size))}
        col = random.sample(letters, size)
        self.col_dict = {index: letter for index, letter in enumerate(col)}
        self.col_by_letter = {letter: index for index, letter in enumerate( col)}

        self.matrix = [random.sample(letters, size)
                       for counter in range(size)]

    def encrypt(self, key, plain):
        encrypted = ""
        for index, letter in enumerate(plain):
            colmn = self.col_by_letter[letter]
            row = self.row_dict[key[index % len(key)]]
            encrypted += self.matrix[row][colmn]

        return encrypted

    def decrypt(self, key, encrypted):
        decrypted = ""

        for index, letter in enumerate(encrypted):
            row_letter = index % len(key)
            row = self.row_dict[key[row_letter]]

            for idx, element in enumerate(self.matrix[row]):
                if element == letter:
                    decrypted += self.col_dict[idx]
                    break
        return decrypted


vigenere = Vigenere()

def encryptor():
    key = keyInput.get("1.0", "end-1c")
    message = textInput.get("1.0", "end-1c")
    ans = vigenere.encrypt(key, message)
    outPut.delete("1.0", "end")
    outPut.insert(END, "This is the encrypted message: "+ans)


def decryptor():
    key = keyInput.get("1.0", "end-1c")
    enc = textInput.get("1.0", "end-1c")
    ans = vigenere.decrypt(key, enc)
    outPut.delete("1.0", "end")
    outPut.insert(END, "This is the decrypted message: "+ans)


root = Tk()
root.geometry("1000x1000")
inputFrame = Frame(root).grid(row=0)
textFrame = Frame(inputFrame, background="blue").grid(column=0, row=0)
keyFrame = Frame(inputFrame, background="cyan").grid(column=1, row=0)
textLabel = Label(textFrame, text="Enter text here").grid(column=0, row=0)
keyLabel = Label(keyFrame, text="Enter key here").grid(column=1, row=0)
textInput = Text(textFrame, background="lightgray", width=60, height=7)
textInput.grid(column=0, row=1)
keyInput = Text(keyFrame, background="lightgray", width=35, height=7)
keyInput.grid(column=1, row=1)
gap1 = Frame(root, height=50).grid(row=2)
buttonsFrame = Frame(root).grid(column=0, row=3)
enryptButton = Button(buttonsFrame, text="Encrypt",
                      command=encryptor).grid(column=0, row=3)
decryptButton = Button(buttonsFrame, text="Decrypt",
                       command=decryptor).grid(column=1, row=3)
gap2 = Frame(root, height=50).grid(column=0, row=4)
outPut = Text(root, width=120, height=10, background="lightgray")
outPut.grid(row=5, column=0, columnspan=2)


root.mainloop()