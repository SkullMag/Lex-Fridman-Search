from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import sqlite3
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
conn = sqlite3.connect("database.db", check_same_thread=False)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/search")
def search(query: str):
    query = query.replace("%20", " ")
    result = list(conn.execute(f"select distinct title, video_link, image_link, highlight(videos, 3, '<b>', '</b>') from videos where captions match '\"{query}\"'"))

    json_data = []
    for guest in result:
        data = {"title": guest[0],
                "videoLink": guest[1],
                "imageLink": guest[2],
                "timelines": []}
        index = guest[3].find("<b>")
        while index > -1:
            start = -1
            end = -1
            for i in range(index, index + 100):
                if i not in range(len(guest[3])):
                    end = i - 1
                    break
                if guest[3][i] == "\n":
                    end = i
                    break
            for i in range(index, index - 100, -1):
                if i not in range(len(guest[3])):
                    start = i + 1
                    break
                if guest[3][i] == "\n":
                    start = i
                    break

            data["timelines"].append(guest[3][start + 1:end])
            index = guest[3].find("<b>", end, -1)
        json_data.append(data)
    return JSONResponse(content=json_data)


@app.get("/", response_class=HTMLResponse)
def index():
    return open("fridman-search-react-app/build/index.html").read()
