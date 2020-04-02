import requests
import json
import sys
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8"
} #设置头文件，伪装请求为谷歌访问


class DD_xinxi():

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

    def NekoMoeK(self):
        return self.get_xinxi(67642150)

    def lunai(self):
        return self.get_xinxi(316381099)

    def aqua(self):
        return self.get_xinxi(375504219)

    def mea(self):
        return self.get_xinxi(349991143)

    def pekora(self):
        return self.get_xinxi(443305053)

    def lvzongzi(self):
        return self.get_xinxi(443300418)

    def miaomiaohu(self):
        return self.get_xinxi(332704117)

    def kanata(self):
        return self.get_xinxi(491474048)

    def qita(self):
        user_set_uid = input("请输入查询uid：")
        return self.get_xinxi(user_set_uid)

def main(): #驱动程序
    userinset = {
            1:"NekoMoeK",
            2:"鹿乃",
            3:"阿夸",
            4:"mea",
            5:"烤兔",
            6:"绿粽子",
            7:"喵喵狐",
            8:"天哥",
            9:"其他",
            10:"菜单",
            0:"退出",
     } #目录系统

    DDretrun = DD_xinxi()
    print("="*8+"欢迎使用DD"+"="*8) #欢迎语

    for key,value in userinset.items():
        print(str(key)+"\t\t"+value) #打印目录
    print("="*27)
    print("\n请选择相应的预选服务：\n")
    while True: #主系统
        try:
            userDD = int(input("DD> ")) #输入对应数字，对应数据
        except Exception:
            print("输入错误，请输入正确参数")
            continue
        except KeyboardInterrupt:
            print("欢迎下次使用")
            sys.exit(0)
        try:
            if userDD == 1:
                print("="*20)
                for key,value in DDretrun.NekoMoeK().items():
                    print(str(key)+": "+str(value))
                print("="*20)
                continue
            elif userDD == 2:
                print("="*20)
                for key,value in DDretrun.lunai().items():
                    print(str(key)+": "+str(value))
                print("="*20)
                continue
            elif userDD == 3:
                print("="*20)
                for key,value in DDretrun.aqua().items():
                    print(str(key)+": "+str(value))
                print("="*20)
                continue
            elif userDD == 4:
                print("="*20)
                for key,value in DDretrun.mea().items():
                    print(str(key)+": "+str(value))
                print("="*20)
                continue
            elif userDD == 5:
                print("="*20)
                for key,value in DDretrun.pekora().items():
                    print(str(key)+": "+str(value))
                print("="*20)
                continue
            elif userDD == 6:
                print("="*20)
                for key,value in DDretrun.lvzongzi().items():
                    print(str(key)+": "+str(value))
                print("="*20)
                continue
            elif userDD == 7:
                print("="*20)
                for key,value in DDretrun.miaomiaohu().items():
                    print(str(key)+": "+str(value))
                print("="*20)
                continue
            elif userDD == 8:
                print("="*20)
                for key,value in DDretrun.kanata().items():
                    print(str(key)+": "+str(value))
                print("="*20)
                continue
            elif userDD == 9:
                print("="*20)
                for key,value in DDretrun.qita().items():
                    print(str(key)+": "+str(value))
                print("="*20)
                continue
            elif userDD == 10:
                print("="*8+"欢迎使用DD"+"="*8) #欢迎语
                for key,value in userinset.items():
                    print(str(key)+"\t\t"+value) #打印目录
                print("="*27)
            elif userDD == 0:
                print("欢迎下次使用")
                sys.exit(0)
            else:
                print("\n目前数字操作未添加功能，请确认现有目录内容\n")
        except Exception:
            print("输入错误，请输入正确参数")
            continue


if __name__ == "__main__":

    main()