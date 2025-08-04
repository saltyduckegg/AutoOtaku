import argparse
from adbtools_win import Adbtools
import numpy as np
from OtakuTools import find_video_covers, extract_covers
import time
from AItools import 鉴黄
import json
from datetime import datetime

from imgtools import img_crop




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
    time.sleep(2)
    try:
        xml_str=adb.get_uixml_via_stdout()
        img = adb.adb_screencap_raw()
        boxes = find_video_covers(xml_str)
    except :
        print("获取UI XML或截图失败")
        return 0
    for box in boxes:

        x1, y1, x2, y2 = box
        width = x2 - x1
        height = y2 - y1
        # 如果高度约等于宽度的0.5倍，则跳过
        if (height - 0.5 * width) < 0:
            continue  # 跳过这个 box，处理下一个
        cover = img_crop(img, box)
        # 处理提取的封面
        
        try:
            json_str =鉴黄(cover)
            data = json.loads(json_str)
            keys = list(data.keys())
            level = data[keys[0]]
            anno = json.dumps(data[keys[1]], ensure_ascii=False)
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
        if level >= 7:
            height_png_filename = f"high_level_data/{timestamp}.png"
            cover.save(height_png_filename)
            print(f"高危封面已保存: {height_png_filename}")
    return 1

while True:
    main()
    print("处理完成")
    
