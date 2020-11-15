from tkinter import *
import requests
from random import randint
from bs4 import BeautifulSoup
from PIL import ImageTk
import time

def get_max_page_num():
    pass
    # URL = f"https://xkcd.com/"
    # i = 2000
    # responce = 0
    # while responce != 200:
    #     i += 1
    #     response = requests.get(f"{URL}{i}")
    #     print(i, response.status_code)
    #
    # print(i)


def get_eng_data():
    URL = f"https://xkcd.com/"
    i = randint(1, 100)
    content = requests.get(f"{URL}{i}").content
    soup = BeautifulSoup(content, 'lxml')
    title = soup.find('div', {'id': 'ctitle'}).text
    Img = soup.find('div', {'id': 'comic'}).find_next()
    response = requests.get(f"http:{Img['src']}")
    with open('eng_version.jpg', 'wb') as f:
        f.write(response.content)
    data = {'title': title,
            'comment': f"({Img['title']})",
            'i': i}
    return data


# if __name__ == '__main__':
# get_max_page_num()

root = Tk()
root.iconphoto(False, ImageTk.PhotoImage(file='icon.png'))
# root.geometry("500x500+100+100")
# root.maxsize(800, 500)
# root.resizable(0, 0)
root.title("XKCDViewer")

data = get_eng_data()

cur_num_label = Label(text=data['i'], font=('times', 20, 'bold'))
title_label = Label(text=data['title'], font=('times', 15, 'bold', 'underline'))
img = ImageTk.PhotoImage(file="eng_version.jpg")
imglabel =Label(image=img)
comment_label = Message(text=data['comment'], font=('times', 12, 'italic'), justify=LEFT, bd=3)


def randomf():
    global title_label
    global imglabel
    global comment_label
    global cur_num_label

    data = get_eng_data()

    cur_num_label.config(text=data['i'])
    title_label.config(text=data['title'])
    img = ImageTk.PhotoImage(file="eng_version.jpg")
    imglabel.image = img
    imglabel.config(image=img)
    comment_label.config(text=data['comment'])




button_rus = Button(root, text='Random1')
button_eng = Button(root, text='Random', command=lambda: randomf())
button_exp = Button(root, text='Random3')

cur_num_label.grid(row=0, column=1)
title_label.grid(row=1, column=1)
imglabel.grid(row=2, column=0, columnspan=3)
comment_label.grid(row=3, column=0, columnspan=3)
button_rus.grid(row=4, column=0)
button_eng.grid(row=4, column=1)
button_exp.grid(row=4, column=2)

root.mainloop()
