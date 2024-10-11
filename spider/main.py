import re
import os
from src.api.kugou import Kugou
from src.api.kuwo import Kuwo
from src.log import log_config
from src.extractor import *
from __init__ import __name__, __version__, __author__, __describe__

main_log = log_config("Main")

path:str = os.getcwd().split("\\spider")[0]+'\\download'


kw = Kuwo()
kg = Kugou()


def download_kugou(song_name, kg_dicts, is_get_mv):
    main_log.info(f"Looking for the `{song_name}`...")
    hash = kg_dicts[song_name]
    song_hash = hash[0]
    mv_hash = hash[1]
    # 如果需要下载MV
    if is_get_mv:
        main_log.info("Start downloading MV...")
        mv = kg.get_mv_by_hash(mv_hash=mv_hash, h_quality=True)
        download(mv, filename=song_name, format="mp4")
    song = kg.get_music_by_hash(song_hash)[-1]
    # 如果歌曲是VIP歌曲,通过mv转换下载MP3
    if song == '':
        main_log.warning(f"Warning! The `{song_name}` is a paid VIP song!")
        main_log.info("Try to download music by mv...")
        # 判断是否已经有mv的存在
        if is_get_mv:
            mv2music(os.path.join(path, song_name))                
            os.remove(os.path.join(path, song_name+".mp4"))
        else:
            mv = kg.get_mv_by_hash(mv_hash=mv_hash)
            download(mv, filename=song_name, format="mp4")
            mv2music(os.path.join(path, song_name))                
            os.remove(os.path.join(path, song_name+".mp4"))
    else:
        download(song, filename=song_name)
    main_log.info(f"Downloading `{song_name}` successfully!\n\n")

def download_kuwo(kw_dicts, song_name):
    main_log.info(f"Start downloading `{song_name}`...")
    song_hash = kw_dicts[song_name]
    song = kw.get_music_by_id(rid=song_hash)
    if "588957081" in song:
        main_log.error("Error! Can not find the music!")
        main_log.warning("该酷我歌曲是VIP歌曲,API失效,请尝试下载酷狗源歌曲!")
        main_log.info("Done!\n\n")
        return
    download(song, song_name)
    main_log.info(f"Downloading `{song_name}` successfully!")

def search_then_download():
    music = input("请输入要下载的音乐名称:")
    page = input("请输入搜索的页数(default:1):")
    page = int(page or 1)
    pagesize = input("请输入每页的歌曲个数(default:10):")
    pagesize = int(pagesize or 10)
    is_get_mv = input("是否下载MV(Y/N, default:N[仅支持酷狗音乐MV下载]):")
    is_get_mv = False if (is_get_mv=='') or (is_get_mv=="N") else True

    main_log.info(f"Start searching for `{music}`...")
    try:
        kg_dicts = kg.search(keyword=music, page=page, pagesize=pagesize)
        # 酷我默认初始页数是0
        kw_dicts = kw.search(keyword=music, pn=page-1, rn=pagesize)
    except:
        raise ValueError("The page or the pagesize is Out of range limit!")
    kg_data = [{f"酷狗": keys} for keys in kg_dicts]
    kw_data = [{f"酷我": keys} for keys in kw_dicts]
    data = xmerge(kw_data, kg_data)
    for id, datas in enumerate(data):
        print(f"{id+1}|{get_simple_key(datas)}|{get_simple_value(datas)}")
    choice = input("请输入需要下载的歌曲序号(多选用`,`隔开):")
    if "," in choice: # 批量操作
        a = choice.split(",")
        for it in a:
            content = data[int(it)-1]
            song_name = get_simple_value(content)
            if is_site("酷狗", get_simple_key(content)):
                download_kugou(song_name, kg_dicts, is_get_mv)
            else:
                download_kuwo(kw_dicts=kw_dicts, song_name=song_name)
                
    else: # 单个下载
        content = data[int(choice)-1]
        song_name = get_simple_value(content)
        if is_site("酷狗", get_simple_key(content)):
            download_kugou(song_name=song_name, kg_dicts=kg_dicts, is_get_mv=is_get_mv)
        else:
            download_kuwo(song_name=song_name, kw_dicts=kw_dicts)



def download_by_kuwo_url():
    repeated = True
    while repeated:
        song_url = input("请输入要下载的酷我链接:")
        if song_url == "exit()" or song_url == '':
            break
        main_log.info(f"Start to download the `{song_url}`")
        song = kw.get_music_by_id(rid=''.join(re.findall(r"\d+", song_url)))
        # 含588957081.mp3的歌曲为错误音频
        if "588957081" not in song:
            download(url=str(song))
            main_log.info("Download Successfully!")
        else:
            main_log.error("The KuWo API is wrong. Can not find the music!")
            main_log.warning("We will skip the download task of this music!")
        
        repeat = input("是否继续下载(Y/N, default:N):")
        repeated = True if (repeat=="Y") or (repeat=="y") else False
        

def download_by_kuwo_playlist():
    repeated = True
    while repeated:
        playlist_url = input("请输入要下载的 酷我歌单 名称:")
        if playlist_url == 'exit()' or playlist_url=='':
            break
        main_log.info(f"Start to get the `{playlist_url}`...")
        song = kw.get_music_by_playlist(playlist_url=playlist_url)
        for song_name in song:
            download(url=song[song_name], filename=song_name)
            main_log.info(f"Downloading`{song_name}`...")
        main_log.info("Download the Playlist Successfully!")        
        repeat = input("是否继续下载(Y/N, default:N):")
        repeated = True if (repeat=="Y") or (repeat=="y") else False


try: 
    number = int(input("`-  请输入下载类型(输入编号)\
          \n`- 1.搜索歌曲并下载\
          \n`- 2.通过酷我链接下载酷我单曲\
          \n`- 3.通过酷我歌单下载歌单全部歌曲\
          \n:"))
    match number:
        case 1:
            search_then_download()
        case 2:
            download_by_kuwo_url()
        case 3:
            download_by_kuwo_playlist()
        case _:
            main_log.error("Error!错误的输入!")
            raise Exception
        
except KeyboardInterrupt:
    main_log.warning("\nexit\n")

finally:
    main_log.info("\033[0;32m All Done!\033[0m")
    os.system("pause")