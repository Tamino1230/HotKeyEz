import keyboard as k

by = "tamino1230"

def newHotkey(hotkey, text, vari, supr=None):
 
    key = hotkey

    def vari():
        k.write(text)

    
    if supr == None:
        k.add_hotkey(key, vari)
    elif supr == True:
        k.add_hotkey(key, vari, suppress=True)
    elif supr == False:
        k.add_hotkey(key, vari)
    else: 
        k.add_hotkey(key, vari)

newHotkey("5", "Im streaming right now on Twitch @tamino001 <3", "hotkey1", True)
newHotkey("6", "ggwp have a nice day yall! Was fun to playyy", "hotkey4", True)
newHotkey("7", "Hii gl hf!", "hotkey6", True)

input('\nPress ENTER to quit the programm...')