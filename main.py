import requests
import json
import os

# b站登录Cookie
cookie = ""


def get_image_index(epid, cmid, width):
    req_headers = {"accept": "application/json, text/plain, */*",
                   "accept-encoding": "",
                   "accept-language": "zh-CN,zh;q=0.9",
                   "content-type": "application/json;charset=UTF-8",
                   "cookie": cookie,
                   "origin": "https://manga.bilibili.com",
                   "referer": "https://manga.bilibili.com/mc{}/{}?from=manga_detail".format(cmid, epid),
                   "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                   "sec-ch-ua-mobile": "?0",
                   "sec-ch-ua-platform": '"Windows"',
                   "sec-fetch-dest": "empty",
                   "sec-fetch-mode": "cors",
                   "sec-fetch-site": "same-origin",
                   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    req_data = json.dumps({"ep_id": epid})
    rep = requests.post("https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web",
                        data=req_data, headers=req_headers)
    rep_ = json.loads(rep.text)
    if rep_["code"] == 0:
        ret = []
        for e in rep_["data"]["images"]:
            if width > 0:
                ret.append(e["path"]+"@{}w".format(width))
            else:
                ret.append(e["path"])
        return ret
    return None


def download_images(urls, epid, title, cmid):
    req_headers = {"accept": "application/json, text/plain, */*",
                   "accept-encoding": "",
                   "accept-language": "zh-CN,zh;q=0.9",
                   "content-type": "application/json;charset=UTF-8",
                   "cookie": cookie,
                   "origin": "https://manga.bilibili.com",
                   "referer": "https://manga.bilibili.com/mc{}/{}?from=manga_detail".format(cmid, epid),
                   "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                   "sec-ch-ua-mobile": "?0",
                   "sec-ch-ua-platform": '"Windows"',
                   "sec-fetch-dest": "empty",
                   "sec-fetch-mode": "cors",
                   "sec-fetch-site": "same-origin",
                   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    req_data = json.dumps({"urls": json.dumps(urls)})
    rep = requests.post("https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web",
                        data=req_data, headers=req_headers)
    rep_ = json.loads(rep.text)
    if rep_["code"] == 0:
        count = 1
        os.mkdir("download/{}".format(title))
        for t in rep_["data"]:
            img_url = t["url"]+"?token="+t["token"]
            rep2 = requests.get(img_url, headers=req_headers)
            with open("download/{}/{}.jpg".format(title, count), "wb") as f:
                f.write(rep2.content)
                print("success {}".format(count))
            count += 1


def download_all(cmid, width=0):
    req_headers = {"accept": "application/json, text/plain, */*",
                   "accept-encoding": "",
                   "accept-language": "zh-CN,zh;q=0.9",
                   "content-type": "application/json;charset=UTF-8",
                   "cookie": cookie,
                   "origin": "https://manga.bilibili.com",
                   "referer": "https://manga.bilibili.com/detail/mc{}?from=manga_person".format(cmid),
                   "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                   "sec-ch-ua-mobile": "?0",
                   "sec-ch-ua-platform": '"Windows"',
                   "sec-fetch-dest": "empty",
                   "sec-fetch-mode": "cors",
                   "sec-fetch-site": "same-origin",
                   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    req_data = json.dumps({"comic_id": cmid})
    rep = requests.post("https://manga.bilibili.com/twirp/comic.v1.Comic/ComicDetail?device=pc&platform=web",
                        data=req_data, headers=req_headers)
    rep_ = json.loads(rep.text)
    if rep_["code"] == 0:
        eplist = rep_["data"]["ep_list"]
        for i in eplist:
            epid = i["id"]
            title = i["title"]
            img_urls = get_image_index(epid, cmid, width)
            download_images(img_urls, epid, title, cmid)


if __name__ == "__main__":
    download_all(24442, 480)  # 两个数字分别是漫画ID和图片宽度，图片宽度不填则为下载原图
