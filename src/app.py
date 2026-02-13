from fastapi import FastAPI, BackgroundTasks

from typing import List
import uvicorn
from fastapi import FastAPI, Query
import re
from services import *
from pydantic import BaseModel, Field

app = FastAPI()


MY_REGEX = r"https?:\/\/(www\.)?digikala.com/search/category-([-a-zA-Z0-9\/]*)"
class DigikalaURL(BaseModel):
    url:str = Field(pattern=MY_REGEX)
@app.post("/collect")
def get_collections_list(digikala_category_url: DigikalaURL, background_tasks: BackgroundTasks):
    category =  re.search(r"https://www.digikala.com/search/category-(.+?)(?:/|$)", digikala_category_url.url).group(1)
    background_tasks.add_task(crawl_digikala_comments, category)
    return {"message": "collecting data is started. it's take a few minutes"}


@app.get("/analyze_negative_comments")
def get_collections_list():
    return analyze_negative_comments()


@app.get("/sentiment_analysis")
def get_collections_list():
    return sentiment_analyze_comments()


@app.get("/topics")
def get_collections_list():
    return comments_topic_modeling()


@app.get("/name_entity_reconision")
def get_collections_list():
    return comments_ner()


@app.get("/similar_comments")
def get_collections_list():
    return find_similar_comments()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
