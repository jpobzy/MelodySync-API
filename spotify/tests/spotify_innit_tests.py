class spotify_innit_tests():
    def run_tests(spotify):
        # print("BEGINNING TEST RUNS FOR spotifyAPI")
        expected_display_name = "JPobs_"
        expected_id = "nnnp2au6xj317cjmxn9jsuxlj"
        expected_image_url = "https://i.scdn.co/image/ab6775700000ee85e93208cee96d61db701839a2"
        expected_uri = "spotify:user:nnnp2au6xj317cjmxn9jsuxlj"
        assert spotify.get_display_name() == expected_display_name, f"get_display_name DID NOT MATCH. Expected: {expected_display_name}, Actual: {spotify.get_display_name()}"
        assert spotify.get_id() == expected_id, f"GET DISPLAY NAMES DID NOT MATCH. Expected: {expected_display_name}, Actual: {spotify.get_id()}"
        assert spotify.get_profile_image_url() == expected_image_url, f"GET DISPLAY NAMES DID NOT MATCH. Expected: {expected_display_name}, Actual: {spotify.get_profile_image_url()}"
        assert spotify.get_uri() == expected_uri, f"GET DISPLAY NAMES DID NOT MATCH. Expected: {expected_display_name}, Actual: {spotify.get_uri()}"


