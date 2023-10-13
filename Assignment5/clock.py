import tkinter as tk
import time
import math
from datetime import datetime, timedelta
from PIL import Image, ImageGrab
import io
import os
import pyautogui
import tkcap


current_time = datetime(1,1,1)
time_delta = timedelta(minutes=1)

ghostscript_path = "C:\Program Files\gs\gs10.02.0\bin"

i = 1
# Function to update the clock time
def update_clock():
    global current_time, time_delta, i
    #print(current_time.tm_min)
    seconds = current_time.second
    minutes = current_time.minute
    hours = current_time.hour % 12  # Convert to 12-hour format

    # Calculate angles for clock hands
    second_angle = 360 - (seconds * 6)  # 360 degrees in 60 seconds
    minute_angle = 360 - ((minutes + seconds/60) * 6)  # 360 degrees in 60 minutes
    hour_angle = 360 - ((hours + minutes/60) * 30)  # 360 degrees in 12 hours

    # Update clock hands
    canvas.delete("all")
    draw_clock_face()
    #draw_clock_hand(200, second_angle, "red")
    draw_clock_hand(150, minute_angle, "blue")
    draw_clock_hand(100, hour_angle, "black")

    
    save_clock_image(str(i).zfill(3))
    i += 1
    
    hours_txt = "12" if hours == 0 else str(hours)
    minutes_txt = str(minutes) if minutes > 9 else "0"+str(minutes)
    f = open("labels.txt", "a")
    f.write(hours_txt + ":" + minutes_txt + "\n")
    f.close()
    
    #current_time.tm_min += 1
    # Call update_clock function after 1000ms (1 second)
    current_time = current_time + time_delta
    #root.after(1000, update_clock)

# Function to draw the clock face
def draw_clock_face():
    center_x = 250
    center_y = 250
    canvas.create_oval(center_x - 220, center_y - 220, center_x + 220, center_y + 220, width=2, outline="black")
    for i in range(1, 13):
        angle = math.radians(30 * i)
        x1 = center_x + 180 * math.sin(angle)
        y1 = center_y - 180 * math.cos(angle)
        x2 = center_x + 200 * math.sin(angle)
        y2 = center_y - 200 * math.cos(angle)
        canvas.create_line(x1, y1, x2, y2, width=3, fill="black")
        
        # Add text labels for the numbers
        x_text = center_x + 160 * math.sin(angle)
        y_text = center_y - 160 * math.cos(angle)
        canvas.create_text(x_text, y_text, text=str(i), fill="black", font=("Arial", 20))

    canvas.create_oval(center_x - 10, center_y - 10, center_x + 10, center_y + 10, fill="black")

# Function to draw clock hands
def draw_clock_hand(length, angle, color):
    center_x = 250
    center_y = 250
    angle = math.radians(angle)
    x = center_x + length * math.sin(-angle)
    y = center_y - length * math.cos(-angle)
    canvas.create_line(center_x, center_y, x, y, width=5, fill=color)
    
# Function to capture and save the clock image
def save_clock_image(name):
    global canvas
    #postscript_file = canvas.postscript(colormode="color")
    #clock_image = Image.open(io.BytesIO(postscript_file.encode("utf-8")))
    #clock_image.save("./images/" + name + ".png", format="png", dpi=(300, 300), gs=ghostscript_path)
    clock_image = tkcap.CAP(root)
    clock_image.capture("./images/" + name + ".png", True, False)

# Create the main window
root = tk.Tk()
root.title("Analog Clock")

# Create a canvas to draw the clock
canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack()
draw_clock_face()

clock_image = tkcap.CAP(root)
clock_image.capture("./images/0.png")

time.sleep(2)

# Call update_clock to start the clock
for j in range(1, 721):
    update_clock()
    
    

# Start the Tkinter main loop
root.mainloop()
