from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
""""
current code creates a playlist named test then adds a video to it
"""

# Set up OAuth 2.0 credentials and build YouTube API service
flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/youtube.force-ssl', 'https://www.googleapis.com/auth/youtube.readonly'])
creds = flow.run_local_server(port=8080)
youtube = build('youtube', 'v3', credentials=creds)

# Set the channel ID for the channel you want to retrieve playlists for
channel_id = 'INSERT CHANNEL ID HERE'

# Retrieve list of playlists and print out titles and IDs
playlists = youtube.playlists().list(part='snippet', mine=True).execute()
for playlist in playlists['items']:
    print(f"{playlist['snippet']['title']}: {playlist['id']}")
  

# Create the new playlist
request = youtube.playlists().insert(
    part='snippet,status',
    body={
        'snippet': {
            'title': 'test',
            'description': 'This is a test playlist',
            'tags': ['test', 'playlist']
        },
        'status': {
            'privacyStatus': 'public'
        }
    }
)

# Execute the API request

response = request.execute()
# Add the video with ID "BUqJMPAtmdY" to the "test" playlist
playlist_id = response["id"]
request = youtube.playlistItems().insert(
    part="snippet",
    body={
      "snippet": {
        "playlistId": playlist_id,
        "resourceId": {
          "kind": "youtube#video",
          "videoId": "BUqJMPAtmdY"
        }
      }
    }
)
response = request.execute()
# Print the new playlist ID
print(f"Created new playlist with ID: {response['id']}")

