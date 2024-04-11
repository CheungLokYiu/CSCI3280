#!/usr/bin/python3
import customtkinter
from CTkListbox import *
import os
import time
import threading
import function
import pyaudio
import json
import socket
import signal
import math
import struct
import platform
from protocol import DataType, Protocol
from collections import defaultdict
from PIL import Image
import visualize

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # delete all wav files in the directory
        for file in os.listdir("."):
            if file.endswith(".wav"):
                os.remove(file)

        #initialize parameters
        self.wav_file_name = ""
        self.paused = True
        self.playing = False
        self.audio_length = 0
        self.current_sec = 0
        self.after_id = None
        self.audio_timer = 0
        self.last_file = ''
        self.selected_file_index = 0
        self.edited_frame = []
        self.edit_start_time = 0
        self.edit_end_time = 0
        self.edit_total_second = 0
        self.get_list_detail = True
        self.recordingFrames = [[],[]]

        # configure window
        self.title("Peer to Peer Voice Chat")
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=6)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create scrollable frame
        self.listbox = CTkListbox(master=self, 
                                  command=self.show_value, 
                                  width=350,
                                  justify="center", 
                                  highlight_color="#AD88C6",
                                  hover_color="#AD88C6",
                                  fg_color="#7469B6", 
                                  label_text="Chat Room List", 
                                  label_fg_color="#7469B6",
                                  label_font=(None,30))
        self.listbox.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.listbox.grid_rowconfigure(4, weight=1)
        # the loop the files from the direct directory path
        self.refresh_list()

        # the control bar under the chat room list
        self.room_control_bar = customtkinter.CTkFrame(self, fg_color="#474F7A")
        self.room_control_bar.grid(row=1, column=0, padx=2, pady=1, sticky="nsew")
        self.room_control_bar.grid_columnconfigure((0, 2, 4), weight=1)

        # the create button
        self.create_button = customtkinter.CTkButton(self.room_control_bar, 
                                                     width=100, 
                                                     text="CREATE", 
                                                     font=("Arial", 25, "bold"), 
                                                     fg_color="#AD88C6",
                                                     hover_color="#7469B6",
                                                     command = self.create_room_dialog
                                                     )
        self.create_button.grid(row=0, column=0,rowspan=2, padx=(5,5), pady=(10, 5), sticky="nsew")

        # the join button
        self.join_button = customtkinter.CTkButton(self.room_control_bar, 
                                                     width=100, 
                                                     text="JOIN", 
                                                     font=("Arial", 25, "bold"), 
                                                     fg_color="#AD88C6",
                                                     hover_color="#7469B6",
                                                     command = self.join_room_dialog
                                                     )
        self.join_button.grid(row=0, column=4,rowspan=2, padx=(5,5), pady=(10, 5), sticky="nsew")


        #creaet main view
        self.main_view = customtkinter.CTkFrame(self, fg_color="#F9F5F6")
        self.main_view.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.main_view.grid_columnconfigure(0, weight=1) 
        self.main_view.grid_rowconfigure(2, weight=1)
        #create rename button
        self.rename_button = customtkinter.CTkButton(self.main_view, 
                                                     width=100, 
                                                     text="RENAME", 
                                                     font=("Arial", 30, "bold"), 
                                                     fg_color="#7469B6",
                                                     hover_color="#AD88C6",
                                                     command=self.open_rename_dialog)
        self.rename_button.grid(row=0, column=1, padx=10, pady=(5, 5), sticky="nsew")
        #create edit button
        self.edit_button = customtkinter.CTkButton(self.main_view, 
                                                     width=100, 
                                                     text="EDIT", 
                                                     font=("Arial", 30, "bold"), 
                                                     fg_color="#7469B6",
                                                     hover_color="#AD88C6",
                                                     command=self.open_edit_dialog)
        self.edit_button.grid(row=0, column=2, padx=10, pady=(5, 5), sticky="nsew")
        #create trim audio button
        self.trim_button = customtkinter.CTkButton(self.main_view, 
                                                     width=100, 
                                                     text="TRIM", 
                                                     font=("Arial", 30, "bold"), 
                                                     fg_color="#7469B6",
                                                     hover_color="#AD88C6",
                                                     command=self.open_trim_dialog)
        self.trim_button.grid(row=0, column=3, padx=10, pady=(5, 5), sticky="nsew")
        #create file name label
        self.file_name_label = customtkinter.CTkLabel(self.main_view,
                                            text="", text_color="#7469B6", font=(None, 20, 'bold'))
        self.file_name_label.grid(row=1, column=0, columnspan=4, padx=0, pady=0, sticky="nsew")
        #create image view
        self.audio_image = customtkinter.CTkImage(dark_image=Image.open("out.png"), size=(450, 450))
        self.image_button = customtkinter.CTkButton(self.main_view, image=self.audio_image, fg_color="#F9F5F6", hover_color="#F9F5F6", text="")
        self.image_button.grid(row=2, column=0, columnspan=4, padx=0, pady=0, sticky="nsew")
        #create text of audio label
        self.audio_text_label = customtkinter.CTkLabel(self.main_view,
                                            text="", text_color="#7469B6", font=(None, 15, 'bold'))
        self.audio_text_label.grid(row=3, column=0, columnspan=4, padx=0, pady=0, sticky="nsew")

        #create control panel
        self.control_panel_bar = customtkinter.CTkFrame(self, fg_color="#474F7A")
        self.control_panel_bar.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")
        self.control_panel_bar.grid_columnconfigure((0, 2, 5, 7), weight=1)
        #create recording button
        self.record_button = customtkinter.CTkButton(self.control_panel_bar, 
                                                     width=100, 
                                                     text="🎙", 
                                                     font=("Arial", 30, "bold"),
                                                     fg_color="#7469B6",
                                                     hover_color="#AD88C6", 
                                                     command=self.record_click_listener)
        self.record_button.grid(row=0, column=1, rowspan=2, padx=0, pady=(5, 5), sticky="nsew")
        self.recording = False
        #create timer
        self.timer_label = customtkinter.CTkLabel(self.control_panel_bar,
                                            text="00:00:00")
        self.timer_label.grid(row=0, column=2, rowspan=2, padx=20, pady=0)
        #create play button
        self.play_button = customtkinter.CTkButton(self.control_panel_bar, 
                                                     width=100, 
                                                     text="⏵", 
                                                     font=("Arial", 30, "bold"), 
                                                     fg_color="#7469B6",
                                                     hover_color="#AD88C6", 
                                                     command=self.play_audio)
        self.play_button.grid(row=0, column=3, rowspan=2, padx=10, pady=(5, 5), sticky="nsew")
        #create pause button
        self.pause_button = customtkinter.CTkButton(self.control_panel_bar, 
                                                     width=100, 
                                                     text="⏸", 
                                                     font=("Arial", 30, "bold"),
                                                     fg_color="#7469B6",
                                                     hover_color="#AD88C6",  
                                                     command=self.pause_audio)
        self.pause_button.grid(row=0, column=4, rowspan=2, padx=10, pady=(5, 5), sticky="nsew")
        #create speed selection button
        self.speed_label = customtkinter.CTkLabel(self.control_panel_bar, 
                                                  text="Speed Mode:",
                                                  text_color="white", 
                                                  anchor="w")
        self.speed_label.grid(row=0, column=6, padx=20, pady=0)
        self.speed_optionemenu = customtkinter.CTkOptionMenu(self.control_panel_bar, 
                                                             values=["2.0x", "1.0x", "0.5x"],
                                                             fg_color="#7469B6",
                                                             button_color="#7469B6", 
                                                             button_hover_color="#AD88C6",
                                                             dropdown_fg_color="#7469B6",
                                                             dropdown_hover_color="#AD88C6",
                                                             command=self.change_speed)
        self.speed_optionemenu.grid(row=1, column=6, padx=0, pady=(0, 5), sticky="nsew")
        self.speed_optionemenu.set("1.0x")
        
    #refresh the recording explorer
    def refresh_list(self):
        for file in os.listdir("."):
            file_name = f"{file:70s}"
            file_type = os.path.splitext(file)[1]
            #only show the wav file
            if file_type == ".wav":
                file_time = time.strftime("\n\n%Y-%m-%d (%H:%M:%S)", time.strptime(time.ctime(os.path.getmtime(file))))
                self.listbox.insert(file, file_name + file_time)
            self.playing = False

    #take the data of the .wav file here after you click the left explorer
    def show_value(self, selected_option):
        if self.get_list_detail:
            self.playing = False
            self.speed_optionemenu.set('1.0x')
            self.selected_file_index = self.listbox.curselection()
            if self.last_file != '':
                function.savefile(self.last_file,function.speed_func(self.last_file, float(1)*function.RATE)) 
            self.wav_file_name = selected_option.split()
            self.last_file = self.wav_file_name[0]
            self.current_sec = 0
            #show the selected audio details on right handside
            self.file_name_label.configure(text=self.wav_file_name[0])
            self.show_audio_length()
            self.show_image()
            self.show_audio_text()

    #initialize the main view
    def init_main_view(self):
        self.audio_text_label.configure(text="")
        self.timer_label.configure(text="00:00:00")
        self.file_name_label.configure(text="")
        self.audio_image.configure(dark_image=Image.open("out.png"))
        self.image_button.configure(image=self.audio_image)

    #show the visualized audio image
    def show_image(self):
        visualize.plotSignalWave(self.wav_file_name[0], "photo_image.png")
        self.audio_image.configure(dark_image=Image.open("photo_image.png"))
        self.image_button.configure(image=self.audio_image)
    
    #show the audio text
    def show_audio_text(self):
        audio_text = function.wav_to_text(self.wav_file_name[0])
        self.audio_text_label.configure(text=audio_text)

    #show the audio length on the timer
    def show_audio_length(self):
        self.file_data = function.open_file(self.wav_file_name[0])
        length = self.file_data["length"]
        hour = length // 3600
        min = (length - hour * 60) // 60
        sec = length - hour * 3600 - min * 60
        self.timer_label.configure(text=f"{int(hour):02d}:{int(min):02d}:{int(sec):02d}")

    #record button on click listener
    def record_click_listener(self):
        self.init_main_view()
        if self.recording:
            self.recording = False
            self.record_button.configure(text_color = "white")
        else:
            self.recording = True
            self.record_button.configure(text_color = "red")
            #create a thread to call record_action() function
            threading.Thread(target=self.record_action).start()


    #implement the record function
    def record_action(self):
        # get data from self.recording_stream and self.playing_stream (combine them)
        start = time.time()
        while self.recording:
            self.recordingFrames[0].append(self.recording_stream.read(1024))

            passed = time.time() - start
            sec = passed % 60
            min = passed //60
            hour = min // 60
            self.timer_label.configure(text=f"{int(hour):02d}:{int(min):02d}:{int(sec):02d}")
        #save the fresh recording file
        exist = True
        i = 1
        while exist:
            if os.path.exists(f"Output{i}.wav"):
                i += 1
            else:
                exist = False

        # combine the recording and playing frames
        frames = self.recordingFrames[0] + self.recordingFrames[1]

        function.convert_audio_to_wav(frames, f"Output{i}")
        # clear the recording frames
        self.recordingFrames = [[], []]
        self.refresh_list()

    #start playing the recording
    def start_playing(self):  
        p = pyaudio.PyAudio()
        chunk = 1024
        stream = p.open(format = p.get_format_from_width(self.file_data["bytesperframe"]), channels = self.file_data["nchannel"], rate = self.file_data["framerate"], output = True)
        cur_bytes = int(self.current_sec * 2 * function.RATE) - int((self.current_sec * 2 * function.RATE)%2)
        data = self.file_data["audio_data"][cur_bytes:cur_bytes+chunk*2]
        cur_bytes += chunk*2

        while data != b"" and self.playing:
            if not self.paused:
                stream.write(data)
                data = self.file_data["audio_data"][cur_bytes:cur_bytes+chunk*2]
                cur_bytes += chunk*2
                self.current_sec = cur_bytes/2/function.RATE
                #print time label
                hour = self.current_sec // 3600
                min = (self.current_sec - hour * 60) // 60
                sec = self.current_sec - hour * 3600 - min * 60
                self.timer_label.configure(text=f"{int(hour):02d}:{int(min):02d}:{int(sec):02d}")

        self.playing=False

        if data == b"":
            self.current_sec = 0
            self.change_speed('1.0x')

        stream.close()   
        p.terminate()

    #play button on click listener
    def play_audio(self):
        if not self.playing:
            self.playing = True  
            #create thread to call start_playing() function          
            threading.Thread(target=self.start_playing, daemon=True).start()

        if self.after_id is None:
            print()
        self.paused = False

    #pause button on click listener
    def pause_audio(self):
        self.paused = True
        
        if self.after_id:
            self.after_id = None

    #speed control
    def change_speed(self, speed_mode: str):
        self.speed_optionemenu.set(speed_mode)
        data = function.speed_func(self.wav_file_name[0], float(speed_mode[0:3])*function.RATE)
        function.savefile(self.wav_file_name[0], data)
        self.refresh_list()
        #sync the explorer
        self.get_list_detail = False
        self.listbox.activate(self.selected_file_index)
        self.get_list_detail = True

        self.file_data = data

    #rename button on click listener
    def open_rename_dialog(self):
        self.listbox.activate(self.selected_file_index)
        rename_dialog = customtkinter.CTkInputDialog(text="Type in a new name to replace current file's name\ne.g. XXXX.wav", title="Rename Audio")
        input_value = rename_dialog.get_input()
        #replace the old file name with new inputed name
        os.rename(self.wav_file_name[0], input_value)
        #synchronize the data
        self.wav_file_name[0] = input_value
        self.last_file = ""
        self.listbox.delete(self.selected_file_index)
        self.refresh_list()
        self.init_main_view()

    #trim button on click listener
    def open_trim_dialog(self):
        self.change_speed('1.0x')
        self.listbox.activate(self.selected_file_index)
        trim_dialog = customtkinter.CTkInputDialog(text="Type in the start time and end time to trim the audio\ne.g. 00:00:00.00 - 00:00:00.00", title="Trim Audio")
        input_value = trim_dialog.get_input()
        split_input = input_value.replace(':', ' ').replace('-', ' ').split()
        start_time = float(split_input[0]) * 3600 + float(split_input[1]) * 60 + float(split_input[2])
        end_time = float(split_input[3]) * 3600 + float(split_input[4]) * 60 + float(split_input[5])
        data = function.trim(self.wav_file_name[0], start_time, end_time)
        # function.streamplay(data)
        function.savefile(self.wav_file_name[0], data)
        self.refresh_list()
        self.show_image()
        self.show_audio_text()
        self.show_audio_length()
        
    #edit button on click listener
    def open_edit_dialog(self):
        self.change_speed('1.0x')
        self.listbox.activate(self.selected_file_index)
        edit_dialog = customtkinter.CTkInputDialog(text="Type in the time of audio to edit with\ne.g. 00:00:00.00 - 00:00:00.00", title="Edit Audio")
        input_value = edit_dialog.get_input()
        split_input = input_value.replace(':', ' ').replace('-', ' ').split()
        self.edit_start_time = float(split_input[0]) * 3600 + float(split_input[1]) * 60 + float(split_input[2])
        self.edit_end_time = float(split_input[3]) * 3600 + float(split_input[4]) * 60 + float(split_input[5])
        self.edit_total_second = self.edit_end_time - self.edit_start_time
        self.record_button.configure(text_color = "red")
        #create a thread to call edit_record() function
        threading.Thread(target=self.edit_record).start()

    #start edit recording 
    def edit_record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format = pyaudio.paInt16, channels = 1, rate = 44100, input = True, input_device_index = 2, frames_per_buffer = 1024)
        start = time.time()
        frames = [] 
        for i in range (0, int(44100 / 1024 * self.edit_total_second)):
            data = stream.read(1024)
            frames.append(data)

            passed = time.time() - start
            sec = passed % 60
            min = passed //60
            hour = min // 60
            self.timer_label.configure(text=f"{int(hour):02d}:{int(min):02d}:{int(sec):02d}")
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        #replace the old audio with the fresh record
        replace_data = function.replace_audio(self.edit_start_time, self.edit_end_time, b''.join(frames), self.file_data)
        
        filename = self.wav_file_name[0].replace('.wav', '')
        function.convert_audio_to_wav(replace_data, filename)
        self.refresh_list()
        self.record_button.configure(text_color = "white")
        self.init_main_view()
        return
    
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
        
    #create button on click listener
    def create_room_dialog(self):
        # self.listbox.activate(self.selected_file_index)
        self.ip = App.get_ip()

        while 1:
            try:
                create_dialog = customtkinter.CTkInputDialog(text="You are currently hosting a server. Enter port number to run on", title="Port Number")
                self.port = int(create_dialog.get_input())
                self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.s.settimeout(5)
                self.s.bind((self.ip, self.port))
                break
            except:
                self.addNotes("Couldn't bind to that port.\n")

        self.clients = {}
        self.clientCharId = {}
        self.rooms = defaultdict(list)
        self.client_room = {}

        receive_thread = threading.Thread(target=self.receiveData)
        receive_thread.daemon = True  # Set the thread as a daemon so it terminates when the main thread ends
        receive_thread.start()

        # Change the whole view to the server view (only text)
        # remove the create and join button
        self.create_button.grid_forget()
        self.join_button.grid_forget()
        # create the terminate button
        self.terminate_button = customtkinter.CTkButton(self.room_control_bar,
                                                        width=100,
                                                        text="TERMINATE",
                                                        font=("Arial", 25, "bold"),
                                                        fg_color="#AD88C6",
                                                        hover_color="#7469B6",
                                                        command=self.terminate_server)
        self.terminate_button.grid(row=0, column=2, rowspan=2, padx=(5, 5), pady=(10, 5), sticky="nsew")


    def addNotes(self, text):
        self.audio_text_label.configure(text=self.audio_text_label.cget("text") + text)

    def receiveData(self):   
        self.addNotes('Running on IP: ' + self.ip + '\n')
        self.addNotes('Running on port: ' + str(self.port) + '\n')
        
        while True:
            try:
                data, addr = self.s.recvfrom(1026)
                message = Protocol(datapacket=data)
                self.handleMessage(message, addr)
            except socket.timeout:
                pass

    def handleMessage(self, message, addr):
        if self.clients.get(addr, None) is None:
            try:
                if message.DataType == DataType.GetRoom:
                    key = list(self.rooms.keys())
                    room_numbers = list(self.client_room.values())    
                    # make the list as json format
                    output = json.dumps(dict(zip(key, room_numbers)))           
                    ret = Protocol(dataType=DataType.GetRoom, room=0, data=output.encode(encoding='UTF-8'))
                    self.s.sendto(ret.out(), addr)
                    return
                if message.DataType != DataType.Handshake:
                    return

                name = message.data.decode(encoding='UTF-8')
                room = message.room

                self.clients[addr] = name
                self.clientCharId[addr] = len(self.clients)
                self.rooms[room].append(addr)
                self.client_room[addr] = room

                update_message = self.get_update_message(addr, room, "joined")
                users_message = self.get_online_users(room)
                notification = "".join(update_message + users_message)
                self.addNotes(notification + '\n')

                ret = Protocol(dataType=DataType.Handshake, room=message.room, data="".join(users_message).encode(encoding='UTF-8'))
                ret_b = Protocol(dataType=DataType.Handshake, room=message.room, data=notification.encode(encoding='UTF-8'))
                self.s.sendto(ret.out(), addr)
                self.broadcast(addr, room, ret_b)
            except Exception as err:
                print(err)
            return

        elif message.DataType == DataType.ClientData:
            self.broadcast(addr, message.room, message)

        elif message.DataType == DataType.Terminate:
            room = message.room
            update_message = self.get_update_message(addr, room, "left")
            self.clients.pop(addr)
            self.clientCharId.pop(addr)
            self.rooms[room].remove(addr)
            self.client_room.pop(addr)
            users_message = self.get_online_users(room)
            notification = "".join(update_message + users_message)
            self.addNotes(notification + '\n')
            message_ter = Protocol(dataType=DataType.Terminate, room=room, data=notification.encode("utf-8"))
            self.broadcast(addr, message.room, message_ter)

    def broadcast(self, sentFrom, room, data):
        if not data.head:
            data.head = self.clientCharId[sentFrom]
        for client in self.rooms[room]:
            if client[0] != sentFrom[0] or client[1] != sentFrom[1]:
                try:
                    self.s.sendto(data.out(), client)
                except Exception as err:
                    raise err

    def get_online_users(self, room):
        users = ["Users online in room %s : " % room]
        if len(self.rooms[room]) == 0:
            users.append("0")
        for client in self.rooms[room]:
            if len(users) > 1:
                users.append(", ")
            users.append("\"%s\" (%s:%s)" % (self.clients[client], client[0], client[1]))
        return users

    def get_update_message(self, addr, room, state):
        message_list = ["User \"%s\" (%s:%s) has %s voice chat, room %s.\n" % (self.clients[addr], addr[0], addr[1], state, room)]
        return message_list

    # join button on click listener    
    def join_room_dialog(self):
        # self.listbox.activate(self.selected_file_index)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connected = False
        join_dialog = customtkinter.CTkInputDialog(text="Enter your name", title="Client Name")
        self.name = join_dialog.get_input()

        while 1:
            try:
                join_dialog = customtkinter.CTkInputDialog(text="Enter IP address of server", title="Server IP")
                self.target_ip = join_dialog.get_input()
                join_dialog = customtkinter.CTkInputDialog(text="Enter target port of server", title="Server Port")
                self.target_port = int(join_dialog.get_input())


                # join_dialog = customtkinter.CTkInputDialog(text="Enter the id of room", title="Room ID")
                # self.room = int(join_dialog.get_input())
                # list out the available rooms or create a new room
                # retrieve the list of rooms from the server
                message = Protocol(dataType=DataType.GetRoom, room=0, data=b'')
                self.s.sendto(message.out(), (self.target_ip, self.target_port))
                data, addr = self.s.recvfrom(1026)
                datapack = Protocol(datapacket=data)
                data_str = datapack.data
                data_dict = json.loads(data_str)
                room_list = list(data_dict.values())
                room_dialog = customtkinter.CTkInputDialog(text="Enter the id of room (Available rooms: %s)" % room_list, title="Room ID")
                for i in room_list:
                    self.listbox.insert(i, f"Room {i}")
                self.room = int(room_dialog.get_input())
                self.server = (self.target_ip, self.target_port)
                self.connect_to_server()
                #delete items in the listbox
                self.listbox.delete(0, 'end')
                break
            except Exception as err:
                print(err)
                self.addNotes("Couldn't connect to server...\n")

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)
        self.recording_stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        # Termination handler
        def handler(signum, frame):
            print("\033[2KTerminating...")
            message = Protocol(dataType=DataType.Terminate, room=self.room, data=self.name.encode(encoding='UTF-8'))
            self.s.sendto(message.out(), self.server)
            if platform.system() == "Windows":
                os.kill(os.getpid(), signal.SIGBREAK)
            else:
                os.kill(os.getpid(), signal.SIGKILL)

        if platform.system() == "Windows":
            signal.signal(signal.SIGBREAK, handler)
        else:
            signal.signal(signal.SIGTERM, handler)
        signal.signal(signal.SIGINT, handler)

        # start threads
        self.s.settimeout(0.5)
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        # self.send_data_to_server()
        # make a thread to send data to server
        threading.Thread(target=self.send_data_to_server).start()

        # remove the create and join button
        self.create_button.grid_forget()
        self.join_button.grid_forget()

        # create the terminate button
        self.terminate_button = customtkinter.CTkButton(self.room_control_bar,
                                                        width=100,
                                                        text="TERMINATE",
                                                        font=("Arial", 25, "bold"),
                                                        fg_color="#AD88C6",
                                                        hover_color="#7469B6",
                                                        command=self.terminate_client)
        
        # create mute button
        self.mute_button = customtkinter.CTkButton(self.room_control_bar,
                                                        width=100,
                                                        text="MUTE",
                                                        font=("Arial", 25, "bold"),
                                                        fg_color="#AD88C6",
                                                        hover_color="#7469B6",
                                                        command=self.mute_client)
        
        self.terminate_button.grid(row=0, column=2, rowspan=2, padx=(5, 5), pady=(10, 5), sticky="nsew")
        self.mute_button.grid(row=0, column=4, rowspan=2, padx=(5, 5), pady=(10, 5), sticky="nsew")

    def terminate_server(self):
        self.s.close()
        self.addNotes("Server terminated.\n")
        exit()

    def terminate_client(self):
        self.s.close()
        self.addNotes("Client terminated.\n")
        exit()
        
    def mute_client(self):
        self.recording_stream.stop_stream()
        self.addNotes("Client muted.\n")
        self.mute_button.configure(text="UNMUTE", command=self.unmute_client)

    def unmute_client(self):
        self.recording_stream.start_stream()
        self.addNotes("Client unmuted.\n")
        self.mute_button.configure(text="MUTE", command=self.mute_client)

    def receive_server_data(self):
        while self.connected:
            try:
                data, addr = self.s.recvfrom(1026)
                message = Protocol(datapacket=data)
                if message.DataType == DataType.ClientData:
                    if self.recording:
                        self.recordingFrames[1].append(message.data)
                    self.playing_stream.write(message.data)
                    self.addNotes("User with id %s is talking (room %s)" % (message.head, message.room) + '\n')
                    

                elif message.DataType == DataType.Handshake or message.DataType == DataType.Terminate:
                    print(message.data.decode("utf-8"))
            except socket.timeout:
                print("\033[2K", end="\r")  # clearing line
            except Exception as err:
                pass

    def connect_to_server(self):
        if self.connected:
            return True

        message = Protocol(dataType=DataType.Handshake, room=self.room, data=self.name.encode(encoding='UTF-8'))
        self.s.sendto(message.out(), self.server)

        data, addr = self.s.recvfrom(1026)
        datapack = Protocol(datapacket=data)

        if addr == self.server and datapack.DataType == DataType.Handshake:
            self.addNotes('Connected to server to room %s successfully!' % datapack.room + '\n')
            print(datapack.data.decode("utf-8"))
            self.connected = True
        return self.connected

    def rms(self, frame):
        count = len(frame) / 2
        format = "%dh" % count
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * (1.0 / 32768.0)
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def record(self):
        current = time.time()
        end = time.time() + 2

        while current <= end:
            data = self.recording_stream.read(512)
            if self.rms(data) >= 10:
                end = time.time() + 2
                try:
                    message = Protocol(dataType=DataType.ClientData, room=self.room, data=data)
                    self.s.sendto(message.out(), self.server)
                except:
                    pass
            current = time.time()

    def listen(self):
        while True:
            try:
                inp = self.recording_stream.read(512)
                rms_val = self.rms(inp)
                if rms_val > 10:
                    self.record()
            except:
                pass

    def send_data_to_server(self):
        while self.connected:
            self.listen()
   
if __name__ == "__main__":
    app = App()
    app.mainloop()