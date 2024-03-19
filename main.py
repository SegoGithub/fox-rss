import requests
import mimetypes
import os.path
from feedgen.feed import FeedGenerator

fg = FeedGenerator()
fg.title('FoxRSS')
fg.id('https://github.com/YuaFox/lynx-iberian')
fg.link( href='https://fox.sego.app/rss.xml', rel='self' )
fg.subtitle('the coolest feed ever cuz it has foxes')
fg.language('en')

if not os.path.exists('page'):
    with open("page", "w", encoding="utf-8") as f:
        f.write("0")
        attempts = 0
else:
    with open("page", "r+", encoding="utf-8") as f:
        attempts = int(f.read())
        f.seek(0)
        f.write(str(attempts + 1))
        f.truncate()
        attempts = attempts + 1

response = requests.get(f"https://foxes.cat/api/v1/media?page={attempts}").json()

def storage_resolver(path):
    service = path.split("/")[1]
    filename = path.split("/")[-1]
    if service == "reddit":
        return("https://i.redd.it/" + filename, mimetypes.guess_type(filename)[0])
    elif service == "flickr":
        return("https://farm2.staticflickr.com/1103/" + filename, mimetypes.guess_type(filename)[0])
    elif service == "local":
        return("https://foxes.cat/" + filename, mimetypes.guess_type(filename)[0])

for fox in response:

    fe = fg.add_entry()
    fe.id(fox["source"].split("/")[-1])
    fe.link(href=fox["source"])
    fe.content(content=f"Source: <a href=\"{fox["source"]}\">{fox["source"]}</a>", type="CDATA")

    image = storage_resolver(fox["path"])
    fe.enclosure(image[0], 0, image[1])

    if "subreddit" in fox:
        if fox["tag"]:
            fe.category([{"term": fox["tag"], "label": fox["tag"]}])
    elif "flickrId" in fox:
        flickr_response = requests.get(f"https://www.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key=9ace9e65a5ad1fae443d8a1c7c86e76f&format=json&nojsoncallback=1&photo_id={fox["flickrId"]}").json()

        fe.title(flickr_response["photo"]["title"]["_content"])
        fe.author(name=fox["author"])
        fe.description(flickr_response["photo"]["description"]["_content"])
        tags = []
        for tag in flickr_response["photo"]["tags"]["tag"]:
            tags.append({"term": tag["_content"], "label": tag["raw"]})
        fe.category(tags)
    else:

        fe.title("Cute fox :3c")
        fe.author(name=fox["author"])

fg.rss_file('rss.xml')