#!/usr/bin/python3
import tkinter
import customtkinter
from CTkListbox import *
import os
import time
import threading

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

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
        for wav_file in os.listdir("."):
            file_name = f"{wav_file:70s}"
            file_time = time.strftime("\n\n%Y-%m-%d (%H:%M:%S)", time.strptime(time.ctime(os.path.getmtime(wav_file))))
            self.listbox.insert(wav_file, file_name + file_time)


        #create control panel
        self.control_panel_bar = customtkinter.CTkFrame(self)
        self.control_panel_bar.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")
        self.control_panel_bar.grid_columnconfigure((0, 2, 4, 6), weight=1)
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
                                                     text="⏯", 
                                                     font=("Arial", 30, "bold"), 
                                                     command=self.play_pause)
        self.play_button.grid(row=0, column=3, rowspan=2, padx=0, pady=(5, 5), sticky="nsew")
        #create speed selection button
        self.speed_label = customtkinter.CTkLabel(self.control_panel_bar, 
                                                  text="Speed Mode:", 
                                                  anchor="w")
        self.speed_label.grid(row=0, column=5, padx=20, pady=0)
        self.speed_optionemenu = customtkinter.CTkOptionMenu(self.control_panel_bar, 
                                                             values=["2.0x", "1.0x", "0.5x"],
                                                             command=self.change_speed)
        self.speed_optionemenu.grid(row=1, column=5, padx=0, pady=(0, 5), sticky="nsew")
        self.speed_optionemenu.set("1.0x")
        


    #take the data of the .wav file here after you click the left explorer bar
    def show_value(self, selected_option):
        print(selected_option)

    def record_click_listener(self):
        if self.recording:
            self.recording = False
            self.record_button.configure(text_color = "white")
        else:
            self.recording = True
            self.record_button.configure(text_color = "red")
            threading.Thread(target=self.record_action).start()

    #implement the record function here
    def record_action(self):
        start = time.time()

        #configure timer
        while self.recording:
            passed = time.time() - start
            sec = passed % 60
            min = passed //60
            hour = min // 60
            self.timer_label.configure(text=f"{int(hour):02d}:{int(min):02d}:{int(sec):02d}")

    #implement the play function here
    def play_pause(self):
        print()

    #implement the speed control function here
    def change_speed(self, speed_mode: str):
        print(speed_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()