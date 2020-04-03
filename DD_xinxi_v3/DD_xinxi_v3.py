import requests
import json
import sys
import os
import configparser

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8"
} #设置头文件，伪装请求为TODO:谷歌访问

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "DD.ini")

class DD_xinxi():

    def __init__(self):

        self.DDcf = configparser.ConfigParser()
        self.DDcf.read(configPath)
        self.meau = {
            1:"NekoMoeK",
            2:"鹿乃",
            3:"阿夸",
            4:"mea",
            5:"烤兔",
            6:"绿粽子",
            7:"喵喵狐",
            8:"天哥",
            9:"其他",
            -1:"菜单",
            -2:"其他uid",
            0:"退出",
        }

    def get_uid(self,user_id):

        user_id -= 1
        value_get = self.DDcf.items('def_xinxi')
        return value_get[user_id][1]

    def pust_uid(self,user_id):
        return self.get_xinxi(self.get_uid(user_id))

    def get_xinxi(self,uid):

        setprint = {} #空字典，后续加入数据返回

        #抓取所需的页面信息
        urlfensi = requests.get(f"https://api.bilibili.com/x/relation/stat?vmid={uid}",headers=headers)
        urllike = requests.get(f"https://api.bilibili.com/x/space/upstat?mid={uid}",headers=headers)
        urluser = requests.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}",headers=headers)
        urllive = requests.get(f"https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid={uid}",headers=headers)

        #截取json数据填入字典
        setprint['ID'] = urluser.json().get("data").get("name")
        setprint['uid'] = urluser.json().get("data").get("mid")
        setprint['粉丝数'] = urlfensi.json().get("data").get("follower")
        setprint['总播放量'] = urllike.json().get("data").get("archive").get("view")
        setprint['点赞数'] = urllike.json().get("data").get("likes")
        setprint['直播地址'] = urllive.json().get("data").get("url")
        if urllive.json().get("data").get("liveStatus") == 1:
            setprint["开播情况"] = "直播中"
        elif urllive.json().get("data").get("liveStatus") == 0:
            setprint["开播情况"] = "未开播"

        return setprint #返回数据

    def qita(self):
        try:
            user_set_uid = int(input("请输入查询uid："))
            return self.get_xinxi(user_set_uid)
        except ValueError:
            print("请输入正确参数")


if __name__ == "__main__":
    tset = DD_xinxi()
    print("="*8+"欢迎使用DD,需要帮助请输入-1"+"="*8)
    while True:
        try:
            user_id = int(input("DD> "))
            if user_id == -1:
                for key,value in tset.meau.items():
                    print(str(key)+"\t\t"+value) #打印目录
            elif user_id == 0:
                print("欢迎下次使用")
                sys.exit(0)
            elif user_id == -2:
                try:
                    print("="*20)
                    for key,value in tset.qita().items():
                        print(str(key)+": "+str(value))
                    print("="*20)
                except Exception:
                    print("找不到用户")
            else:
                try:
                    print("="*20)
                    for key,value in tset.pust_uid(user_id).items():
                        print(str(key)+": "+str(value))
                    print("="*20)
                except IndexError:
                    print("预选选项没有此项")
        except KeyboardInterrupt:
            print("欢迎下次使用")
            sys.exit(0)
        except ValueError:
            print("输入错误，请输入正确参数")
