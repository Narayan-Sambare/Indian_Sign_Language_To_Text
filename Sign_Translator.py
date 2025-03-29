

# In[1]:


import cv2
import numpy as np
import os
import mediapipe as mp
print(dir(mp.solutions.holistic))
from tensorflow import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense, InputLayer, SimpleRNN,MaxPooling2D,Flatten,Conv2D,Dropout,BatchNormalization
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
from keras.callbacks import TensorBoard,EarlyStopping
from keras.optimizers import Adam
import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model

# In[2]:


log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)


# In[3]:


mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils


# In[4]:


def mediapipe_detection(image, model):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = model.process(image_rgb)
    return image, results


# In[5]:


def draw_styled_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                              mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
                              mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1))
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
                              mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2))
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                              mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
                              mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2))
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                              mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
                              mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))


# In[6]:



DATA_PATH = os.path.join('MP_Data')
actions = np.array(['Indian', 'Language', 'Welcome', 'Sign', 'deaf', 'Hearing', 'Teacher', 'Thank you', 'strong', 'Good'])
#'Indian', 'Language', 'Welcome', 'Sign', 'Hello', 'Bye', 'He', 'She', 'deaf', 'Hearing', 'Teacher', 'Thank you', 'colours', 'black', 'white', 'red', 'green', 'blue', 'family', 'child', 'day', 'morning', 'afternoon', 'understand', 'we'
#new = np.array([])
#actions = np.append(actions,new)
#no_sequences = 30
#sequence_length = 30
#start_folder = 91


# In[ ]:




# In[7]:


actions


# In[8]:


def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])


# ## Loading and testing the Model

# In[9]:






# Load the model
model = load_model('ISL1.h5')


# In[10]:


#colors = [(245,117,16), (117,245,16), (16,117,245)]
colors = [(228, 26, 28), (55, 126, 184), (77, 175, 74), (152, 78, 163), (255, 127, 0), (255, 255, 51), (166, 86, 40),(245,117,16), (117,245,16), (16,117,245)]
#colors = [(228, 26, 28), (55, 126, 184), (77, 175, 74), (152, 78, 163), (255, 127, 0), (255, 255, 51)]


# In[ ]:




# In[11]:


sequence = []
sentence = []
current_translation=[]
translation=[]
trans=[]
predictions = []
threshold = 0.5


# In[12]:


signs = {'English': ['Indian', 'Language', 'Welcome', 'Sign', 'deaf', 'Hearing', 'Teacher', 'Thank you', 'strong', 'Good'],
         'Malayalam': ["ഇന്ത്യൻ", "ഭാഷ", "സ്വാഗതം", "ആംഗ്യം", "ബധിരൻ", "കേൾക്കുന്നു", "അദ്ധ്യാപകൻ", "നന്ദി", "ശക്തമായ", "നല്ല"],
           'Tamil': ["இந்தியன்", "மொழி", "வரவேற்கிறேன்", "அடையாளம்", "செவிடன்", "கேட்கும்", "ஆசிரியர்", "நன்றி", "வலிமை", "நல்ல"],
           'Hindi': ['भारतीय', 'भाषा', 'स्वागत है', 'निशान', 'बहिरा', 'सुनना', 'शिक्षक', 'धन्यवाद', 'मजबूत', 'अच्छा'],
           'Telugu': ["భారతీయుడు", "భాష", "స్వాగതం", "గుర్తు", "చెవిటి", "వినడం", "ఉపాధ్యాయుడు", "ధన్యవాదాలు", "బలమైన", "మంచి"]}


# In[18]:





# ## Sign Probability Meter

# In[13]:


def prob_viz(res, actions, image, colors):
    assert len(colors) == len(actions), "The number of colors and actions should be the same."
    for num, prob in enumerate(res):
        if num < len(actions):
            cv2.rectangle(image, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), colors[num], -1)
            cv2.putText(image, actions[num], (0, 85 + num * 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    return image


# ## Final UI

# In[24]:


import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time

# Function to execute OpenCV code triggered by GUI
def run_openCV(language):
    global sequence, sentence, predictions, translation, last_sign
    
    # Create translation window
    translation_window = tk.Toplevel(root)
    translation_window.title("Translated Sign Words")
    
    # Calculate window dimensions and position
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = screen_width // 2
    window_height = 100
    window_x = (screen_width - window_width) // 2
    window_y = screen_height - window_height - 50
    
    translation_window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")  # Position at bottom center
    translation_window.resizable(False, False)  # Disable resizing
    translation_window.attributes("-topmost", True)  # Always on top
    translation_window.attributes("-toolwindow", True)  # Remove minimize and maximize buttons
    
    translated_label = tk.Label(translation_window, text="", font=("Arial", 14))
    translated_label.pack(pady=20)
    
    last_sign = None  # Variable to store the last detected sign

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Set width to maximum
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Set height to maximum
    
    with mp_holistic.Holistic(min_detection_confidence=0.4, min_tracking_confidence=0.) as holistic:
        start_time = time.time()
        while cap.isOpened():
            ret, frame = cap.read()
            image, results = mediapipe_detection(frame, holistic)
            draw_styled_landmarks(image, results)
            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]
            res = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]  # Example result
            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                predictions.append(np.argmax(res))
                if np.unique(predictions[-10:])[0] == np.argmax(res):
                    if res[np.argmax(res)] > threshold:
                        current_time = time.time()
                        # Add the label to the sentence only after 2 seconds
                        if current_time - start_time > 4:
                            if len(sentence) > 0:
                                max_index = np.argmax(res) % len(signs[language])  # Ensure valid index
                                if signs[language][max_index] != last_sign:
                                    sentence.append(actions[max_index])
                                    translation.append(signs[language][max_index])
                                    last_sign = signs[language][max_index]
                            else:
                                sentence.append(actions[np.argmax(res)])
                                translation.append(signs[language][np.argmax(res)])
                                last_sign = signs[language][np.argmax(res)]
                            start_time = current_time  # Reset the start time
                            # Ensure only the last 5 translated words are displayed
                            if len(translation) > 5:
                                translation = translation[-5:]
                translated_label.config(text=' '.join(translation))
                translated_label.update_idletasks()  # Update the label text
                image = prob_viz(res, actions, image, colors)
            cv2.rectangle(image, (0, 0), (1920, 40), (245, 117, 16), -1)  # Change resolution accordingly
            cv2.putText(image, ' '.join(sentence[-5:]), (3, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow('OpenCV Feed', image)

            key = cv2.waitKey(10)
            if key & 0xFF == ord('q'):  # Exit when 'q' is pressed
                break
        
        sentence.clear()
        translation.clear()

        cap.release()
        cv2.destroyAllWindows()
        root.deiconify()  # Show the initial Tkinter UI after closing OpenCV window
        translation_window.destroy()  # Close the translated window

def on_button_click():
    language = language_var.get()
    messagebox.showinfo("Info", f"{language} Sign Language Translation Started.")
    root.withdraw()  # Hide the initial Tkinter UI
    run_openCV(language)  # You must define this function elsewhere

# Create Tkinter window
root = tk.Tk()
root.title("SignSense")
root.configure(bg="white")

# Set window dimensions to match OpenCV window
window_width = 800
window_height = 600
root.geometry(f"{window_width}x{window_height}+{root.winfo_screenwidth()//2 - window_width//2}+{root.winfo_screenheight()//2 - window_height//2}")

# Change background color
root.configure(bg="#2C2C2B")

# Green rectangular component containing the heading "SignSense"
header_frame = tk.Frame(root, bg="#2C2C2B", width=window_width, height=50)
header_frame.pack_propagate(False)  # Prevent frame from shrinking to fit its contents
header_frame.pack(side="top", fill="x")
header_text = tk.Text(header_frame, height=1, bg="#2C2C2B", bd=0, highlightthickness=0, font=("Montserrat Classic", 30, "bold"), cursor="arrow")
header_text.tag_configure("Sign", foreground="#0057CB")
header_text.tag_configure("Translator", foreground="#0CC0DF")  # Changed "Sense" to "Translator"
header_text.insert("1.0", "Sign", "Sign")
header_text.insert("end", " Translator", "Translator")  # Changed "Sense" to "Translator"
header_text.configure(state="disabled", relief="flat")

# Center the text widget content and remove the ability to highlight the text
header_text.tag_configure("center", justify="center")
header_text.tag_add("center", "1.0", "end")

header_text.pack(expand=True, fill="both")

# Main container frame to center the below components
center_frame = tk.Frame(root, bg="#2C2C2B")
center_frame.pack(expand=True)

# Language selection label
language_label = tk.Label(center_frame, text="Choose Your Language to Translate", font=("poppins", 18, "bold"), fg="white", bg="#2C2C2B")
language_label.pack(pady=(10, 10))  # Adjust vertical spacing

# Language selection menu
language_var = tk.StringVar(root)
language_var.set("English")  # Default language

# Function to style the dropdown menu
def customize_dropdown(dropdown, font, bg_color, fg_color):
    dropdown.config(font=font, bg=bg_color, fg=fg_color)
    # Change the dropdown arrow symbol to something more modern if desired
    dropdown["menu"].config(bg=bg_color, fg=fg_color)

dropdown_font = ("poppins", 14)
dropdown_bg = "#EFEEE7"
dropdown_fg = "#000000"
dropdown_menu_bg = "#2c3e50"

language_menu = tk.OptionMenu(center_frame, language_var, "English", "Malayalam", "Tamil", "Hindi", "Telugu")
customize_dropdown(language_menu, dropdown_font, dropdown_bg, dropdown_fg)

language_menu.pack(pady=10)

# Create and style the button using Canvas
canvas_width = 220
canvas_height = 60  # Adjusted for a more standard button height
button_text = "Start Translation"

# Canvas for the button
canvas = tk.Canvas(center_frame, bg="#2C2C2B", highlightthickness=0, width=canvas_width, height=canvas_height)
canvas.pack(pady=(20, 20))

# Function to draw a rounded rectangle on the canvas
def create_rounded_rectangle(x1, y1, x2, y2, radius, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Draw the button and add text
btn_shape = create_rounded_rectangle(10, 10, canvas_width-10, canvas_height-10, 20, fill="#2980b9")
btn_text = canvas.create_text(canvas_width / 2, canvas_height / 2, text=button_text, fill="white", font=("Arial", 16))

# Function to handle button press events
def on_button_press(event):
    canvas.itemconfig(btn_shape, fill="#3498db")  # Lighter shade to simulate button press

def on_button_release(event):
    canvas.itemconfig(btn_shape, fill="#2980b9")  # Original color
    on_button_click()  # Function to handle button click

# Bind the button events
canvas.tag_bind(btn_shape, "<ButtonPress-1>", on_button_press)
canvas.tag_bind(btn_shape, "<ButtonRelease-1>", on_button_release)
canvas.tag_bind(btn_text, "<ButtonPress-1>", on_button_press)
canvas.tag_bind(btn_text, "<ButtonRelease-1>", on_button_release)

root.mainloop()


