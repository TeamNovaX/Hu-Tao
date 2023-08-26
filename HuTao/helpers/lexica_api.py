# Copyright 2023 Qewertyy, MIT License

import httpx, base64,os
from typing import Union, List, Dict
from HuTao import LEXICA_API

async def UpscaleImages(image: bytes) -> str:
    """
    Upscales an image and return with upscaled image path.
    """
    try:
        b = base64.b64encode(image).decode("utf-8")
        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(
                f"{LEXICA_API}/upscale",
                data={"image_data": b},
                timeout=None,
            )
        if response.status_code == 200:
            upscaled_file_path = "upscaled.png"
            with open(upscaled_file_path, "wb") as output_file:
                output_file.write(response.content)
            return upscaled_file_path
        else:
            return None
    except Exception as e:
        raise Exception(f"Failed to upscale the image: {e}")
