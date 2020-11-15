import os
import io
import requests
import re
import urllib.request
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
apikey = json.loads(open("config.json").read())['apikey']
# Input Phase
mapid = input("BeatmapsetID:\n")
# Getting a Background Image
image_base = urllib.request.urlretrieve(f"https://assets.ppy.sh/beatmaps/{mapid}/covers/cover.jpg", "base.jpg")
im = Image.open(f"base.jpg").convert("RGBA")
txt = Image.new("RGBA", im.size, (255,255,255,0))
# Initiallize Fonts & Images
fnt = ImageFont.truetype("NotoSansJP-Bold.otf", 40)
fnt2 = ImageFont.truetype("NotoSansJP-Bold.otf", 20)
d = ImageDraw.Draw(txt)

# Use API to get the Beatmap Data
api = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={apikey}&s={mapid}")
api = api.json()

# Write the text
W, H = (450,250/2)
msg = f"{api[0]['artist']}\n{api[0]['title']}"
msg2 = f"Mapped by : {api[0]['creator']}"
w, h = d.textsize(msg, font=fnt)
w2, h2 = d.textsize(msg2, font=fnt2)
# -- shadow
d.text((W-(w/2)+5,30+5), msg, font=fnt, fill=(0,0,0,200), align='center', stroke_width=2, stroke_fill=(0,0,0,0))
d.text((W-(w2/2)+3,200+3), msg2, font=fnt2,    ill=(0,0,0,200), align='center', stroke_width=2, stroke_fill=(0,0,0,0))
# -- text
d.text((W-(w/2),30), msg, font=fnt, fill=(255,255,255,255), align='center', stroke_width=2, stroke_fill=(0,0,0,255))
d.text((W-(w2/2),200), msg2, font=fnt2, fill=(255,255,255,255), align='center', stroke_width=2, stroke_fill=(0,0,0,255))

# Merge the Text Layer and the Image layer together
out = Image.alpha_composite(im, txt)

# Remove the Base Background Image File
os.remove("base.jpg")
# Save the Image
out.save(f"{api[0]['beatmapset_id']}.png")
# Do some actions
exit = input("Done\nPress Enter To Show This Image")
out.show()
quit()