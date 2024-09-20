#! /usr/bin/env python3
from datetime import datetime
from typing import Container
from numpy import roots
import pygame as pg
import tkinter as tk
from tkinter import Entry
from tkinter import filedialog, messagebox
from os import chdir, listdir, sys
from functools import partial
 
 
PAUSE = pg.USEREVENT+1
TRACK_END = pg.USEREVENT+1


 
class MusicFolder:
    def __init__(self):
        self.folder = None
 
    def get_files(self, tracklist, *args, **kwargs):
        self.folder = kwargs['folder']
        tracklist.delete(0, tk.END)
        chdir(self.folder)
        tracks = []
        formats = ['mp3', 'wav', 'ogg']
        playlist = listdir()
        for track in playlist:
            if track[-3:] in formats:
                tracklist.insert(tk.END, track)
        tracklist.select_set(0)
 
class Controls:
    def __init__(self):
        pass
 
    def play(self, *args, **kwargs):
        file = f'{kwargs["folder"]}/{kwargs["active"]}'
        pg.mixer.music.set_endevent(TRACK_END)
        try :
            pg.mixer.music.load(file)
            pg.mixer.music.play()
        except Exception:
            messagebox.showerror(title='No folder selected', \
            message='You must select a music folder to load the play list. The program will exit now.')
            sys.exit()
 
    def pause(self):
        pg.mixer.music.pause()
 
    def unpause(self):
        pg.mixer.music.unpause()
 
    def next(self, *args, **kwargs):
        pass
 
    def prev(self, *args, **kwargs):
        pass
 
    def stop(self, *args, **kwargs):
        pg.mixer.music.stop()
        pg.mixer.music.set_endevent()
        file = f'{kwargs["folder"]}/{kwargs["active"]}'
        pg.mixer.music.set_endevent(TRACK_END)
        pg.mixer.music.load(file)
 
 
class Player:
    def __init__(self, parent):
        self.parent = parent
        self.parent.update()
        self.width = self.parent.winfo_width()
        self.height = self.parent.winfo_height()
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)
        bgcolor = 'light blue'
        fgcolor = 'navy'
        self.folder = None
        pg.init()
        pg.mixer.init()
 
 
        pg.mixer.music.set_endevent(TRACK_END)
 
        self.control = Controls()
        self.music = MusicFolder()
 
        # Container
        container = tk.Frame(self.parent)
        container.grid(column=0, row=0, sticky='news')
 
        # Contains the header image/canvas
        headerframe = tk.Frame(container)
        headerframe.grid(column=0, row=0, sticky='new', pady=2, padx=2)
 
        # Contains 3 columns of info - status/track/choose folder button
        frame1 = tk.Frame(container)
        frame1.grid(column=0, row=1, sticky='new', pady=2)
 
        # Status Label
        self.status_label = tk.Label(frame1, padx=8, bg=bgcolor, fg=fgcolor, \
        width=17, text='No status', anchor='w')
        self.status_label['bd'] = 1
        self.status_label['relief'] = 'ridge'
        self.status_label.grid(column=0, row=0, sticky='news', padx=2)
 
        # Track playing label
        self.track_label = tk.Label(frame1, padx=8, bg=bgcolor, fg=fgcolor, \
        width=70, text='No track is playing', anchor='w')
        self.track_label['bd'] = 1
        self.track_label['relief'] = 'ridge'
        self.track_label.grid(column=1, row=0, sticky='news', padx=4)


        # Button for populating our listbox with tracks
        self.button = tk.Button(frame1, text='Enter Age and Gender', \
        fg='navy', bg='lightsteelblue')
        self.button['command'] = partial(self.get_music)
        self.button.grid(column=2, row=0, sticky='new', padx=2)
        self.button.bind('<Enter>', partial(self.on_enter, self.button))
        self.button.bind('<Leave>', partial(self.on_exit, self.button))
 
        # Contains 3 columns - spacer/listbox/scrollbar
        frame2 = tk.Frame(container)
        frame2.grid(column=0, row=2, sticky='new', pady=2)
        frame2.grid_columnconfigure(0, weight=3)
 
        # Just a spacer label. May use to show album image?
        spacer_label = tk.Label(frame2, bg='silver', bd=1, relief='ridge')
        spacer_label['height'] = 15
        spacer_label['width'] = 30
        spacer_label.grid(column=0, row=0, sticky='news', padx=2)
 
        # Frame for listbox to give appearence of text not against side
        padframe = tk.Frame(frame2, bd=1, relief='ridge', bg='aliceblue', padx=8, \
        pady=5)
        padframe['highlightcolor'] = '#999999'
        padframe['highlightbackground'] = '#999999'
        padframe['highlightthickness'] = 1
        padframe.grid(column=2, row=0, sticky='news', padx=2)
        padframe.grid_rowconfigure(0, weight=3)
        padframe.grid_columnconfigure(0, weight=3)
 
        # Listbox and scrollbar
        self.scrollbar = tk.Scrollbar(frame2, orient='vertical')
        self.playlist = tk.Listbox(padframe, width=70, bd=0, bg='aliceblue')
        self.playlist['yscrollcommand'] = self.scrollbar.set
        self.playlist['selectmode'] = 'single'
        self.playlist['selectbackground'] = 'lightsteelblue'
        self.playlist['selectforeground'] = 'navy'
        self.playlist['highlightcolor'] = 'white'
        self.playlist['highlightbackground'] = 'white'
        self.playlist['highlightthickness'] = 0
        self.playlist['bd'] = 0
        self.playlist.grid(column=0, row=0, sticky='news')
        self.scrollbar.grid(column=3, row=0, sticky='ns', padx=2)
 
        # Contains the control buttons - play/stop/next/prev
        frame3 = tk.Frame(container)
        frame3.grid(column=0, row=3, sticky='new', pady=2)
        for i in range(4):
            frame3.grid_columnconfigure(i, weight=3, uniform='control_btns')
 
        # The buttons - play/stop/next/prev
        # play button will double as a pause button
        self.play_btn = tk.Button(frame3, text='Play', fg='navy', bg='lightsteelblue')
        self.play_btn.grid(column=0, row=0, sticky='new', padx=2)
        self.play_btn['command'] = partial(self.play, state='play')
        self.play_btn.bind('<Enter>', partial(self.on_enter, self.play_btn))
        self.play_btn.bind('<Leave>', partial(self.on_exit, self.play_btn))
 
 
        self.stop_btn = tk.Button(frame3, text='Stop', fg='navy', bg='lightsteelblue')
        self.stop_btn.grid(column=1, row=0, sticky='new', padx=2)
        self.stop_btn['command'] = partial(self.play, state='stop')
        self.stop_btn.bind('<Enter>', partial(self.on_enter, self.stop_btn))
        self.stop_btn.bind('<Leave>', partial(self.on_exit, self.stop_btn))
 
 
        self.next_btn = tk.Button(frame3, text='Next', fg='navy', bg='lightsteelblue')
        self.next_btn.grid(column=2, row=0, sticky='new', padx=2)
        self.next_btn['command'] = partial(self.next)
        self.next_btn.bind('<Enter>', partial(self.on_enter, self.next_btn))
        self.next_btn.bind('<Leave>', partial(self.on_exit, self.next_btn))
 
        self.back_btn = tk.Button(frame3, text='Prev', fg='navy', bg='lightsteelblue')
        self.back_btn.grid(column=3, row=0, sticky='new', padx=2)
        self.back_btn['command'] = partial(self.prev)
        self.back_btn.bind('<Enter>', partial(self.on_enter, self.back_btn))
        self.back_btn.bind('<Leave>', partial(self.on_exit, self.back_btn))
 
 
    
    def get_music(self):
        #06
        def age():
            if my_entry.get():
                # Get the current year
                
                # Calculate The Age
                your_age = my_entry.get()
                your_gender = my_entry2.get()
                # Show age in message box
                messagebox.showinfo("Confirmation", f"Your age is {your_age}, your gender is {your_gender}")
                self.folder = filedialog.askdirectory()
                self.music.get_files(self.playlist, folder=self.folder)
                popup.destroy()

            else:
                # Show Error Message
                messagebox.showerror("Error", "You forgot to enter your age!")

        popup = tk.Tk()
        popup.title('Details')

        popup.geometry("500x300")
        
        my_label = tk.Label(popup, text="Enter Your Details", font=("Helvetica", 18))
        my_label.pack(pady=20)

        my_label1 = tk.Label(popup, text="Age", font=("Helvetica", 15))
        my_label1.pack(pady=0)
        my_entry = Entry(popup, font=("Helvetica", 12))
        my_entry.pack(pady=10)

        my_label2 = tk.Label(popup, text="Gender", font=("Helvetica", 15))
        my_label2.pack(pady=0)
        my_entry2 = Entry(popup, font=("Helvetica", 12))
        my_entry2.pack(pady=10)

        my_button = tk.Button(popup, text="OK!", font=("Helvetica", 18), command=age)
        my_button.pack(pady=20)
        
        popup.mainloop()

        
        # self.folder = filedialog.askdirectory()
        # self.music.get_files(self.playlist, folder=self.folder)
 
    # Define some button animations
    def on_enter(self, btn, event):
        btn['bg'] = 'powderblue'
        btn['fg'] = 'navy'
        btn['cursor'] = 'hand2'
 
    def on_exit(self, btn, event):
        btn['bg'] = 'lightsteelblue'
        btn['fg'] = 'navy'
 
    def next(self):
        pg.mixer.music.stop()
        index = self.playlist.curselection()
        if index:
            next_index = 0
            if len(index) > 0:
                last_index = int(index[-1])
                self.playlist.selection_clear(index)
 
                if last_index < self.playlist.size()-1:
                    next_index = last_index + 1
            self.playlist.activate(next_index)
            self.playlist.selection_set(next_index)
            self.status_label['text'] = 'Now Playing here'
            self.play(state='play')
        else:
            pass
 
    def prev(self):
        try:
            pg.mixer.music.stop()
            index = self.playlist.curselection()
            last_index = int(index[-1])
            if last_index == 0:
                last_index = self.playlist.size()
            self.playlist.selection_clear(index)
            last_index = last_index - 1
            self.playlist.activate(last_index)
            self.playlist.selection_set(last_index)
            self.play(state='play')
        except Exception:
            pass
 
    def play(self, *args, **kwargs):
        if self.playlist.get(tk.ACTIVE):
            state = kwargs['state']
            self.track_label['text'] = self.playlist.get(tk.ACTIVE)[:-4]
 
            if state == 'play':
                self.play_btn['text'] = 'Pause'
                self.play_btn['command'] = partial(self.play, state='pause')
                self.status_label['text'] = 'Now Playing'
                self.control.play(active=self.playlist.get(tk.ACTIVE), folder=self.folder)
 
 
            elif state == 'pause':
                self.play_btn['text'] = 'Resume'
                self.play_btn['command'] = partial(self.play, state='unpause')
                self.status_label['text'] = 'Paused'
                self.control.pause()
 
            elif state == 'unpause':
                self.play_btn['text'] = 'Pause'
                self.play_btn['command'] = partial(self.play, state='pause')
                self.status_label['text'] = 'Now Playing'
                self.control.unpause()
 
            else:
                try:
                    index = self.playlist.curselection()
                    self.play_btn['text'] = 'Play'
                    self.play_btn['command'] = partial(self.play, state='play')
                    self.status_label['text'] = 'No status'
                    self.track_label['text'] = 'No track is playing'
                    self.playlist.selection_clear(index)
                    self.playlist.select_set(0)
                    self.playlist.activate(0)
                    self.control.stop(folder=self.folder, active=self.playlist.get(tk.ACTIVE))
                except Exception:
                    pass
        else:
            messagebox.showerror(title='No folder selected.', message='Please choose a folder with music files.')
            pass
 
 
 
 
def main():
    root = tk.Tk()
    root.title('Tkinter Music Player')
    root.geometry('805x315+250+250')
    root.resizable(0, 0)
    root['padx'] = 10
    root['pady'] = 5
    Player(root)
    root.mainloop()
 
if __name__ == "__main__":
    main()