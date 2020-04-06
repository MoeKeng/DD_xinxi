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
} # TODO:设置头文件，伪装请求为谷歌访问

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "DD.ini")

class DD_xinxi():

    def __init__(self):

        self.DDcf = configparser.ConfigParser(allow_no_value = True)
        self.DDcf.read(configPath,encoding='utf-8-sig')

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
        setprint['直播标题'] = urllive.json().get("data").get("title")
        if urllive.json().get("data").get("liveStatus") == 1:
            setprint["开播情况"] = "直播中"
        elif urllive.json().get("data").get("liveStatus") == 0:
            setprint["开播情况"] = "未开播"

        return setprint #返回数据

    def qita(self,user_set_uid):
        try:
            return self.get_xinxi(user_set_uid)
        except ValueError:
            print("请输入正确参数")

    def addmeau(self):
        try:
            find_uid = 1
            user_set_id = input("请输入添加的名称：")
            user_set_uid = int(input("请输入添加uid："))
            try:
                self.qita(user_set_uid)
            except Exception:
                find_uid = 0
            if find_uid == 1:
                self.DDcf.set("def_xinxi",user_set_id,str(user_set_uid))
                self.DDcf.set("def_meau",str(len(self.DDcf.items('def_meau')) - 4),user_set_id)
                with open(configPath,'w+',encoding="utf-8-sig") as f:
                    self.DDcf.write(f)
                print(f"添加成功,序号为{str(len(self.DDcf.items('def_meau')) - 5)}")
            elif find_uid == 0:
                print("添加失败，无效uid")
        except ValueError:
            print("请输入正确参数")

    def delmeau(self):
        try:
            find_uid = 1
            user_set_id = input("请输入删除的名称：")
            user_set_uid = int(input("请输入要删除的预选项："))
            if user_set_uid <= 0:
                print("无法删除此预选")
            elif user_set_uid > 0:
                for key,value in self.DDcf.items("def_xinxi"):
                    if user_set_id == key:
                        find_uid = 1
                    elif user_set_id != key:
                        find_uid = 0
                if find_uid == 1:
                    self.DDcf.remove_option("def_xinxi",user_set_id)
                    self.DDcf.remove_option("def_meau",str(user_set_uid))
                    with open(configPath,'w+',encoding="utf-8-sig") as f:
                        self.DDcf.write(f)
                    print("删除成功")
                elif find_uid == 0:
                    print("删除失败，找不到此项")
        except ValueError:
            print("请输入正确参数")


    def get_meau(self):
        meau = sorted(self.DDcf.items("def_meau"),key=lambda item:item[0], reverse=False)
        for key,value in meau:
            print(str(key)+"\t\t"+str(value)) #打印目录

if __name__ == "__main__":
    tset = DD_xinxi()
    print("="*8+"欢迎使用DD,需要帮助请输入-1"+"="*8)
    tset.get_meau()
    while True:
        try:
            user_id = int(input("DD> "))
            if user_id == -1:
                tset.get_meau()
            elif user_id == 0:
                print("欢迎下次使用")
                sys.exit(0)
            elif user_id == -2:
                try:
                    user_set_uid = int(input("请输入查询uid："))
                    print("="*20)
                    for key,value in tset.qita(user_set_uid).items():
                        print(str(key)+": "+str(value))
                    print("="*20)
                except Exception:
                    print("找不到用户")
                except ValueError:
                    print("请输入正确参数")
            elif user_id == -3:
                tset.addmeau()
            elif user_id == -4:
                tset.delmeau()
            elif user_id >= 0:
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
