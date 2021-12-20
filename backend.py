from fastapi import FastAPI
import sqlite3


app = FastAPI()
conn = sqlite3.connect("database.db", check_same_thread=False)


@app.get("/api/search")
def search(query: str):
    query = query.replace("%20", " ")
    result = list(conn.execute("select title, video_link, image_link, highlight(videos, 3, '<b>', '</b>') from videos where captions match ?", (query,)))

    json_data = []
    for guest in result:
        data = {"title": guest[0],
                "video_link": guest[1],
                "image_link": guest[2],
                "timelines": []}
        index = guest[3].find("<b>")
        while index > -1:
            start = -1
            end = -1
            for i in range(index, index + 100):
                if guest[3][i] == "\n":
                    end = i
                    break
            for i in range(index, index - 100, -1):
                if guest[3][i] == "\n":
                    start = i
                    break

            data["timelines"].append(guest[3][start + 1:end])
            index = guest[3].find("<b>", end, -1)
        json_data.append(data)
    return json_data 
