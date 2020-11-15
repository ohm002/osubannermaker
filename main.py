import os
import io
import requests
import re
import urllib.request
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
apikey = json.loads(open("config.json").read())['apikey']

mapid = input("BeatmapsetID:\n")
image_base = urllib.request.urlretrieve(f"https://assets.ppy.sh/beatmaps/{mapid}/covers/cover.jpg", "base.jpg")
# # add vig
# import cv2
# import numpy as np

# img = cv2.imread(f"base.jpg")
# rows, cols = img.shape[:2]

# # generating vignette mask using Gaussian kernels
# kernel_x = cv2.getGaussianKernel(cols,500)
# kernel_y = cv2.getGaussianKernel(rows,500)
# kernel = kernel_y * kernel_x.T
# mask = 255 * kernel / np.linalg.norm(kernel)
# output = np.copy(img)

# # applying the mask to each channel in the input image
# for i in range(3):
#     output[:,:,i] = output[:,:,i] * mask

# cv2.imwrite((f"base.jpg"), output)
# cv2.waitKey(0)

im = Image.open(f"base.jpg").convert("RGBA")
# im = im.filter(filter=ImageFilter.GaussianBlur(radius=2))
txt = Image.new("RGBA", im.size, (255,255,255,0))
fnt = ImageFont.truetype("NotoSansJP-Bold.otf", 40)
fnt2 = ImageFont.truetype("NotoSansJP-Bold.otf", 20)
d = ImageDraw.Draw(txt)

api = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={apikey}&s={mapid}")
api = api.json()

W, H = (450,250/2)
msg = f"{api[0]['artist']}\n{api[0]['title']}"
msg2 = f"Mapped by : {api[0]['creator']}"
w, h = d.textsize(msg, font=fnt)
w2, h2 = d.textsize(msg2, font=fnt2)
# shadow
d.text((W-(w/2)+5,30+5), msg, font=fnt, fill=(0,0,0,200), align='center', stroke_width=2, stroke_fill=(0,0,0,0))
d.text((W-(w2/2)+3,200+3), msg2, font=fnt2,    ill=(0,0,0,200), align='center', stroke_width=2, stroke_fill=(0,0,0,0))
# real
d.text((W-(w/2),30), msg, font=fnt, fill=(255,255,255,255), align='center', stroke_width=2, stroke_fill=(0,0,0,255))
d.text((W-(w2/2),200), msg2, font=fnt2, fill=(255,255,255,255), align='center', stroke_width=2, stroke_fill=(0,0,0,255))

out = Image.alpha_composite(im, txt)

os.remove("base.jpg")
out.save(f"{api[0]['beatmapset_id']}.png")
exit = input("Done\nPress Enter To Show This Image")
out.show()
quit()