from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api import YouTubeTranscriptApi
import concurrent.futures
from bs4 import BeautifulSoup
from dataclasses import dataclass
import requests
import sqlite3
import re


@dataclass
class Guest:
    title: str
    link: str
    img: str
    captions: str


def get_text_captions(video_id: str) -> str:
    tr = YouTubeTranscriptApi.get_transcript(video_id)
    formatter = TextFormatter()
    formatted = formatter.format_transcript(tr)
    return formatted


def map_guest(guest):
    vid_title_link = guest.find("div", {"class": "vid-title"}).find("a")
    link = vid_title_link["href"]
    title = vid_title_link.decode_contents()
    img = guest.find("div", {"class": "thumb-youtube"}).find("img")["src"]
    video_id = re.search("\?v=(.+)", link).group(1)
    try:
        captions = get_text_captions(video_id)
    except Exception:
        captions = None
    return Guest(title, link, img, captions)


if __name__ == "__main__":
    conn = sqlite3.connect("database.db", check_same_thread=False)
    with open("podcasts.html") as html:
        soup = BeautifulSoup(html, "html.parser")
        guests = soup.find_all("div", {"class": "guest"})
        guests_number = len(guests)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = (executor.submit(map_guest, guest) for guest in guests)
            n = 0
            for future in concurrent.futures.as_completed(futures):
                try:
                    res = future.result()
                except Exception as e:
                    print(e)
                n += 1
                if res.captions is None:
                    print(res.link)
                else:
                    conn.execute("insert into videos (title, video_link, image_link, captions) values (?, ?, ?, ?)", 
                                 (res.title, res.link, res.img, res.captions,))
                print(f"{n / guests_number * 100}%", end="\r")
        conn.commit()

