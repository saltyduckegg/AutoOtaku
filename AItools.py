from openai import OpenAI
from io import BytesIO
import os
import base64
from PIL import Image


def 鉴(crops):
    base64_image = image_to_base64(crops, format='PNG')
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-vl-max-2025-04-02", # 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages=[
            {
                "role": "system",
                "content": [{"type":"text","text": "You are an expert in analyzing video thumbnails and output structured JSON with fields 'level' and 'tag'. Focus only on image content analysis."}]},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        # 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。"f"是字符串格式化的方法。
                        # PNG图像：  f"data:image/png;base64,{base64_image}"
                        # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
                        # WEBP图像： f"data:image/webp;base64,{base64_image}"
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"}, 
                    },
                    {
                        "type": "text",
                        "text": "请以标准 JSON 格式输出，用于描述图片中“擦边女主播”的擦边等级。要求如下：\n1. 'level' 字段表示等级，取值 1-10，其中 10 代表 100% 确认的擦边女主播，1 代表完全不可能是擦边视频, 大于 6 即为含有擦边元素。\n2. 'tag' 字段包含若干简短标签，用于描述图片的特征，用至少一个tag描述。\n3. tag重点关注性暗示元素和裸漏部位 \n4. 输出必须严格遵守 JSON 格式。\n示例输出：\n{\n  \"level\": 7,\n  \"tag\": [\"性感姿势\", \"低胸衣服\", \"暗示表情\", \"裸漏大腿\"]\n}"
                    },                
                ],
            }
        ],
        response_format={"type": "json_object"},
    )
    return completion.choices[0].message.content

def image_to_base64(img, format='PNG'):
    buffered = BytesIO()
    img.save(buffered, format=format)
    img_bytes = buffered.getvalue()
    base64_str = base64.b64encode(img_bytes).decode('utf-8')
    return base64_str


