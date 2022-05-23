#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by Oleg Zubak
# Version-1.0

from tkinter import (Frame, Button, Label, Text, Checkbutton, Entry, Listbox,
                     Menu, Tk, IntVar, StringVar)

from tkinter.constants import SINGLE, ACTIVE, END, SW, SE, UNDERLINE

import random

import os

import platform

import sys

import errno

from pathlib import Path

from tkinter.messagebox import showerror

from tkinter.filedialog import askdirectory, askopenfile

import colors


operation_platform = platform.system()

username = str(os.getlogin())  # get username from OS

user = str(username)  # username

homedir = str(Path.home())

initial_dir_music = "Music"

name_of_playlist = "mymusic"

# list here extensions what you need
main_ext = [".mp3", ".mp4", ".ogg", ".flac", ".webm", ".avi"]


class Playlist(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Playlist creation")
        self.master.maxsize(1000, 900)
        self.master.minsize(500, 400)
        self.grid(ipadx=15, ipady=15, rowspan=4, columnspan=5)
        self.create_widgets()

    def create_widgets(self):
        '''Define here all initial widgets
        and variables what you need on app
        start-up
        '''
        # Initializing our widgets and Frames
        self.frame = Frame()
        self.frame0 = Frame()
        self.frame1 = Frame()
        self.frame2 = Frame()

        self.frame.grid()
        self.frame0.grid()
        self.frame1.grid()
        self.frame2.grid()

        # Initial state allow to create playlist
        # through all path in selected directory
        # or only in root of selected directory
        self.initial_state = IntVar()
        self.path_mode = StringVar()
        # 0 - means to create playlist in all paths
        # 1 - only in root path
        self.initial_state.set(0)
        self.path_mode.set("All paths")
        # Select what file extension to be added to playlist
        self.playlist_ext_mode = IntVar()

        # multiple extension mode
        self.playlist_ext_mode.set(0)
        # self.playlist_ext_mode2.set(0)

        self.mode_variable = StringVar()
        self.mode_variable.set("Multiple extension mode")

        # Directory of where is playlist placed
        self.dir_playlist = homedir+os.sep+str(".config")+os.sep+str(
            "mpd")+os.sep+str("playlists")+os.sep+str(name_of_playlist)+str(".m3u")

        # Restart button
        restart_btn = Button(
            self.master, text="Restart script",
            command=self.restart,
            bg=colors.restart_btn_bg, pady=5,
            padx=5, activebackground=colors.on_hover_btn_bg
        )
        restart_btn.grid(sticky=SW, column=0, row=50)

        # Quit button
        self.quit_btn = Button(
            self.master, text="Quit", command=self.master.quit,
            bg=colors.quit_btn_bg, pady=5, padx=5,
            activebackground=colors.on_hover_btn_bg
        )
        self.quit_btn.grid(sticky=SE, column=10, row=50)

        def toggle_path():
            if self.initial_state.get() == 0:
                self.path_mode.set("All paths")
            else:
                self.path_mode.set("Only one path")

        # Checkbox - to choose the mode of playlist creation
        # By deafault it's setted to all paths (0-self.initial_state)
        self.checkbox = Checkbutton(
            self.frame2, textvariable=self.path_mode,
            variable=self.initial_state, command=lambda: toggle_path()
        )
        self.checkbox.grid()

        # change the mode text
        def toggle_mode():
            if self.playlist_ext_mode.get() == 0:
                self.mode_variable.set("Multiple extension mode")
            else:
                self.mode_variable.set("Single extension mode")

        # Ask which mode fo extension is selected
        self.checkbox_mode = Checkbutton(
            self.frame2, textvariable=self.mode_variable,
            variable=self.playlist_ext_mode, command=lambda: toggle_mode()
        )
        self.checkbox_mode.grid()

        self.extension_choose()

    def extension_choose(self):

        # Shuffle script for randomize llready existing songs in playlist
        shuffle_btn = Button(
            self.master, text="Suffle script",
            command=self.shuffle,
            bg=colors.shuffle_btn_bg, pady=5,
            padx=5, activebackground=colors.on_hover_btn_bg
        )

        # Label for explanation text
        self.label = Label(self.frame0)
        self.label["text"] = (
            " Files with next extension will be added to the playlist:"+"\n"
        )
        # checking how many rows will be our listbox heght
        get_size_listbox = int(len(main_ext))
        self.list_extensions = Listbox(
            self.frame0, height=get_size_listbox + 2,
            width=10, selectbackground=colors.list_extensions_bg,
            selectmode=SINGLE
        )
        for item in main_ext:
            # insert into listbox all extensions
            self.list_extensions.insert(END, item)

        shuffle_btn.grid(sticky=SW,
                         padx=10,
                         column=5, row=50
                         )

        self.label.grid(row=0, column=0)
        self.list_extensions.grid(row=1, column=0)

        self.button = Button(
            self.frame1, text="Choose folder",
            command=lambda: self.openfolder(), bg=colors.choose_folder_btn
        )
        self.button.grid(row=1, column=0)

    def openfolder(self):
        '''
        Here is asking folder from where to start,and if
        only one folder mode is choosed- the folder from where to take songs for playlist
        '''
        if self.playlist_ext_mode.get() != 0:
            # Check which extension is choosed by user
            self.selected_ext = int(self.list_extensions.curselection()[0])

        # Creating new ".m3u" empty file. Doesn't matter if allready exist same
        # file with same name end extention
        with open(self.dir_playlist, mode="w", encoding="utf-8") as clear_playlist:
            clear_playlist.write("")

        self.folder = str(askdirectory(
            title="Choose folder",
            # by default is setted "$HOME/Music" folder
            initialdir=homedir+os.sep+str(initial_dir_music)
        ))

        self.os_listing = os.listdir(self.folder)
        self.total_files_num = len(self.os_listing)
        self.show_songs()

    def show_songs(self):

        self.frame0.destroy()
        self.frame1.destroy()

        self.num_of_songs = []

        # For one extension
        if self.playlist_ext_mode.get() != 0:
            for i, f in enumerate(self.os_listing):
                if f.endswith(str(main_ext[self.selected_ext])):
                    self.num_of_songs.append(f)

        # For multiple extensions
        else:
            for i, f in enumerate(self.os_listing):
                for ext_ind, ext_name in enumerate(main_ext):
                    if f.endswith(str(ext_name)):
                        self.num_of_songs.append(f)

        self.num_of_songs_with_same_ext = int(len(self.num_of_songs))
        self.label_files = Label(
            self.frame2, padx=20
        )
        self.list = Listbox(
            self.frame2, width=60, selectbackground=colors.list_extensions_bg,
            selectmode=SINGLE
        )

        if self.playlist_ext_mode.get() != 0:
            for j, songs in enumerate(self.os_listing):
                if songs.endswith(str(main_ext[self.selected_ext])):
                    self.list.insert(END, songs)
        else:
            for j, songs in enumerate(self.os_listing):
                for ext_ind1, ext_name1 in enumerate(main_ext):
                    if songs.endswith(str(ext_name1)):
                        self.list.insert(END, songs)

        if self.num_of_songs_with_same_ext != 0:
            self.label_files = Label(
                self.frame2, padx=20
            )
            if self.playlist_ext_mode.get() != 0:
                self.label_files["text"] = str(
                    "There are " +
                    str(self.num_of_songs_with_same_ext)+" files " +
                    "with extension " + str(main_ext[self.selected_ext]) +
                    " from " + str(self.total_files_num)
                )
            else:
                self.label_files["text"] = str(
                    "There are " +
                    str(self.num_of_songs_with_same_ext)+" files " +
                    "with extension " + str(list(main_ext)) +
                    " from " + str(self.total_files_num)
                )
            self.list.grid(row=1, column=0)
            self.label_files.grid(row=0, column=0)
            self.button = Button(
                self.frame2, text="Create playlist",
                command=self.start_parsing
            )
            self.button.grid(row=2, column=1)
        else:
            self.label_files["text"] = str(
                "There are no any songs with reqiured extensions\n" +
                "Try in other directory"
            )
            self.list.grid_forget()
            self.label_files.grid(row=0, column=0)
            self.button = Button(
                self.frame2, text="Change path",
                command=self.repeat
            )
            self.button.grid(row=2, column=1)

    def repeat(self):
        '''
        Repeat choosing of folder
        '''
        self.label_files.grid_forget()
        self.openfolder()

    def start_parsing(self):
        '''
        Start to search music files and add them in tuple
        '''
        self.initialdir = str(self.folder)
        self.directories = []
        self.directories_2 = []
        self.frame.destroy()
        self.frame2.destroy()

        if self.playlist_ext_mode.get() != 0:
            with open(self.dir_playlist, mode="a", encoding="utf-8") as playlist:
                for num1, string1 in enumerate(self.num_of_songs):
                    if string1.endswith(str(main_ext[self.selected_ext])):
                        playlist.write(str(self.initialdir) +
                                       os.sep+str(string1)+"\n")

        else:
            for ext in main_ext:
                if ext == main_ext:

                    with open(self.dir_playlist, mode="a", encoding="utf-8") as playlist:
                        for num1, string1 in enumerate(self.os_listing):
                            if string1.endswith(str(main_ext)):
                                playlist.write(str(self.initialdir) +
                                               os.sep+str(string1)+"\n")

                else:

                    with open(self.dir_playlist, mode="a", encoding="utf-8") as playlist:
                        for num2, string2 in enumerate(self.os_listing):
                            if string2.endswith(str(ext)):
                                playlist.write(str(self.initialdir) +
                                               os.sep+str(string2)+"\n")
        if self.playlist_ext_mode.get() != 0:
            for i, f in enumerate(self.num_of_songs):
                if os.path.isdir(self.initialdir+os.sep+(f)) == True:
                    self.directories.append(self.initialdir+os.sep+(f))
            if self.initial_state.get() == 0:
                for i, f in enumerate(self.os_listing):
                    if os.path.isdir(self.initialdir+os.sep+(f)) == True:
                        self.directories.append(self.initialdir+os.sep+(f))

        else:
            for i, f in enumerate(self.os_listing):
                if os.path.isdir(self.initialdir+os.sep+(f)) == True:
                    self.directories.append(self.initialdir+os.sep+(f))

        if len(self.directories) > 0:
            if self.initial_state.get() == 0:
                self.parsing_more(self.directories)
            else:
                self.shellCommand()

    def parsing_more(self, content_of_path):

        list_directories = []
        list_directories2 = []
        for index, file_string in enumerate(content_of_path):

            list_Dir = os.listdir(file_string)

            for item, string in enumerate(list_Dir):
                if os.path.isdir(str(file_string)+os.sep+str(string)) == True:
                    list_directories.append(
                        str(file_string)+os.sep+str(string))
                else:
                    if self.playlist_ext_mode.get() != 0:
                        with open(self.dir_playlist, mode="a", encoding="utf-8") as playlist:
                            for extension in main_ext[self.selected_ext]:
                                if string.endswith(str(extension)):
                                    playlist.write(
                                        str(file_string)+os.sep+str(string)+"\n")
                    else:
                        with open(self.dir_playlist, mode="a", encoding="utf-8") as playlist:
                            for extension in main_ext:
                                if string.endswith(str(extension)):
                                    playlist.write(
                                        str(file_string)+os.sep+str(string)+"\n")

        if len(list_directories) > 0:
            self.parsing_more(list_directories)

        else:
            self.shellCommand()

    def shuffle(self):
        '''
        Read the playlist file and shuffle it.
        After open playlist file in writing mode and write lines in playlist 
        '''
        with open(self.dir_playlist, mode="r") as text_to_shuffle:
            text = text_to_shuffle.readlines()
            random.shuffle(text)
        with open(self.dir_playlist, mode="w") as shuffled:
            shuffled.writelines(text)

        self.shellCommand()

    def shellCommand(self):
        '''
        Lower perform a shell commands with Python3 
        module os.system
        "mpc clear" - clean the playlist
        ""mpc load"+str(name_of_playlist)" - add new created playlist to mpd 
        '''
        shellCommand = "mpc clear"
        os.system(shellCommand)
        print("cleaned")
        command_add = str("mpc load "+str(name_of_playlist))
        shellCommand_add = command_add
        os.system(shellCommand_add)
        print("added")

    def restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)


if __name__ == "__main__":
    root = Tk()
    app = Playlist(master=root)
    app.mainloop()
