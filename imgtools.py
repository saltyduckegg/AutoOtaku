from PIL import Image
import numpy as np
import time


#裁剪图片
def img_crop(image, box):
    return image.crop(box)





def calculate_mse(image1, image2):
    """
    计算两张图片的均方误差 (MSE)
    """
    img1 = np.array(image1)
    img2 = np.array(image2)
    
    # 确保两张图片的大小相同
    if img1.shape != img2.shape:
        print(f"图片1大小: {img1.shape}")
        print(f"图片2大小: {img2.shape}")
        raise ValueError("图片大小不一致，无法计算 MSE。")
    
    # 计算均方误差
    mse = np.mean((img1 - img2) ** 2)
    return mse

def are_images_similar_mse(image1, image2, threshold=1000):
    """
    根据 MSE 判断两张图片是否相似。
    threshold: MSE 阈值，低于该值则认为图片相似。
    """
    mse = calculate_mse(image1, image2)
    print(f"MSE: {mse}")
    
    if mse < threshold:
        return True
    else:
        return False
    
def are_images_humandetermin_similar_mse(image1, image2, threshold=1000):
    """
    根据 MSE 判断两张图片是否相似。
    threshold: MSE 阈值，低于该值则认为图片相似。
    """
    mse = calculate_mse(image1, image2)
    print(f"MSE: {mse}")
    
    if mse < threshold:
        return True
    else:
        #如果不相似，就显示两张图片 并等待人工判断 y or n
                # 获取当前时间戳作为文件名前缀
        timestamp = int(time.time())  # 获取当前时间戳，单位为秒
        
        # 创建以时间戳为前缀的文件名
        image1_filename = fr"D:\mypythonpipline\20241230\log\image1_{timestamp}.png"
        image2_filename = fr"D:\mypythonpipline\20241230\log\image2_{timestamp}.png"
        
        # 保存图像文件
        image1.save(image1_filename)
        image2.save(image2_filename)
        
        print(f"Images saved as {image1_filename} and {image2_filename}")

        return input("是否相似？(y/n)") == 'y'
        #return False

    
def box2center(box):
    """
    将 box 转换为中心坐标
    """
    x1, y1, x2, y2 = box
    return (x1 + x2) / 2, (y1 + y2) / 2