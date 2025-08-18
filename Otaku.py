import argparse
from adbtools_win import Adbtools
import numpy as np
from OtakuTools import is_similar_to_4_3
import time
from AItools import 鉴
import json
from datetime import datetime

from imgtools import img_crop
from lxml import etree




parser = argparse.ArgumentParser(description="通过命令行传入设备的MAC地址")
parser.add_argument("--mac",default="1ab4919e" , help="设备的MAC地址")
parser.add_argument("--host", default="localhost", help="设备的IP地址 (默认: localhost)")
parser.add_argument("--port", type=int, default=16449, help="ADB端口 (默认: 16449)")
parser.add_argument("--adb_path", default=r'D:\安卓工具\platform-tools-latest-windows\platform-tools\adb.exe',
                    help="ADB工具路径 (默认: 指定的路径)")

args = parser.parse_args()

# 使用解析的参数
host = args.host
port = args.port
adb_path = args.adb_path
mac = args.mac  # 从命令行传入的MAC地址


def main():
    adb = Adbtools(adb_path, host, port, mac)
    adb.adb_swipe_raw(500,500,500,1500, 500)
    time.sleep(4)
    try:
        coverdetil_list=[]
        #xml_str=adb.get_uixml_via_stdout()
        img = adb.adb_screencap_raw()
        time.sleep(2)
        xml_str= adb.get_uixml_via_stdout()
        root = etree.fromstring(xml_str.encode("utf-8"))
        for i, child in enumerate(reversed(root.xpath("./node[1]/node[1]/node[1]/node[1]/node[1]/node[1]/node[1]/node[1]/node[3]/node[1]/node[2]/node[1]/node[1]/node[1]/node[1]/node"))):
            for child_children in child.xpath("./node[1]/node[1]"):
                if child_children.attrib.get("class") != "android.widget.ImageView":
                    continue
                boxdetail=is_similar_to_4_3(child_children.attrib.get("bounds"))
                if boxdetail[1] == False:
                    continue
                print(boxdetail[0])
                cover_dict={}
                cover_dict['box'] = boxdetail[0]
                cover_dict['vidio_class'] = child.attrib.get("content-desc").split(',')[0]
                cover_dict['vidio_title'] = child.attrib.get("content-desc")
                cover_dict['cover'] = img_crop(img, boxdetail[0])
                coverdetil_list.append(cover_dict)
    except :
        print("获取UI XML或截图失败")
        return 0
    for coverdetil in coverdetil_list:
        #box = coverdetil['box']
        cover = coverdetil['cover']
        # 处理提取的封面
        try:
            json_str =鉴(cover)
            data = json.loads(json_str)
            keys = list(data.keys())
            level = data[keys[0]]
            anno = json.dumps(data[keys[1]], ensure_ascii=False)
            print(f"封面等级: {level}, 注释: {anno}")
        except (IndexError, KeyError, json.JSONDecodeError) as e:
            print(f"跳过有问题的json，错误：{e}")
            continue  # 跳过本次循环，进入下一个
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        png_filename = f"data/images/{timestamp}.png"
        anno_filename = f"data/anno/{timestamp}.txt"
        label_filename = f"data/label/{timestamp}.txt"
        with open(anno_filename, "w", encoding="utf-8") as f:
            f.write(anno)
        with open(label_filename, "w", encoding="utf-8") as f:
            f.write(str(level))
        cover.save(png_filename)
        if int(level) >= 7:
            height_png_filename = f"high_level_data/{timestamp}.png"
            cover.save(height_png_filename)
            print(f"高危封面已保存: {height_png_filename}")
    return 1

while True:
    main()
    print("处理完成")
    
