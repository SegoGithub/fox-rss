import requests
import mimetypes
import os.path
from feedgen.feed import FeedGenerator

fg = FeedGenerator()
fg.title('OnlyFoxes')
fg.id('https://github.com/YuaFox/lynx-iberian')
fg.link( href='https://fox.sego.app/', rel='self' )
fg.subtitle('the coolest feed ever cuz it has only foxes')
fg.language('en')

if not os.path.exists('page'):
    with open("page", "w", encoding="utf-8") as f:
        f.write("0")
        page = 0
else:
    with open("page", "r+", encoding="utf-8") as f:
        page = int(f.read())
        f.seek(0)
        f.write(str(page + 1))
        f.truncate()
        page = page + 1

response = requests.get(f"https://foxes.cat/api/v1/media?page={page}").json()

def storage_resolver(path, id):
    service = path.split("/")[1]
    filename = path.split("/")[-1]

    if service == "reddit":
        return(f"https://i.redd.it/{filename}", mimetypes.guess_type(filename)[0])
    elif service == "flickr":
        return(f"https://farm2.staticflickr.com/1103/{filename}", mimetypes.guess_type(filename)[0])
    elif service == "local":
        return(f"https://foxes.cat/api/v1/media/{id}/file", mimetypes.guess_type(filename)[0])

for fox in response:
    fe = fg.add_entry()
    
    
    if fox["caption"]:
        fe.description(fox["caption"])
    if fox["author"]:
        fe.author(fox["author"])
    else:
        fe.author(name="Unknown")
    
    image = storage_resolver(fox["path"], fox["id"])
    fe.link(link=[{"href": image[0], "type": image[1], "rel": "enclosure"}])

    fe.id(image[0])

    if fox["source"]:
        fe.content(content=f"Source: <a href=\"{fox["source"]}\">{fox["source"]}</a>", type="html")
    else:
        fe.content(content=f"Image URL: <a href=\"{image[0]}\">{image[0]}</a>", type="html")

    if "subreddit" in fox:
        fe.title(fox["title"])
        if fox["tag"]:
            fe.category([{"term": fox["tag"], "label": fox["tag"]}])
    elif "flickrId" in fox:
        flickr_response = requests.get(f"https://www.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key=9ace9e65a5ad1fae443d8a1c7c86e76f&format=json&nojsoncallback=1&photo_id={fox["flickrId"]}").json()

        fe.title(flickr_response["photo"]["title"]["_content"])
        fe.description(flickr_response["photo"]["description"]["_content"])
        tags = []
        for tag in flickr_response["photo"]["tags"]["tag"]:
            tags.append({"term": tag["_content"], "label": tag["raw"]})
        fe.category(tags)
    else:
        fe.title("Cute fox :3c")

fg.rss_file('rss.xml')
fg.atom_file('atom.xml')