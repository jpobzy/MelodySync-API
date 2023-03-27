class input_options():
    def __init__(self):
        pass

    def get_input_scope(self):
        scopes = {
            "public": """
                ugc-image-upload
                user-read-playback-state
                user-modify-playback-state
                user-read-currently-playing
                app-remote-control
                playlist-modify-public
                playlist-modify-private
                playlist-read-private
                playlist-read-collaborative
                """,
            "private": """
                user-read-email
                user-read-private
                user-library-read
                user-library-modify
                user-read-recently-played
                """
        }

        scope_choice = input("Please choose public, private, both scope setting: ")
        if scope_choice in scopes:
            return scopes[scope_choice]
        elif scope_choice == "both":
            return scopes["public"] + scopes["private"]
        else:
            raise ValueError("Invalid input")
