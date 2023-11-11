import tkinter as tk
import mysql.connector
from tkinter import Entry, Label, Button, PhotoImage, messagebox
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

# Function to check login credentials
conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="20606379",
    database="sys"
)
cursor = conn.cursor()

# Function to check login credentials
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check the credentials against the database
    cursor.execute('SELECT * FROM new_table WHERE username=%s AND password=%s', (username, password))
    user = cursor.fetchone()

    if user:
        login_label.config(text="Login successful!", fg="green")
        show_crop_prediction()
    else:
        login_label.config(text="Login failed. Please try again.", fg="red")
# Function to perform crop prediction and display the result
def predict_crop():
    try:
        N = float(nitrogen_entry.get())
        P = float(phosphorus_entry.get())
        K = float(potassium_entry.get())
        temperature = float(temp_entry.get())
        humidity = float(humidity_entry.get())
        ph = float(ph_entry.get())
        rainfall = float(rainfall_entry.get())

        # Perform the prediction
        y_ans = cls.predict([[N, P, K, temperature, humidity, ph, rainfall]])
        predicted_crop = le.inverse_transform(y_ans)[0]

        result_label.config(text="The suitable crop is: " + predicted_crop)
        show_crops()  # Show crop images after prediction

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for all fields.")

# Function to display images of crops
def show_crops():
    login_frame.pack_forget()  # Hide the login frame

    # Create a frame for crop images and centered colors
    crop_frame = tk.Frame(root, bg="white")
    crop_frame.pack(expand=True, fill="both")

    # Load and display crop images
    wheat_image = Image.open("path_to_directory/wheat_image.png")
    rice_image = Image.open("path_to_directory/rice_image.png")

    wheat_photo = ImageTk.PhotoImage(wheat_image)
    rice_photo = ImageTk.PhotoImage(rice_image)

    wheat_label = tk.Label(crop_frame, image=wheat_photo)
    rice_label = tk.Label(crop_frame, image=rice_photo)

    wheat_label.image = wheat_photo  # Keep a reference to prevent image from being garbage collected
    rice_label.image = rice_photo

    wheat_label.pack(side="left", padx=20, pady=20)
    rice_label.pack(side="right", padx=20, pady=20)

    # Add centered colored labels
    color_label1 = tk.Label(crop_frame, text="Wheat", font=("Arial", 20), bg="green", fg="white")
    color_label2 = tk.Label(crop_frame, text="Rice", font=("Arial", 20), bg="blue", fg="white")

    color_label1.place(relx=0.5, rely=0.5, anchor="center")
    color_label2.place(relx=0.5, rely=0.8, anchor="center")

# Load the dataset and train the model
data = pd.read_csv('Crop_recommendation.csv')
x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

le = LabelEncoder()
y = le.fit_transform(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

cls = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
cls.fit(x_train, y_train)

# Create the main Tkinter window
root = tk.Tk()
root.title("Crop Prediction")

# Create a frame for login
login_frame = tk.Frame(root)
login_frame.pack(expand=True, fill="both")

# Username and password entry fields
username_label = Label(login_frame, text="Username:")
username_label.pack(pady=10)
username_entry = Entry(login_frame)
username_entry.pack()

password_label = Label(login_frame, text="Password:")
password_label.pack(pady=10)
password_entry = Entry(login_frame, show="*")
password_entry.pack()

# Login button
login_button = Button(login_frame, text="Login", command=login)
login_button.pack(pady=20)

# Label to display login status
login_label = Label(login_frame, text="", fg="black")
login_label.pack()

# Function to create and display input fields for crop prediction
def show_crop_prediction():
    login_frame.pack_forget()  # Hide the login frame

    prediction_frame = tk.Frame(root, bg="white")
    prediction_frame.pack(expand=True, fill="both")

    Label(prediction_frame, text="Enter Nitrogen Content:").grid(row=0, column=0, pady=5)
    Label(prediction_frame, text="Enter Phosphorus Content:").grid(row=1, column=0, pady=5)
    Label(prediction_frame, text="Enter Potassium Content:").grid(row=2, column=0, pady=5)
    Label(prediction_frame, text="Enter Temperature:").grid(row=3, column=0, pady=5)
    Label(prediction_frame, text="Enter Humidity:").grid(row=4, column=0, pady=5)
    Label(prediction_frame, text="Enter pH Value:").grid(row=5, column=0, pady=5)
    Label(prediction_frame, text="Enter Rainfall (cm):").grid(row=6, column=0, pady=5)

    global nitrogen_entry, phosphorus_entry, potassium_entry, temp_entry, humidity_entry, ph_entry, rainfall_entry
    nitrogen_entry = Entry(prediction_frame)
    phosphorus_entry = Entry(prediction_frame)
    potassium_entry = Entry(prediction_frame)
    temp_entry = Entry(prediction_frame)
    humidity_entry = Entry(prediction_frame)
    ph_entry = Entry(prediction_frame)
    rainfall_entry = Entry(prediction_frame)

    nitrogen_entry.grid(row=0, column=1, padx=10, pady=5)
    phosphorus_entry.grid(row=1, column=1, padx=10, pady=5)
    potassium_entry.grid(row=2, column=1, padx=10, pady=5)
    temp_entry.grid(row=3, column=1, padx=10, pady=5)
    humidity_entry.grid(row=4, column=1, padx=10, pady=5)
    ph_entry.grid(row=5, column=1, padx=10, pady=5)
    rainfall_entry.grid(row=6, column=1, padx=10, pady=5)

    predict_button = Button(prediction_frame, text="Predict Crop", command=predict_crop)
    predict_button.grid(row=7, columnspan=2, pady=10)

    global result_label
    result_label = Label(prediction_frame, text="", font=("Arial", 14))
    result_label.grid(row=8, columnspan=2, pady=10)

# Start the GUI main loop
root.mainloop()
