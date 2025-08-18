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

def is_similar_to_4_3(box_str, tol=0.05):
    """
    Check if a bounding box ratio is similar to 4:3.
    
    Args:
        box_str (str): string like '[548,966][1065,1353]'
        tol (float): tolerance for similarity, default ±0.05
    
    Returns:
        ratio (float), is_similar (bool)
    """
    # Extract numbers
    #import re
    nums = list(map(int, re.findall(r"\d+", box_str)))
    if len(nums) != 4:
        raise ValueError("Input must contain 4 numbers like [x1,y1][x2,y2]")
    
    x1, y1, x2, y2 = nums
    width = x2 - x1
    height = y2 - y1
    box=(x1, y1, x2, y2)
    if height == 0:
        raise ValueError("Height is zero, invalid box")
    
    ratio = width / height
    target = 4 / 3
    
    return box, abs(ratio - target) <= tol