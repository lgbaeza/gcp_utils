from google import genai
from google.genai import types
import os
import googleapiclient.discovery
import base64
from io import StringIO
import pandas as pd
import json
from google.cloud import bigquery
import constants
from datetime import date, datetime

ai_client = genai.Client(
  vertexai=True,
  location="global",
)
bq_client = bigquery.Client()

def save_bq_table(table_name, dataframe):
    table_id = f"{constants.project_id}.{constants.dataset_name}.{table_name}"
    job = bq_client.load_table_from_dataframe(
        dataframe, table_id, job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    )
    job.result()
    
def prepare_env():
    SQL = f"""
        CREATE SCHEMA IF NOT EXISTS `{constants.project_id}.{constants.dataset_name}`;
    """
    run_bq_query(SQL)
    
def run_bq_query(SQL):
    query_job = bq_client.query(SQL)
    query_job.result()
    
def run_bq_query_df(SQL):
    query_job = bq_client.query(SQL)
    return query_job.to_dataframe()

def get_categories_from_term(terms):
    prompt = f"""
        You are an expert in retail and will receive a list of search terms from google trends. 
        Categorize each term it in categories that might be relevant for a retailer, like: artist, event, sports, music, games, etc, list is not exhaustive. 
        You can add multiple categories.  
        Always return a list separated by comma of the categories for each term.
        Only return the categories, nothing more.
        If no category is found, return 'None'
        The term list is: 
        {terms}
    """
    msg1_text1 = types.Part.from_text(text = prompt)
    contents = [
        types.Content(
          role="user",
          parts=[
            msg1_text1
          ]
        )
    ]

    cat_text = gemini_request(contents)
    return cat_text
    
def get_bq_trends():
    SQL = f"""
        SELECT 
            region_name
            , term
            , score
            , week
            , rank
            FROM  `bigquery-public-data.google_trends.international_top_rising_terms` 
            WHERE 
              country_name = 'Chile'
              AND rank <= 5
              and week >= (select week from `bigquery-public-data.google_trends.international_top_rising_terms` order by week desc limit 1)
            ORDER by region_name, rank desc;
    """
    query_job = bq_client.query(SQL)
    df = query_job.to_dataframe() 
    df["source"] = "google_trends"
    categories = get_categories_from_term('\n'.join(df['term'].values))
    df["categories"] = categories.split('\n')
    
    return df

def gemini_request(contents):
    tools = [
        types.Tool(google_search=types.GoogleSearch()),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature = 1,
        top_p = 0.95,
        seed = 0,
        max_output_tokens = 65535,
        safety_settings = [types.SafetySetting(
          category="HARM_CATEGORY_HATE_SPEECH",
          threshold="OFF"
        ),types.SafetySetting(
          category="HARM_CATEGORY_DANGEROUS_CONTENT",
          threshold="OFF"
        ),types.SafetySetting(
          category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
          threshold="OFF"
        ),types.SafetySetting(
          category="HARM_CATEGORY_HARASSMENT",
          threshold="OFF"
        )],
        tools = tools,
        thinking_config=types.ThinkingConfig(
          thinking_budget=-1,
        ),
    )

    out_text = ""  
    for chunk in ai_client.models.generate_content_stream(
        model = constants.model,
        contents = contents,
        config = generate_content_config,
        ):
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue
        out_text += chunk.text
        
    return out_text

def generate_gemini_trends():
    prompt = """
        Create a json list with a list of the top 10 trends in Chile for the last 7 days that a retailer could use to prioritize product selling, add properties:
        - trend: short name of the trend
        - description: what is the trend
        - ranking: popularity relative to the same day, from 1-10
        - date
        - category: categorize the trend like sports, artist, music, holiday,
        - source: where is this being talked about

        Discard any information related to: deaths, politics, tragedy, accidents. 
        Do not include any other info in the output, only the json object. 
    """
    msg1_text1 = types.Part.from_text(text = prompt)
    contents = [
        types.Content(
          role="user",
          parts=[
            msg1_text1
          ]
        )
    ]

    json_text = gemini_request(contents).replace('```json','').replace('```','')
    json_file_like_object = StringIO(json_text)
    df = pd.read_json(json_file_like_object)
    
    df["source"] = "gemini_search"

    return df

def get_popular_videos(api_key, region_code='CL', max_results=15):
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key
    )

    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        hl="es",
        regionCode = region_code,
        maxResults = max_results
    )
    response = request.execute()
    popular_videos = []
    for item in response.get("items", []):
        video_title = item["snippet"]["title"]
        video_id = item["id"]
        view_count = item["statistics"].get("viewCount", "N/A")
        like_count = item["statistics"].get("likeCount", "N/A")
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        prompt = f"""
            Create a json with info extracted from this video as if you were a retail agent that wants to capture trends to personalize the product catalog. All info should be in spanish:
            - summary
            - keywords: topics separated by a comma of relevant things covered in the video
            - category: music, sports, holidays, artists, etc
            
            Do not provide anything else, but the requested content. If you cannot access the video or generate the requested content, return either way the json structured requested, but with NULL values.
        """
        msg_video = types.Part.from_uri(
            file_uri=video_url,
            mime_type="video/mp4")
        msg1_text1 = types.Part.from_text(text = prompt)
        contents = [
            types.Content(
              role="user",
              parts=[
                msg1_text1, msg_video
              ]
            )
        ]
        
        json_text = gemini_request(contents).replace('```json','').replace('```','')
        json_obj = json.loads(json_text)
        
        popular_videos.append({
            "title": video_title,
            "url": video_url,
            "views": view_count,
            "likes": like_count,
            "summary": json_obj['summary'],
            "keywords": json_obj['keywords'],
            "category": json_obj['category']
        })

    popular_videos = pd.DataFrame(popular_videos)
    popular_videos["source"] = "youtube"
    popular_videos["date"] = datetime.now().strftime("%Y-%m-%d")
    
    return popular_videos