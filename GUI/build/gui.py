from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label
from PIL import Image, ImageTk
import paho.mqtt.client as mqtt


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("900x600")
window.iconbitmap(relative_to_assets("pet.ico"))
window.title("FeedMyPet")

def on_connect(client, userdata, flags, rc):
    global loop_flag
    print("\n Connected with result code " + str(rc))
    print("\n connected with client " + str(client))
    print("\n connected with userdata " + str(userdata))
    print("\n connected with flags " + str(flags))
    loop_flag=0

try:
    counter=0
    client = mqtt.Client("GUI")
    client.on_connect = on_connect 
    client.connect("test.mosquitto.org", 1883, 60)

    client.loop_start()
except Exception as e:
    print("exception ", e)


canvas = Canvas(
    window,
    bg = "#E2DD56",
    height = 600,
    width = 900,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

def feed_pet(event):
    client.publish("IoT22_FeedMyPet", "Feed")

def enter_pressed(event):
    try:
        number = int(entry_1.get())
        if(number >= 0 and number <= 5):
            client.publish("IoT22_FeedMyPet", str(number))
    except ValueError:
        print("Insert an integer!")
    entry_1.delete(0, 'end')

    try:
        number = int(entry_2.get())
        if(number >= 10 and number <= 60):
            client.publish("IoT22_FeedMyPet", str(number))
    except ValueError:
        print("Insert an integer!")
    entry_2.delete(0, 'end')


window.bind('<Return>', enter_pressed)


canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    450.0,
    300.0,
    image=image_image_1
)

def button_func(event):
    print("ciao")

button_image_1 = ImageTk.PhotoImage(Image.open(relative_to_assets("button_1.png")))
button_1 = canvas.create_image(390, 550, image=button_image_1)
canvas.tag_bind(button_1, "<Button-1>", feed_pet)

entry_1 = Entry(
    bd=0,
    bg="#808080",
    highlightthickness=0
)
entry_1.place(
    x=102.0,
    y=257.0,
    width=63,
    height=51
)

entry_2 = Entry(
    bd=0,
    bg="#808080",
    highlightthickness=0
)
entry_2.place(
    x=102.0,
    y=365.0,
    width=63,
    height=51
)


window.resizable(False, False)
window.mainloop()