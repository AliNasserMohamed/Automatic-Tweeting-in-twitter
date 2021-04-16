import tkinter as tk
from tkinter import *
from selenium import webdriver
import time
import threading
import sys, os
import pickle

import pandas as pd

try:
    f = open("last_session.txt", "r")
    i = int(f.readline())
    f.close()
except:
    i = -1


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()

        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#C4C4C4", padx=40, pady=10, width=880, height=500)
        master.geometry("660x400")
        # master.iconbitmap("favicon.ico")
        master.title("Automatic tweeting")
        master.resizable(False, False)

        start_header = Label(self, text="Please fill in all fields as required ", bg="#C5C3C3")
        start_header.grid(padx=5, pady=(0, 10), sticky=W, row=0)
        global label1
        frame1 = LabelFrame(self, padx=10, pady=20, bg="#ffffff", borderwidth=0, highlightthickness=0, relief='ridge')
        frame1.grid(padx=5, pady=0, sticky=W, row=1)
        frame11 = LabelFrame(frame1, padx=0, pady=5, bg="#ffffff", borderwidth=0, highlightthickness=0, relief='ridge')
        frame11.grid(row=0, column=0, padx=(0, 20), pady=10, )
        frame12 = LabelFrame(frame1, padx=0, pady=0, bg="#ffffff", borderwidth=0, highlightthickness=0, relief='ridge')
        frame12.grid(row=0, column=1)
        frame13 = LabelFrame(self, padx=20, pady=0, bg="#ffffff", borderwidth=0, highlightthickness=0, relief='ridge')
        frame13.grid(row=2, column=0, padx=0, pady=0)
        label1 = Label(frame11, text="please inter your email ", bg="#ffffff")
        label1.grid(row=0, column=0, padx=5, pady=7, sticky=W)
        global my_entry1
        my_entry1 = Entry(frame11, width=50, highlightthickness=1, background="white")

        my_entry1.insert(0, "email")
        my_entry1.configure(state=DISABLED)

        def on_click1(event):
            my_entry1.configure(state=NORMAL)
            my_entry1.delete(0, END)
            # make the callback only work once
            my_entry1.unbind('<Button-1>', on_click_id)

        on_click_id = my_entry1.bind('<Button-1>', on_click1)
        my_entry1.grid(row=1, column=0, padx=5, pady=2, sticky=W, ipadx=70, ipady=5)

        label1 = Label(frame11, text="Please inter your password  ", bg="#ffffff")
        label1.grid(row=2, column=0, padx=5, pady=7, sticky=W)
        global my_entry2
        my_entry2 = Entry(frame11, width=50, show="*", highlightthickness=1)
        my_entry2.insert(0, "password")
        my_entry2.configure(state=DISABLED)

        def on_click2(event):
            my_entry2.configure(state=NORMAL)
            my_entry2.delete(0, END)
            # make the callback only work once
            my_entry2.unbind('<Button-1>', on_click_id2)

        on_click_id2 = my_entry2.bind('<Button-1>', on_click2)
        my_entry2.grid(row=3, column=0, padx=5, pady=2, sticky=W, ipadx=70, ipady=5)

        label1 = Label(frame11, text="Please inter time of waiting between tweets in hours  ", bg="#ffffff")
        label1.grid(row=4, column=0, padx=5, pady=7, sticky=W)
        global my_entry3
        my_entry3 = Entry(frame11, width=50, highlightthickness=1)
        my_entry3.insert(0, "sleeping time in hour ")
        my_entry3.configure(state=DISABLED)

        def on_click3(event):
            my_entry3.configure(state=NORMAL)
            my_entry3.delete(0, END)
            # make the callback only work once
            my_entry3.unbind('<Button-1>', on_click_id3)

        on_click_id3 = my_entry3.bind('<Button-1>', on_click3)
        my_entry3.grid(row=5, column=0, padx=5, pady=2, sticky=W, ipadx=70, ipady=5)

        def fill_input_data():
            session_data = {"email": my_entry1.get(), "password": my_entry2.get(), "waiting_time": my_entry3.get()
                            }
            pickle.dump(session_data, open("save.p", "wb"))

        def twitter_scraping(username, password, sleeping_time, i):
            columns = ["tweets"]
            df = pd.read_excel("tweets.xlsx", names=columns)
            contents = df.tweets.to_list()
            path = r"C:/chromedriver.exe"
            global driver

            if getattr(sys, "chromedriver.exe", False):
                chromedriver_path = (os.path.join(sys._MEIPASS, "chromedriver.exe"))
                driver = webdriver.Chrome(chromedriver_path)
            else:
                driver = webdriver.Chrome()
            driver.get("https://twitter.com/login")
            time.sleep(3)
            driver.find_element_by_xpath(
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input').send_keys(
                username)
            driver.find_element_by_xpath(
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input').send_keys(
                password)
            time.sleep(3)
            driver.find_element_by_xpath(
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div').click()
            time.sleep(6)
            while len(contents) > i:
                try:
                    i += 1
                    driver.get("https://twitter.com/home")
                    time.sleep(5)
                    tweet = driver.find_element_by_css_selector("br[data-text='true']")
                    tweet.send_keys(contents[i])
                    time.sleep(2)
                    button = driver.find_element_by_css_selector("div[data-testid='tweetButtonInline']")
                    button.click()
                    time.sleep(3)
                    r = open("last_session.txt", "w")
                    r.writelines(str(i))
                    r.close()
                    sleeping_time=float(sleeping_time)
                    sleeping_time = sleeping_time * 60 * 60
                    print("the sleeping time is ",sleeping_time)
                    time.sleep(sleeping_time)

                except:
                    pass

        def auto_fill():
            my_entry1.configure(state=NORMAL)
            my_entry2.configure(state=NORMAL)
            my_entry3.configure(state=NORMAL)

            my_entry1.delete(0, END)
            my_entry2.delete(0, END)
            my_entry3.delete(0, END)

            # f=open("data.txt","r")
            # data_items=f.read()
            # data_items=data_items.split("\n")
            try:
                session_data = pickle.load(open("save.p", "rb"))
                my_entry1.insert(0, session_data["email"])
                my_entry2.insert(0, session_data["password"])
                my_entry3.insert(0, session_data["waiting_time"])

            except:
                pass
            print("we reached end of function auto_fill")
            print("we are printing my_entry_1", my_entry1.get())

        def running_function():
            s1 = threading.Thread(target=twitter_scraping, args=[my_entry1.get(), my_entry2.get(), my_entry3.get(), i])
            s1.start()

        def stop():
            driver.quit()

        remember_button = Checkbutton(frame13, text="remember me", command=fill_input_data, bg="#ffffff")
        remember_button.grid(row=0, column=0, padx=5, pady=2, sticky=W, ipadx=5, ipady=5)

        auto_button = Button(frame13, text="Auto fill", command=auto_fill, bg="#FFD45B", borderwidth=2,
                             highlightthickness=0, relief='ridge')
        auto_button.grid(row=0, column=1, padx=5, sticky=E, pady=2, ipadx=30, ipady=5)

        start_button = Button(frame13, text="start", command=running_function, bg="#35A11B",
                              borderwidth=2, highlightthickness=0, relief='ridge')
        start_button.grid(row=0, column=2, padx=5, pady=2, sticky=E, ipadx=40, ipady=5)

        delete_button = Button(frame13, text="stop program", command=stop, bg="#FFD45B", borderwidth=2,
                               highlightthickness=0, relief='ridge')

        delete_button.grid(row=0, column=3, padx=0, pady=2, sticky='NSEW', ipadx=5, ipady=5)

        footer = Label(self, text="All rights reserved to Ali_Nasser foundation 2021-2022", bg="#C5C3C3")
        footer.grid(row=3, column=0, padx=5, pady=(10, 0), sticky=W)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
