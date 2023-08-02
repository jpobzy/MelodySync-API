from src.app.App import App
import time

def commands():
    while True:
        new_input = input("Enter your command: ")
        start_time = time.time()
        if new_input == "q":
            print("Exiting app")
            break
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
          
          
import random

def main():
    api = App()  # Create an instance of the API class
    # Call the display_name function
    start_time = time.time()

    # x = api.generate_playlist(100,"4NHQUGzhtTLFvgF5SZesLK",  "hip-hop", "0c6xIDDpzE81m2q797ordA")

    # print(len(x['tracks']))
    print()
    print(api.generate_playlist(10))
    # print(time.time())
    end_time = time.time()

    runtime = end_time - start_time
    print("Runtime:", runtime, "seconds")


if __name__ == "__main__":
    main()
    
