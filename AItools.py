from openai import OpenAI
from io import BytesIO
import os
import base64
from PIL import Image


def 鉴黄(crops):
    base64_image = image_to_base64(crops, format='PNG')
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-vl-max-latest", # 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages=[
            {
                "role": "system",
                "content": [{"type":"text","text": "You are a helpful assistant."}]},
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
                    {"type": "text", "text": "以标准的json格式输出用于描述图片擦边女主播等级，分为10个等级，为10级为100%确认的擦边女主播，1级为完全不是。的简短tag"},
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


