
import re
import os

from src.api.kugouA import Kugou
from src.api.kuwo import Kuwo
from src.extractor import mv2music
from src.log import log_config
from src.extractor import download
from typing import Dict
from __init__ import __name__, __version__, __author__

mainLog = log_config("Main")

try:
    while (music := input("\n请输入要下载的歌曲或酷我链接:")) != 'exit()':
        if music == '':
            mainLog.error("\033[0;37;42m Error!歌曲为空!\033[0m")
            break
        if "https://" in music or "http://" in music:
            kw = Kuwo()
            if "play_detail" in music:
                song = kw.get_music_by_id(rid=''.join(re.findall(r"\d+", music)))
                download(url=str(song))
            else:
                mainLog.info(f"Start to get the http(get) to the {music}")
                song = kw.get_music_by_playlist(playlist_url=music)
                for song_name in song:
                    download(url=song[song_name], filename=song_name)
                    mainLog.info(f"下载{song_name}中……")
                mainLog.info("Successfully Download All Music of the playlist")
        else:
            mainLog.info(f"解析 `{music}`")
            kugou = Kugou(music)
            # kw = Kuwo()
            mainLog.info("开始搜索……")
            page = input("请输入搜索的页数(default:1):")
            page = int(page or 1)
            pagesize = input("请输入每页的个数(default:20):")
            pagesize = int(pagesize or 20)
            isGetMV = input("是否下载MV(default:n)[y/n]:")
            isGetMV = False if isGetMV=='' else True

            mainLog.info("搜索中……")
            # music_list = kw.search(music)
            info, hash, mv = kugou._search(page=page, pagesize=pagesize, mvUrl=True)
            mainLog.info(f"Start getting {info}")
            
            url = kugou._getMusicUrl(hash)
            if url == 0 or isGetMV:
                mvUrl = kugou._getMvUrl(mvHash=mv)
                download(url=mvUrl, filename=info+'_MV', format="mp4")
            if url == 0:
                mv2music(os.getcwd()+'\\download\\'+info)
                os.remove(os.getcwd()+'\\download\\'+info+'_MV.mp4')
            else:
                if url is None:
                    break
                download(url=url[0], filename=info, format="mp3")
           
except KeyboardInterrupt:
    mainLog.warning("exit\n")

finally:
    mainLog.info("\033[0;32m All Done!\033[0m")
    os.system("pause")


