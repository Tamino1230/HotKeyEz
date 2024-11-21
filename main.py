import keyboard as k
import tkinter as tk
from tkinter import messagebox

by = "tamino1230"

def newHotkey(hotkey, text, vari, supr=None):
    key = hotkey

    def vari():
        k.write(text)

    if supr is None:
        k.add_hotkey(key, vari)
    elif supr is True:
        k.add_hotkey(key, vari, suppress=True)
    elif supr is False:
        k.add_hotkey(key, vari)
    else:
        k.add_hotkey(key, vari)

# hotkeys getting saved
FILE_NAME = "hotkeys.py"

# Funktion zur Speicherung der Hotkeys in der Datei
def save_hotkeys_to_file(hotkeys):
    with open(FILE_NAME, "w") as file:
        file.write("# Automatic generated Hotkeys\nimport main as m\n")
        for hotkey in hotkeys:
            supress_str = f", {hotkey['supress']}" if hotkey["supress"] is not None else ""
            file.write(f"m.newHotkey('{hotkey['hotkey']}', '{hotkey['text']}', '{hotkey['vari']}'{supress_str})\n")

# initialasion of the keys
def load_hotkeys_from_file():
    hotkeys = []
    try:
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("m.newHotkey"):
                    # Parsen der Argumente aus der Zeile
                    args = line.strip().replace("m.newHotkey(", "").replace(")", "").split(", ")
                    hotkey = args[0].strip("'")
                    text = args[1].strip("'")
                    vari = args[2].strip("'")
                    supress = args[3] if len(args) > 3 else None
                    hotkeys.append({"hotkey": hotkey, "text": text, "vari": vari, "supress": supress})
                    newHotkey(hotkey, text, vari, supress)  # Register the hotkey
    except FileNotFoundError:
        pass
    return hotkeys

# initilasing keys
hotkeys = load_hotkeys_from_file()

# closing function
def on_closing():
    # cleanup action
    print("Exit programm...")
    root.destroy()  # close window

# gui
root = tk.Tk()
root.title("HotKeyEZ - @tamino1230")
root.geometry("800x400")
root.protocol("WM_DELETE_WINDOW", on_closing)  # event handler on closing
root.resizable(False, False)  # Größenänderung deaktivieren

label = tk.Label(root, text="You sometimes need to restart, to update.", font=("Helvetica", 8))
label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

# background color
root.configure(bg='lightblue')

# icon of the app
root.iconbitmap('babToma.ico') 

# inputssettings
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# inputs2
tk.Label(input_frame, text="Hotkey (example: shift+a; f6):").grid(row=0, column=0, padx=5, pady=5)
hotkey_entry = tk.Entry(input_frame)
hotkey_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Text: (example: Hello World!)").grid(row=1, column=0, padx=5, pady=5)
text_entry = tk.Entry(input_frame)
text_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Variable (unique name):").grid(row=2, column=0, padx=5, pady=5)
vari_entry = tk.Entry(input_frame)
vari_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Suppress ('True' or 'False' or nothing):").grid(row=3, column=0, padx=5, pady=5)
supress_entry = tk.Entry(input_frame)
supress_entry.grid(row=3, column=1, padx=5, pady=5)

# func action
def add_hotkey():
    hotkey = hotkey_entry.get()
    text = text_entry.get()
    vari = vari_entry.get()
    supress = supress_entry.get() or None  # if nothing on supress

    if not hotkey or not text or not vari:
        messagebox.showerror("Error", "The Field Hotkey, Text and Variable need to be filled out!")
        return

    hotkey_data = {"hotkey": hotkey, "text": text, "vari": vari, "supress": supress}
    hotkeys.append(hotkey_data)
    save_hotkeys_to_file(hotkeys)
    newHotkey(hotkey, text, vari, supress)  # register the new hotkey
    update_hotkey_list()
    clear_entries()

def delete_hotkey(index):
    hotkeys.pop(index)
    save_hotkeys_to_file(hotkeys)
    update_hotkey_list()

def edit_hotkey(index):
    hotkey = hotkeys[index]
    hotkey_entry.delete(0, tk.END)
    text_entry.delete(0, tk.END)
    vari_entry.delete(0, tk.END)
    supress_entry.delete(0, tk.END)

    hotkey_entry.insert(0, hotkey["hotkey"])
    text_entry.insert(0, hotkey["text"])
    vari_entry.insert(0, hotkey["vari"])
    if hotkey["supress"] is not None:
        supress_entry.insert(0, hotkey["supress"])

    hotkeys.pop(index)
    save_hotkeys_to_file(hotkeys)
    update_hotkey_list()

def clear_entries():
    hotkey_entry.delete(0, tk.END)
    text_entry.delete(0, tk.END)
    vari_entry.delete(0, tk.END)
    supress_entry.delete(0, tk.END)

# Hotkey-Liste anzeigen
list_frame = tk.Frame(root)
list_frame.pack(pady=10)

hotkey_listbox = tk.Listbox(list_frame, width=100, height=10)
hotkey_listbox.pack(side=tk.LEFT, padx=10, pady=10)

# Buttons für Aktionen
button_frame = tk.Frame(list_frame)
button_frame.pack(side=tk.RIGHT, padx=10)

add_button = tk.Button(button_frame, text="Add Hotkey", command=add_hotkey)
add_button.pack(fill=tk.X, pady=5)

def delete_selected():
    selected = hotkey_listbox.curselection()
    if not selected:
        return
    delete_hotkey(selected[0])

delete_button = tk.Button(button_frame, text="Delete Selected", command=delete_selected)
delete_button.pack(fill=tk.X, pady=5)

def edit_selected():
    selected = hotkey_listbox.curselection()
    if not selected:
        return
    edit_hotkey(selected[0])

edit_button = tk.Button(button_frame, text="Edit Selected", command=edit_selected)
edit_button.pack(fill=tk.X, pady=5)

# Update Hotkeys
def update_hotkey_list():
    hotkey_listbox.delete(0, tk.END)
    for hotkey in hotkeys:
        supress_text = f", Supress: {hotkey['supress']}" if hotkey["supress"] else ""
        hotkey_listbox.insert(tk.END, f"Hotkey: {hotkey['hotkey']}, Text: {hotkey['text']}, Variable: {hotkey['vari']}{supress_text}")

update_hotkey_list()

# start of the mainloop
root.mainloop()
