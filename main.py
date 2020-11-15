import requests
import time
from tkinter import *
from tkinter import ttk
from random import randint
from bs4 import BeautifulSoup
from PIL import ImageTk, Image
from screeninfo import get_monitors

# def get_max_page_num():
#    URL = f"https://xkcd.com/"
    # i = 2380
    # while True:
    #     i += 1
    #     response = requests.get(f"{URL}{i}")
    #     if response.status_code == 404:
    #         break
    #     print(i, response.status_code)
    # print(f"RESULT: {i}")


def get_eng_data():
    URL = f"https://xkcd.com/"
    i = randint(1, 100) #24 for scrollbar
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
resolution = str(get_monitors()[0]).split(',')
m_x, m_y = int(resolution[2].split('=')[1]), int(resolution[3].split('=')[1])





root = Tk()
root.iconphoto(False, ImageTk.PhotoImage(file='icon.png'))
root.geometry(f'+{m_x//3}+{m_y//5}')
root.title("XKCDViewer")

data = get_eng_data()

cur_num_label = Label(text=data['i'], font=('times', 20, 'bold'))
title_label = Label(text=data['title'], font=('times', 16, 'bold', 'underline'))


_img = Image.open("eng_version.jpg")
img = ImageTk.PhotoImage(_img)
h = _img.size[1] if _img.size[1] < 500 else 500


imgframe = LabelFrame()

imgcanvas = Canvas(imgframe, width=_img.size[0], height=h)

scrollbar = ttk.Scrollbar(imgframe, orient=VERTICAL, command=imgcanvas.yview)



win = imgcanvas.create_window((0, 0), window=imgframe, anchor=NW)
imagetag = imgcanvas.create_image((0, 0), anchor=NW, image=img)

imgcanvas.config(yscrollcommand=scrollbar.set, scrollregion=imgcanvas.bbox('all'))


mframe = LabelFrame(text="Randall Munroe's commentary")
comment_label = Message(mframe, text=data['comment'], font=('times', 12, 'italic'), justify=LEFT,
                        width=_img.size[0]-_img.size[0]/20)


def randomf():
    global title_label
    global imagetag
    global imgcanvas
    global comment_label
    global cur_num_label

    data = get_eng_data()
    _img = Image.open("eng_version.jpg")
    img = ImageTk.PhotoImage(_img)
    h = _img.size[1] if _img.size[1] < 500 else 500

    cur_num_label.config(text=data['i'])
    title_label.config(text=data['title'])

    imgcanvas.image = img
    imgcanvas.itemconfig(imagetag, image=img)
    imgcanvas.config(yscrollcommand=scrollbar.set, scrollregion=imgcanvas.bbox('all'), width=_img.size[0], height=h)


    comment_label = Message(mframe, text=data['comment'], width=_img.size[0] - _img.size[0] / 20)



buttonsframe = LabelFrame(text="Buttons")
button_rus = Button(buttonsframe, text="Rus")
button_eng = Button(buttonsframe, text="Random", command=randomf)
button_exp = Button(buttonsframe, text="Exp")

# imgframe.grid_propagate(False)

cur_num_label.grid(row=0, column=1)
title_label.grid(row=1, column=1)

imgframe.grid(row=2, column=0, columnspan=3)
imgcanvas.grid(row=2, column=0)
scrollbar.grid(row=2, column=3, sticky=NS)

mframe.grid(row=3, column=0, columnspan=3)
comment_label.grid(row=3, column=0, columnspan=3)
buttonsframe.grid(row=4, column=1)
button_rus.grid(row=4, column=0)
button_eng.grid(row=4, column=1)
button_exp.grid(row=4, column=2)


root.mainloop()
