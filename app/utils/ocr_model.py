from openai import OpenAI
from io import BytesIO
from base64 import b64encode
from json import loads

class OCRModel():
    def __init__(self, api_url, api_key, model):
        self.api_url = api_url
        self.api_key = api_key
        self.model = model

    def __pil_to_base64(self, pil_img, format="PNG"):
        buffered = BytesIO()
        pil_img.save(buffered, format=format)  # 保存图像到内存缓冲区
        img_bytes = buffered.getvalue()
        return "data:image/png;base64," + b64encode(img_bytes).decode("utf-8")  # 编码为Base64字符串

    def predict(self, img):
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_url,
        )

        completion = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "你是一个图片分析专家，请判断图片中是否是一个公式，如果是，则返回公式的标准的Latex格式，只输出最终的结果，请你以JSON格式输出，具体的返回格式为：{\"formula\"：\"yes/no\", \"content\": \"空/具体的Latex\"}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": self.__pil_to_base64(img)
                            }
                        }
                    ]
                },
            ],
        )
        status = -1
        message = "ocr failed"
        if len(completion.choices) >= 1:
            status = 0
            res_filter = completion.choices[0].message.content.lstrip("```json").rstrip("```")
            message = completion.choices[0].message
        return status, message, res_filter