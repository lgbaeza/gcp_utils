import os

project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
dataset_name = 'demo_trends'
model = "gemini-2.5-pro"
table_name_gemini_search = 'trends_gemini'
table_name_youtube = 'trends_youtube'
table_name_google_trends = 'trends_google'
YOUTUBE_API_KEY = ""