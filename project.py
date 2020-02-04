""" The main project to run a slideshow. """
import sys
import os
import time
import tkinter as tk
from tkinter import messagebox
from matplotlib.colors import is_color_like
from PIL import ImageTk, Image
from screeninfo import get_monitors

# global variables
C = 'white'
D = '#EEF9F4'
W_MAX = get_monitors()[0].width
H_MAX = get_monitors()[0].height
BUTTON_WIDTH = 5
BUTTON_HEIGHT = 2
DELAY = 1000  # milliseconds


def curr_directory():
    """ Get the name of dir, from which I make a slideshow. """
    directory = ''
    if len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]):
            directory += sys.argv[1]
    else:
        directory += '.'
    return directory


def init_pictures(curr_dir, order_needed):
    """ Create a list of images paths, maybe it will be needed to read the order from a file. """
    image_files_in_curr_dir = []
    for name in os.listdir(curr_dir):
        if name.endswith(".png") or name.endswith(".jpg") \
                and name != 'start.jpg' and name != 'end.jpg':
            image_files_in_curr_dir.append(curr_dir + '\\' + name)  # lists of images in current dir
    if not order_needed:  # alphabetical order
        return image_files_in_curr_dir

    # read the file with the order, check if it is correct
    f_opened = open(curr_dir + '\\order.txt', "r")
    image_files_in_curr_dir_ordered = []
    for line in f_opened:
        image_files_in_curr_dir_ordered.append(curr_dir + '\\' + line.split('\n')[0])
    f_opened.close()
    # file with order was correct
    if set(image_files_in_curr_dir) == set(image_files_in_curr_dir_ordered):
        return image_files_in_curr_dir_ordered
    # it was wrong, we use default order
    return image_files_in_curr_dir


def mult(tuple_arg, multiplyer):
    """ Multiply each tuple component, round out to integer and return as list. """
    return [int(multiplyer * x) for x in tuple_arg]


def get_name(path):
    """ Get dir / file name only from the path. """
    splited = path.split('\\')
    return splited[len(splited) - 1]


def wanted_size(tuple_arg):
    """ Adjusting image size to the window. """
    width, height = tuple_arg
    scale = 0
    if width > W_MAX and height <= H_MAX:
        scale += W_MAX / width
    elif width <= W_MAX and height > H_MAX:
        scale += H_MAX / height
    elif width > W_MAX and height > H_MAX:
        scale += min(W_MAX / width, H_MAX / height)
    else:
        return tuple_arg
    return mult((width, height), scale)


def reformat_comment(comment):
    """ If a comment is long, I need to divide it into lines so as to make it
     visible in App's comment label. It can store 14 characters in one line. """
    if comment == '' or len(comment) <= 14:
        return comment
    splitted = comment.split()
    res = ''
    line = splitted[0]
    for i in range(1, len(splitted)):
        if len(line + ' ' + splitted[i]) > 14:
            res += line
            res += '\n'
            line = splitted[i]
            if i == len(splitted) - 1:
                res += line
        else:
            line += ' '
            line += splitted[i]
            if i == len(splitted) - 1:
                res += line
    return res


def load_comments(dir_from):
    """ The functions that searches current directory if it contains 'comments.txt'
    file. If yes, it makes a list o this comments and returns it, instead it returns
    list of empty strings. """
    res = []
    # I count how many images there is in the current directory
    num_of_images = 0
    comments_needed = False
    for name in os.listdir(dir_from):
        if name == 'comments.txt':
            comments_needed = True
        if name.endswith(".png") or name.endswith(".jpg") \
                and name != 'start.jpg' and name != 'end.jpg':
            num_of_images += 1
    if not comments_needed:  # we will display empty comments
        res = [''] * (num_of_images + 2)
        return res
    res.append('')  # for the starting picture
    f_opened = open(dir_from + '\\comments.txt', "r")
    for line in f_opened:
        res.append(reformat_comment(line.split('\n')[0]))
    res.append('')  # for the ending picture
    f_opened.close()
    return res


class App(tk.Tk):
    """ Main class for slideshow. """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, image_files, dir_from):
        tk.Tk.__init__(self)
        app_width = self.winfo_screenwidth()
        app_height = self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (app_width - 10, app_height))
        self.title("Python project, Dominika Kapanowska")
        self.configure(background=C)
        self.image_files = image_files
        self.pictures = []
        self.browse_files(self.image_files)
        self.comments = load_comments(dir_from)

        # buttons panel
        # pylint: disable=assignment-from-no-return
        self.buttons = tk.Label(self, height=40, width=15, background=C)
        self.buttons.pack(side='left', anchor='nw', padx=10, pady=10)
        self.b_prev = tk.Button(self.buttons, text='PREV', command=self.show_previous_image, bg=D,
                                height=BUTTON_HEIGHT, width=BUTTON_WIDTH).grid(row=0, column=0)
        self.b_next = tk.Button(self.buttons, text='NEXT', command=self.show_next_image, bg=D,
                                height=BUTTON_HEIGHT, width=BUTTON_WIDTH).grid(row=0, column=1)
        self.first_button = tk.Button(self.buttons, text='FIRST', command=self.show_first,
                                      bg=D, height=BUTTON_HEIGHT, width=BUTTON_WIDTH) \
            .grid(row=1, column=0)
        self.last_button = tk.Button(self.buttons, text='LAST', command=self.show_last,
                                     bg=D, height=BUTTON_HEIGHT, width=BUTTON_WIDTH) \
            .grid(row=1, column=1)
        self.quit_button = tk.Button(self.buttons, text='QUIT', command=self.destroy, bg=D,
                                     height=BUTTON_HEIGHT, width=BUTTON_WIDTH).grid(row=2, column=0)
        self.auto_button = tk.Button(self.buttons, text='AUTO', command=self.auto, bg=D,
                                     height=BUTTON_HEIGHT, width=BUTTON_WIDTH).grid(row=2, column=1)
        self.default_button = tk.Button(self.buttons, text='DFLT', command=self.default, bg=D,
                                        height=BUTTON_HEIGHT, width=BUTTON_WIDTH) \
            .grid(row=3, column=0)

        # manual color setting
        self.entered_color = tk.StringVar()
        self.text_box = tk.Entry(self.buttons, width=3 * BUTTON_WIDTH - 1,
                                 textvariable=self.entered_color)
        self.text_box.grid(row=4, columnspan=3)
        self.color_button = tk.Button(self.buttons, text='SET', command=self.set_color, bg=D,
                                      height=BUTTON_HEIGHT, width=BUTTON_WIDTH) \
            .grid(row=3, column=1)

        # place for comment
        self.comment_label = tk.Label(self.buttons, text='', height=15, width=12,
                                      anchor='nw', justify=tk.LEFT, background=C)
        self.comment_label.grid(row=7, columnspan=5)

        # place for an image
        self.picture_display = tk.Label(self, height=int(H_MAX * 0.85), width=int(W_MAX * 0.85),
                                        background=C)
        self.picture_display.pack(side='left', anchor='nw', pady=30)

        # other features
        self.idx = 0
        self.num_of_im = len(self.image_files)
        img_object = list(self.pictures[0])[0]  # title image
        self.picture_display.config(image=img_object)
        self.history = None

    def browse_files(self, images):
        """ Making image objects from paths. """
        images = ['.\\start.jpg', *images]  # title image
        images.append('.\\end.jpg')  # ending image
        for image in images:
            tmp = Image.open(image)
            wid, hgt = wanted_size(tmp.size)
            tmp = tmp.resize((wid, hgt), Image.ANTIALIAS)
            self.pictures.append((ImageTk.PhotoImage(tmp), image))

    def show_previous_image(self):
        """ Shows previous image. """
        if self.idx <= 0:  # we are at the beggining
            self.idx = 0
            messagebox.showinfo('Info', "That is the beginning!\nPlease press"
                                        " the NEXT button!")
            return
        self.idx -= 1
        # display a comment to this picture
        self.comment_label.config(text=self.comments[self.idx])
        img_object, img_name = self.pictures[self.idx]
        self.picture_display.config(image=img_object)
        # I do not write to the history neither title nor ending image name
        if get_name(img_name) != 'start.jpg':
            self.history.write(get_name(img_name) + '\n')
        return

    def show_next_image(self):
        """ Shows next image, when it does not exist, quit the slideshow. """
        if self.idx < 0:
            self.idx = 0
        if self.idx == self.num_of_im + 1:
            messagebox.showinfo('Info', 'That is the end! We quit the presentation.')
            self.destroy()
            return
        self.idx += 1
        # display a comment to this picture
        self.comment_label.config(text=self.comments[self.idx])
        img_object, img_name = self.pictures[self.idx]
        self.picture_display.config(image=img_object)
        # I do not write to the history neither title nor ending image name
        if get_name(img_name) != 'end.jpg':
            self.history.write(get_name(img_name) + '\n')
        return

    def show_first(self):
        """ Shows the first image after the title one. """
        self.idx = 1
        # display a comment to this picture
        self.comment_label.config(text=self.comments[self.idx])
        img_object, img_name = self.pictures[self.idx]
        self.picture_display.config(image=img_object)
        self.history.write(get_name(img_name) + '\n')

    def show_last(self):
        """ Show the last image before the ending one. """
        self.idx = len(self.pictures) - 2
        # display a comment to this picture
        self.comment_label.config(text=self.comments[self.idx])
        img_object, img_name = self.pictures[self.idx]
        self.picture_display.config(image=img_object)
        self.history.write(get_name(img_name) + '\n')

    def auto(self):
        """ Automatic slideshow, delay equal to 1 second. """
        if self.idx < 0:
            self.idx = 0
        if self.idx == self.num_of_im + 1:
            return
        self.idx += 1
        # display a comment to this picture
        self.comment_label.config(text=self.comments[self.idx])
        img_object, img_name = self.pictures[self.idx]
        self.picture_display.config(image=img_object)
        if get_name(img_name) != 'end.jpg':
            self.history.write(get_name(img_name) + '\n')
        self.after(DELAY, self.auto)
        return

    def default(self):
        """ Set the white (default) color scheme. """
        self.config(bg=C)
        self.picture_display.config(background=C)

    def set_color(self):
        """ Checks is string from text_box is a color,
        if yes, it sets this color on the background. """
        color = self.entered_color.get()
        if is_color_like(color):
            self.config(bg=color)
            self.picture_display.config(bg=color)
            self.text_box.delete(0, 'end')
        else:
            messagebox.showinfo('Info', '\"' + color + '\"' + ' is not a color!')
            self.text_box.delete(0, 'end')
            return

    def run(self):
        """ Runs the tkinter class. """
        self.mainloop()


def run_project(curr_dir):
    """ Main function to run this project. """
    if curr_dir == '' or not os.path.exists(curr_dir):
        return "Wrong name of a directory! / There is nothing to show!"
    # check if there is a file with order in the curr_dir
    order_needed = bool(os.path.isfile(curr_dir + '\\order.txt'))
    image_files = init_pictures(curr_dir, order_needed)
    num_of_im = len(image_files)
    if num_of_im == 0:
        return "Wrong name of a directory! / There is nothing to show!"
    app = App(image_files, curr_dir)
    # for each running creates the history file
    history_name = 'history' + str(int(time.time())) + '.txt'
    history = open('.\\History\\' + history_name, 'a')
    history.write('Directory: ' + curr_dir + ', ' + str(len(image_files)) + ' images\n')
    app.history = history
    app.run()
    history.close()
    return "Project run successfully, check the " + history_name + " file."

# how to run project:
# print(run_project(".//Ordered_default"))
# print(run_project(curr_directory()))
