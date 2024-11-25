import requests
import re
import json
import time


def get_video_url(cid,bvid,title):
    downheader = {"referer":"https://www.bilibili.com",
              "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
                        }
    url = 'https://api.bilibili.com/x/player/wbi/playurl?cid='+cid+'&bvid='+bvid
    r = json.loads(requests.get(url, headers=header).text)
    video_url = r['data']['durl'][0]['url']
    # 使用 replace 去掉特殊字符 写入文件
    special_chars = [',', '!', '@', '#', '$', '%', '^', '&', '*', ' ', '\\', '/', ':', '?', '|', '<', '>','"',"'"]
    for char in special_chars:
        title = title.replace(char, '')

    with open(title+'.mp4','wb') as f:
        f.write(requests.get(video_url,headers=downheader).content)
    print(title+"下载完成")
    return 1

id = "xxx" #favlist?fid=   需要修改 收藏夹id
surl = "https://api.bilibili.com/x/v3/fav/resource/list?media_id="+id+"&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web"

header = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    ,"referer":"https://www.bilibili.com"}

r = requests.get(url=surl,headers=header)
data = json.loads(r.text)
num = data['data']['info']["media_count"]
if num < 20: #只有一页
    for i in range(20):
        try:
            title = data['data']["medias"][i]['title']
            bvid = data['data']["medias"][i]['bvid']
            cid = data['data']["medias"][i]['ugc']['first_cid']
            get_video_url(str(cid),str(bvid),str(title))
        except IndexError:
            break
            print("全部下载完成")
else:#多页
    for p in range((int(num/20))+1): #下载全部 可按指定页下载 range(1,3)
        urlt = "https://api.bilibili.com/x/v3/fav/resource/list?media_id="+id+"&pn="+str(p+1)+"&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web"
        nd = requests.get(url=urlt,headers=header)
        data = json.loads(nd.text)
        for n in range(20):
            try:
                title = data['data']["medias"][n]['title']
                bvid = data['data']["medias"][n]['bvid']
                cid = data['data']["medias"][n]['ugc']['first_cid']
                if title=="已失效视频":
                    continue
                get_video_url(str(cid), str(bvid), str(title))
            except IndexError:
                break
        print("第" + str(p + 1) + "页下载完成")
        time.sleep(2)




                 #将mp4转化为mp3
#import  moviepy
# import  os
# directory = '.'
# for filename in os.listdir(directory):
#     # 检查是否是文件（而不是目录）
#     if os.path.isfile(os.path.join(directory, filename)):
#         if filename.endswith('.mp4'):
#             video_clip = moviepy.VideoFileClip(filename)
#             new_filename = filename.replace('.mp4', '.mp3')
#             video_clip.audio.write_audiofile(new_filename)
#             video_clip.close()
#             print(f"转换完成! 音频已保存为: {new_filename}")





