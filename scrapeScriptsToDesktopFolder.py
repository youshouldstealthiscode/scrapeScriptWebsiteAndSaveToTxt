import os
import re
import requests
from bs4 import BeautifulSoup
import html2text

URL = "https://www.simplyscripts.com/tv_all.html"

def download_script(url, save_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type")
            if "text/rtf" in content_type:
                extension = ".rtf"
                content = response.content
            elif "application/pdf" in content_type:
                extension = ".pdf"
                content = response.content
            else:
                extension = ".txt"
                html = response.text
                formatter = html2text.HTML2Text()
                formatter.wrap_links = False
                formatter.inline_links = False
                formatter.ignore_links = True
                formatter.ignore_images = True
                formatter.ignore_anchors = True
                content = formatter.handle(html).encode("utf-8")

            file_path = os.path.join(save_path, f"{os.path.basename(url)}{extension}")
            with open(file_path, "wb") as f:
                f.write(content)
            print(f"Downloaded {url} as {file_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "lxml")

    desktop_path = os.path.expanduser("~/Desktop")
    base_path = os.path.join(desktop_path, "TV_Show_Scripts")
    os.makedirs(base_path, exist_ok=True)

    shows = soup.find_all("blockquote")

    for show in shows:
        show_name = show.find("b").text.strip()
        show_folder = re.sub(r"[^\w\s]", "", show_name).strip().replace(" ", "_")
        show_path = os.path.join(base_path, show_folder)
        os.makedirs(show_path, exist_ok=True)

        episodes = show.find_all("a", href=True)

        for episode in episodes:
            episode_url = episode["href"]
            if episode_url.endswith((".html", ".htm")):
                episode_name = episode.text.strip()
                episode_folder = re.sub(r"[^\w\s]", "", episode_name).strip().replace(" ", "_")
                save_path = os.path.join(show_path, episode_folder)
                os.makedirs(save_path, exist_ok=True)
                download_script(episode_url, save_path)

if __name__ == "__main__":
    main()
