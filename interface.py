#!/usr/bin/python3
import tkinter
import customtkinter
from CTkListbox import *
import os
import time
import threading
import function
import pyaudio

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.wav_file_name = ""
        self.paused = True
        self.playing = False
        self.audio_length = 0
        self.current_sec = 0
        self.after_id = None
        self.audio_timer = 0

        # configure window
        self.title("Sound Recorder")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=6)
        self.grid_rowconfigure(0, weight=1)

        # create scrollable frame
        self.listbox = CTkListbox(master=self, 
                                  command=self.show_value, 
                                  justify="center", 
                                  highlight_color="#4382C4",
                                  fg_color="#90C6FF", 
                                  label_text="All Recordings", 
                                  label_fg_color="#90C6FF",
                                  label_font=(None,30),
                                  font=(None,30))
        self.listbox.grid(row=0, column=0, rowspan=7, padx=0, pady=0, sticky="nsew")
        self.listbox.grid_rowconfigure(4, weight=1)
        #the loop the files from the direct directory path
        self.refresh_list()

        #creaet main view
        self.main_view = customtkinter.CTkFrame(self, fg_color="red")
        self.main_view.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.main_view.grid_columnconfigure(0, weight=1)
        self.main_view.grid_rowconfigure(1, weight=1)
        #
        self.edit_button = customtkinter.CTkButton(self.main_view, 
                                                     width=100, 
                                                     text="EDIT", 
                                                     font=("Arial", 30, "bold"), 
                                                     command=self.play_audio)
        self.edit_button.grid(row=0, column=3, padx=10, pady=(5, 5), sticky="nsew")
        #
        self.textbox = customtkinter.CTkTextbox(self.main_view)
        self.textbox.grid(row=1, column=0, columnspan=4, padx=0, pady=0, sticky="nsew")
        

        #create control panel
        self.control_panel_bar = customtkinter.CTkFrame(self)
        self.control_panel_bar.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")
        self.control_panel_bar.grid_columnconfigure((0, 2, 5, 7), weight=1)
        #create recording button
        self.record_button = customtkinter.CTkButton(self.control_panel_bar, 
                                                     width=100, 
                                                     text="🎙", 
                                                     font=("Arial", 30, "bold"), 
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
                                                     command=self.play_audio)
        self.play_button.grid(row=0, column=3, rowspan=2, padx=10, pady=(5, 5), sticky="nsew")
        #create pause button
        self.pause_button = customtkinter.CTkButton(self.control_panel_bar, 
                                                     width=100, 
                                                     text="⏸", 
                                                     font=("Arial", 30, "bold"), 
                                                     command=self.pause_audio)
        self.pause_button.grid(row=0, column=4, rowspan=2, padx=10, pady=(5, 5), sticky="nsew")
        #create speed selection button
        self.speed_label = customtkinter.CTkLabel(self.control_panel_bar, 
                                                  text="Speed Mode:", 
                                                  anchor="w")
        self.speed_label.grid(row=0, column=6, padx=20, pady=0)
        self.speed_optionemenu = customtkinter.CTkOptionMenu(self.control_panel_bar, 
                                                             values=["2.0x", "1.0x", "0.5x"],
                                                             command=self.change_speed)
        self.speed_optionemenu.grid(row=1, column=6, padx=0, pady=(0, 5), sticky="nsew")
        self.speed_optionemenu.set("1.0x")
        
    def refresh_list(self):
        for file in os.listdir("."):
            file_name = f"{file:70s}"
            file_type = os.path.splitext(file)[1]
            if file_type == ".wav":
            
                file_time = time.strftime("\n\n%Y-%m-%d (%H:%M:%S)", time.strptime(time.ctime(os.path.getmtime(file))))
                self.listbox.insert(file, file_name + file_time)

    #take the data of the .wav file here after you click the left explorer bar
    def show_value(self, selected_option):
        self.wav_file_name = selected_option.split()
        print(self.wav_file_name[0])
        self.file_data = function.open_file(self.wav_file_name[0])
        length = self.file_data["length"]
        hour = length // 3600
        min = (length - hour * 60) // 60
        sec = length - hour * 3600 - min * 60
        self.timer_label.configure(text=f"{int(hour):02d}:{int(min):02d}:{int(sec):02d}")

    def record_click_listener(self):
        if self.recording:
            self.recording = False
            self.record_button.configure(text_color = "white")
            
        else:
            self.recording = True
            self.record_button.configure(text_color = "red")
            threading.Thread(target=self.record_action).start()

    #implement the record function
    def record_action(self):
        p = pyaudio.PyAudio()
        stream = p.open(format = pyaudio.paInt16, channels = 1, rate = 44100, input = True, input_device_index = 0, frames_per_buffer = 1024)

        frames = []
        start = time.time()
        
        while self.recording:
            #configure timer
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

        exist = True
        i = 1
        while exist:
            if os.path.exists(f"Output{i}.wav"):
                i += 1
            else:
                exist = False
        function.streamplay(frames)
        function.convert_audio_to_wav(frames, f"Output{i}")
        self.refresh_list()

    def start_playing(self):  
        p = pyaudio.PyAudio()
        chunk = 1024

        # self.file_data = function.open_file(self.wav_file_name[0])
        print("bytesperframe", self.file_data["bytesperframe"])
        print("framerate", self.file_data["framerate"])
        print("nchannel", self.file_data["nchannel"])
        print("nframe", self.file_data["nframe"])
        print("length", self.file_data["length"])
        stream = p.open(format = p.get_format_from_width(self.file_data["bytesperframe"]), channels = self.file_data["nchannel"], rate = self.file_data["framerate"], output = True)
        cur_bytes = 0
        data = self.file_data["audio_data"][cur_bytes:cur_bytes+chunk*2]
        cur_bytes += chunk*2
        while data != b"" and self.playing:
            if not self.paused:
                stream.write(data)
                data = data = self.file_data["audio_data"][cur_bytes:cur_bytes+chunk*2]
                cur_bytes += chunk*2
                self.current_sec = cur_bytes/2/self.file_data["framerate"]
                #print time label
                hour = self.current_sec // 3600
                min = (self.current_sec - hour * 60) // 60
                sec = self.current_sec - hour * 3600 - min * 60
                self.timer_label.configure(text=f"{int(hour):02d}:{int(min):02d}:{int(sec):02d}")

        self.playing=False
        stream.close()   
        p.terminate()

    #implement the play function here
    def play_audio(self):
        if not self.playing:
            self.playing = True
            print(self.wav_file_name[0])
            threading.Thread(target=self.start_playing, daemon=True).start()
        
        if self.after_id is None:
            print()

        self.paused = False

    #implement the play function here
    def pause_audio(self):
        self.paused = True
        
        if self.after_id:
            self.after_id = None

    #implement the speed control function here
    def change_speed(self, speed_mode: str):
        print(speed_mode)
        function.streamplay(function.speed_func(self.wav_file_name[0], float(speed_mode[0:3])))


if __name__ == "__main__":
    app = App()
    app.mainloop()