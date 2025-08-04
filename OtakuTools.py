import xml.etree.ElementTree as ET
import re
from imgtools import img_crop

def find_video_covers(xml_str):
    def parse_bounds(bounds_str):
        nums = list(map(int, re.findall(r'\d+', bounds_str)))
        return tuple(nums)  # (x1, y1, x2, y2)

    root = ET.fromstring(xml_str)
    boxes = []

    for node in root.iter('node'):
        if node.attrib.get('class') == 'android.widget.ImageView':
            if node.attrib.get('resource-id') == 'tv.danmaku.bili:id/cover':
                bounds = node.attrib.get('bounds')
                if bounds:
                    box = parse_bounds(bounds)
                    boxes.append(box)
    return boxes

def extract_covers(img, boxes):
    crops = []
    for box in boxes:
        crop = img_crop(img, box)
        crops.append(crop)
    return crops

