from API import API

if __name__ == "__main__":
    x = API()
    while True:
        new_input = input("Enter your command: ")
        if new_input == "q":
            print("Exiting app")
            break
        elif new_input == "pause":
            x.pause()
        elif new_input == "play" or new_input == "resume":
            x.play()
        elif new_input == "skip":
            x.skip()
        elif new_input == "shuffle":
            x.shuffle()   
        elif new_input == "info":
            x.current_track_info()
        elif new_input == "hi":
            print("Hello, world!")
        else:
            print("Unknown command")
