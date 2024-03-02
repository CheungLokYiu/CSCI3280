#!/usr/bin/python3
import tkinter
import customtkinter
from CTkListbox import *
import os, sys
import time
import threading
import function
import pyaudio
from PIL import Image
import visualize

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
        self.last_file = ''
        self.selected_file_index = 0
        self.edited_frame = []
        self.edit_start_time = 0
        self.edit_end_time = 0
        self.edit_total_second = 0
        self.get_list_detail = True

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
                                  width=350,
                                  justify="center", 
                                  highlight_color="#AD88C6",
                                  hover_color="#AD88C6",
                                  fg_color="#7469B6", 
                                  label_text="All Recordings", 
                                  label_fg_color="#7469B6",
                                  label_font=(None,30))
        self.listbox.grid(row=0, column=0, rowspan=7, padx=0, pady=0, sticky="nsew")
        self.listbox.grid_rowconfigure(4, weight=1)
        #the loop the files from the direct directory path
        self.refresh_list()

        #creaet main view
        self.main_view = customtkinter.CTkFrame(self, fg_color="#F9F5F6")
        self.main_view.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.main_view.grid_columnconfigure(0, weight=1)
        self.main_view.grid_rowconfigure(2, weight=1)
        #create edit button
        self.edit_button = customtkinter.CTkButton(self.main_view, 
                                                     width=100, 
                                                     text="EDIT", 
                                                     font=("Arial", 30, "bold"), 
                                                     fg_color="#7469B6",
                                                     hover_color="#AD88C6",
                                                     command=self.open_edit_dialog)
        self.edit_button.grid(row=0, column=1, padx=10, pady=(5, 5), sticky="nsew")
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
        
    def refresh_list(self):
        for file in os.listdir("."):
            file_name = f"{file:70s}"
            file_type = os.path.splitext(file)[1]
            if file_type == ".wav":
            
                file_time = time.strftime("\n\n%Y-%m-%d (%H:%M:%S)", time.strptime(time.ctime(os.path.getmtime(file))))
                self.listbox.insert(file, file_name + file_time)
            self.playing = False

    #take the data of the .wav file here after you click the left explorer bar
    def show_value(self, selected_option):
        if self.get_list_detail:
            self.playing = False
            self.speed_optionemenu.set('1.0x')
            self.selected_file_index = self.listbox.curselection()
            if self.last_file != '':
                function.savefile(self.last_file,function.speed_func(self.last_file, float(1)*function.RATE)) 
            print('last_file', self.last_file)
            self.wav_file_name = selected_option.split()

            self.file_name_label.configure(text=self.wav_file_name[0])

            
            self.last_file = self.wav_file_name[0]
            self.current_sec = 0
            self.show_audio_length()

            # image_name = self.wav_file_name[0].replace(".wav", "")
            self.show_image()
            self.show_audio_text()

    def init_main_view(self):
        self.audio_text_label.configure(text="")
        self.timer_label.configure(text="00:00:00")
        self.file_name_label.configure(text="")
        self.audio_image.configure(dark_image=Image.open("out.png"))
        self.image_button.configure(image=self.audio_image)


    def show_image(self):
        visualize.plotSignalWave(self.wav_file_name[0], "photo_image.png")
        self.audio_image.configure(dark_image=Image.open("photo_image.png"))
        self.image_button.configure(image=self.audio_image)
    
    def show_audio_text(self):
        audio_text = function.wav_to_text(self.wav_file_name[0])
        self.audio_text_label.configure(text=audio_text)

    def show_audio_length(self):
        self.file_data = function.open_file(self.wav_file_name[0])
        length = self.file_data["length"]
        hour = length // 3600
        min = (length - hour * 60) // 60
        sec = length - hour * 3600 - min * 60
        self.timer_label.configure(text=f"{int(hour):02d}:{int(min):02d}:{int(sec):02d}")

    def record_click_listener(self):
        self.init_main_view()
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
        cur_bytes = int(self.current_sec * 2 * function.RATE) - int((self.current_sec * 2 * function.RATE)%2)
        # (int(start*bytesperframe*framerate)-int(start*bytesperframe*framerate)%2)
        print(cur_bytes, self.current_sec)
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

    #implement the play function here
    def play_audio(self):
        if not self.playing:
            self.playing = True
            print(self.wav_file_name[0])
            threading.Thread(target=self.start_playing, daemon=True).start()
        
        if self.after_id is None:
            print()

        self.paused = False

    #implement the pause function here
    def pause_audio(self):
        self.paused = True
        
        if self.after_id:
            self.after_id = None

    #implement the speed control function here
    def change_speed(self, speed_mode: str):
        print(speed_mode)
        self.speed_optionemenu.set(speed_mode)
        data = function.speed_func(self.wav_file_name[0], float(speed_mode[0:3])*function.RATE)
        function.savefile(self.wav_file_name[0], data)
        self.refresh_list()

        self.get_list_detail = False
        self.listbox.activate(self.selected_file_index)
        self.get_list_detail = True

        self.file_data = data

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
        print(start_time, end_time)

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

        threading.Thread(target=self.edit_record).start()

    #start edit recording 
    def edit_record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format = pyaudio.paInt16, channels = 1, rate = 44100, input = True, input_device_index = 0, frames_per_buffer = 1024)

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
        print(self.wav_file_name[0], type(self.wav_file_name[0]))
        filename = self.wav_file_name[0].replace('.wav', '')
        function.convert_audio_to_wav(replace_data, filename)
        self.refresh_list()
        self.record_button.configure(text_color = "white")
        self.init_main_view()
        return
        


if __name__ == "__main__":
    app = App()
    app.mainloop()