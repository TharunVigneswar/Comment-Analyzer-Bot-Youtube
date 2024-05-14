import requests
import googleapiclient.discovery
from urllib.parse import urlparse, parse_qs

# Function to extract video ID from YouTube URL
def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc == 'www.youtube.com' and 'v' in parse_qs(parsed_url.query):
        return parse_qs(parsed_url.query)['v'][0]
    return None

# Function to classify text using a machine learning API
def classify_text(text):
    # Replace "MACHINE_LEARNING_MODEL_ID" with your actual model ID
    key = "MACHINE_LEARNING_MODEL_ID"
    url = f"https://machinelearningforkids.co.uk/api/scratch/{key}/classify"
    response = requests.get(url, params={"data": text})
    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch["class_name"]
    else:
        response.raise_for_status()

# Get video URL from user input
url = input("Enter video URL to detect video sentiment: ")
video_id = extract_video_id(url)

if video_id is None:
    print("Invalid YouTube video URL")
else:
    # Set up YouTube API
    DEVELOPER_KEY = "API_KEY"  # Replace "API_KEY" with your actual API key
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=DEVELOPER_KEY)

    # Get comments for the video
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )
    response = request.execute()

    # Classify comments and calculate sentiment
    sentiments = []
    for item in response['items']:
        comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
        sentiment = classify_text(comment_text)
        sentiments.append(sentiment)

    sentiment_score = sentiments.count("Positive") - sentiments.count("Negative")

    # Output sentiment result
    if sentiment_score > 0:
        print("Positive Video")
    elif sentiment_score == 0:
        print("Neutral Video")
    else:
        print("Negative Video")
