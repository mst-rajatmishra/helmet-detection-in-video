import cv2
import tkinter as tk
from PIL import ImageTk, Image
import os

cascade_src = 'bike.xml'
video_src = 'vidd.mp4'

cap = cv2.VideoCapture(video_src)
fgbg = cv2.createBackgroundSubtractorMOG2()
car_cascade = cv2.CascadeClassifier(cascade_src)

# Set up GUI
window = tk.Tk()  # Makes main window
window.wm_title("Digital Microscope")
window.config(background="#ADD8E6")

# Title Label
titleLabel = tk.Label(window, text="Digital Microscope", font=("Helvetica", 16), background="#ADD8E6")
titleLabel.grid(row=0, column=0, padx=10, pady=2)

# Graphics window
imageFrame = tk.Frame(window, width=600, height=500, background="#ADD8E6")
imageFrame.grid(row=1, column=0, padx=10, pady=2)

# Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)

# Slider window (slider controls stage position)
sliderFrame = tk.Frame(window, width=600, height=100, background="#ADD8E6")
sliderFrame.grid(row=2, column=0, padx=10, pady=2)

# Function to save a frame
def save_frame():
    _, frame = cap.read()
    if not os.path.exists('captures'):
        os.makedirs('captures')
    cv2.imwrite(f'captures/frame_{int(cap.get(cv2.CAP_PROP_POS_FRAMES))}.png', frame)

# Add Save Frame Button
saveButton = tk.Button(sliderFrame, text="Save Frame", command=save_frame, background="#FFFFFF")
saveButton.grid(row=0, column=0, padx=5, pady=5)

# Function to stop video capture
def stop_capture():
    cap.release()
    window.destroy()

# Add Stop Button
stopButton = tk.Button(sliderFrame, text="Stop", command=stop_capture, background="#FFFFFF")
stopButton.grid(row=0, column=1, padx=5, pady=5)

def show_frame():
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cars = car_cascade.detectMultiScale(gray, 1.59, 1)

    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 215), 2)

    color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(color)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

show_frame()  # Display 2

# Handle window close event
def on_closing():
    if cap.isOpened():
        cap.release()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()  # Starts GUI

cv2.destroyAllWindows()
