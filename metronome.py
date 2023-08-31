import time
import random
import pygame
import tkinter as tk
from tkinter import ttk
import threading

def metronome():
    pygame.mixer.init()

    non_accent_sound = pygame.mixer.Sound("tock.wav")
    audio_files = ["1.wav", "2.wav", "3.wav", "4.wav"]

    loop_count = 0
    tacts = 0
    while not stop_event.is_set():
        tempo = int(tempo_scale.get())
        duration = 60 / tempo
        random_interval = int(random_interval_scale.get())

        if loop_count % random_interval == 0:
            random_file = random.choice(audio_files)
            sound = pygame.mixer.Sound(random_file)
            print("Random file selected:", random_file)

            # Adjust the volume of the selected file
            if random_file in ["1.wav", "2.wav", "3.wav", "4.wav"]:
                sound.set_volume(2)  # Increase the volume by 50%


            sound.play()

        if accent_toggle.get() == 1:  # Check the value of the accent toggle button
                accent_sound = pygame.mixer.Sound("tick.wav")
        else:
                accent_sound = pygame.mixer.Sound("tock.wav")        


        accent_sound.play()
        print("Accent")
        time.sleep(duration)

        for _ in range(3):
            non_accent_sound.play()
            print("Non-accent")
            time.sleep(duration)

        loop_count += 1
        if loop_count % (random_interval * 4) == 0:
            tacts += 1
            metronome_counter.set(tacts)
       

# Create the GUI window
window = tk.Tk()
window.title("Metronome")

# Tempo slider
tempo_label = ttk.Label(window, text="Tempo (BPM):")
tempo_label.pack()
tempo_scale = ttk.Scale(window, from_=40, to=130, orient="horizontal")
tempo_scale.set(120)
tempo_scale.pack()

# Random interval slider
random_interval_label = ttk.Label(window, text="Random Interval (beats):")
random_interval_label.pack()
random_interval_scale = ttk.Scale(window, from_=1, to=8, orient="horizontal")
random_interval_scale.set(4)
random_interval_scale.pack()

# Accent toggle button
accent_toggle = tk.IntVar()
accent_toggle.set(1)  # Default: accent sound enabled
accent_button = ttk.Checkbutton(window, text="Accent", variable=accent_toggle)
accent_button.pack()

# BPM label
bpm_label = ttk.Label(window, text="BPM: {}".format(int(tempo_scale.get())))
bpm_label.pack()

# Tacts label
tacts_label = ttk.Label(window, text="Tacts: {}".format(int(random_interval_scale.get())))
tacts_label.pack()

def start_metronome():
    global stop_event
    stop_event = threading.Event()
    thread = threading.Thread(target=metronome)
    thread.start()

def stop_metronome():
    stop_event.set()
    pygame.mixer.stop()

def update_bpm_tacts():
    bpm_label.configure(text="BPM: {}".format(int(tempo_scale.get())))
    tacts_label.configure(text="Tacts: {}".format(int(random_interval_scale.get())))
    window.after(100, update_bpm_tacts)

# Metronome counter
metronome_counter = tk.IntVar()
metronome_counter.set(0)

# Start button
start_button = ttk.Button(window, text="Start", command=start_metronome)
start_button.pack()

# Stop button
stop_button = ttk.Button(window, text="Stop", command=stop_metronome)
stop_button.pack()

# Start updating BPM and tacts labels
update_bpm_tacts()

# Run the GUI window
window.mainloop()
