import json
import math
import re
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = [20, 10]
plt.rcParams["font.size"] = 20

folder = "thebtsarmy"
if len(sys.argv) > 1:
    folder = sys.argv[2]

with open(f"{folder}/message_1.json", "r") as file:
    mes = json.load(file)
    mes_tb = pd.DataFrame(mes['messages'])
    mes_tb.set_index(pd.to_datetime(mes_tb["timestamp_ms"], unit='ms'), inplace=True)
    mes_tb.drop('timestamp_ms', inplace=True, axis=1)
# for i in range(2, 10):
#     with open(f"{folder}/message_" + str(i) + ".json", "r") as file:
#         mes = json.load(file)
#         temp = pd.DataFrame(mes['messages'])
#         temp.set_index(pd.to_datetime(temp["timestamp_ms"], unit='ms'), inplace=True)
#         temp.drop('timestamp_ms', inplace=True, axis=1)
#         mes_tb = pd.concat([temp, mes_tb])
print(mes_tb)

mes_tb = mes_tb.dropna(subset=['content'])
links = mes_tb[mes_tb.content.str.contains("youtube")].content.values
print(len(links))

url_regex = re.compile(
    r"((http(s)?(\:\/\/))+(www\.)?([\w\-\.\/])*(\.[a-zA-Z]{2,3}\/?))[^\s\b\n|]*[^.,;:\?\!\@\^\$ -]")
video_id = re.compile(r"v=(.{11})($|&)")


def filter_url(mes):
    match = url_regex.search(mes)
    if match:
        vmatch = video_id.search(match.group(0))
        if not vmatch:
            print(vmatch, match.group(0))
            return None
        else:
            return vmatch.group(1)
    else:
        return None


link_urls = list(filter(lambda x: x, map(filter_url, links)))
print(link_urls)
print(len(link_urls))
playlists = []
for i in range(0, math.ceil(len(link_urls) / 50)):
    playlist = f"https://www.youtube.com/watch_videos?video_ids={','.join(link_urls[i * 50:min(len(link_urls), (i + 1) * 50)])}"
    playlists.append(playlist)

for l in playlists:
    print(l)
# Instruction after clicking link
# 1. Replace watch with playlist and append &disable_polymer=true
# 2. Click 3 dots in the right and click add all to a playlist you want to save to
