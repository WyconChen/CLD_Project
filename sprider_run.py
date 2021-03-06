import threading
from Sprider.Baoyun18 import BaoYun18
from Sprider.Fengqi import FengQi
from Sprider.Niubao100 import Niubao100
from Sprider.Qixin18 import QiXin18
from Sprider.Yisheng import Yisheng
from Sprider.Zhongbao import ZhongBao
import requests
import json

if __name__ == "__main__":
    BaoYun18 = BaoYun18()
    FengQi = FengQi()
    Niubao100 = Niubao100()
    QiXin18 = QiXin18()
    Yisheng = Yisheng()
    ZhongBao = ZhongBao()

    res = requests.post(url="http://120.25.103.152:8002/set_json_data_status_to_1/")
    res_data = json.loads(res.text)
    if res_data["result"]:
        BaoYun18_Thread = threading.Thread(target=BaoYun18.run)
        FengQi_Thread = threading.Thread(target=FengQi.run)
        Niubao100_Thread = threading.Thread(target=Niubao100.run)
        #QiXin18_Thread = threading.Thread(target=QiXin18.run)
        Yisheng_Thread = threading.Thread(target=Yisheng.run)
        ZhongBao_Thread = threading.Thread(target=ZhongBao.run)

        BaoYun18_Thread.start()
        FengQi_Thread.start()
        Niubao100_Thread.start()
        #QiXin18_Thread.start()
        Yisheng_Thread.start()
        ZhongBao_Thread.start()
    else:
        print("爬取前处理数据库失败....")
