from src.app.App import App
import time

def commands(new_input):
        start_time = time.time()
        if new_input == "q":
            print("Exiting app")
        elif new_input == "play" or new_input == "resume" or new_input == 'p':
            App().toggle_pause_play()
        elif new_input == "skip":
            App().skip()
        elif new_input == "shuffle":
            App().shuffle()   
        elif new_input == "info" or new_input == '!i':
            App().current_track_info()
        elif new_input == "hi":
            print("Hello, world!")
        elif new_input == 'repeat':
            App().repeat()    
            
        elif new_input.startswith("volume"):
            App().volume(new_input.replace('volume', '').strip())
        else:
            print("Unknown command")
        end_time = time.time()
        runtime = end_time - start_time
        print("Runtime:", runtime, "seconds")  