import os
from PIL import Image, ImageDraw
import random
import colorsys

def generate_random_color():
    """生成随机的艺术风格颜色"""
    # 使用HSV色彩空间生成更艺术的颜色
    h = random.random()  # 随机色相
    s = 0.7 + random.random() * 0.3  # 较高的饱和度
    v = 0.7 + random.random() * 0.3  # 较高的亮度
    
    # 转换为RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))

def create_vangogh_style():
    """创建梵高风格的预览图像"""
    size = (300, 300)
    img = Image.new('RGB', size, (20, 30, 90))  # 深蓝色背景
    draw = ImageDraw.Draw(img)
    
    # 模拟梵高的星空漩涡效果
    for _ in range(100):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        radius = random.randint(1, 10)
        color = (255, 255, 150)
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)
    
    return img

def create_picasso_style():
    """创建毕加索风格的预览图像"""
    size = (300, 300)
    img = Image.new('RGB', size, (220, 180, 170))  # 米色背景
    draw = ImageDraw.Draw(img)
    
    # 模拟立体派风格
    colors = [(200, 50, 50), (50, 50, 200), (50, 200, 50)]
    
    # 绘制几何形状
    for _ in range(15):
        x1 = random.randint(0, size[0])
        y1 = random.randint(0, size[1])
        x2 = x1 + random.randint(30, 100)
        y2 = y1 + random.randint(30, 100)
        color = random.choice(colors)
        draw.polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], fill=color)
    
    return img

def create_ink_style():
    """创建水墨画风格的预览图像"""
    size = (300, 300)
    img = Image.new('RGB', size, (245, 245, 245))  # 白色背景
    draw = ImageDraw.Draw(img)
    
    # 模拟水墨效果
    for _ in range(50):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        width = random.randint(5, 20)
        height = random.randint(20, 80)
        intensity = random.randint(10, 80)
        color = (intensity, intensity, intensity)
        draw.line([(x, y), (x, y+height)], fill=color, width=width)
    
    return img

def create_impression_style():
    """创建印象派风格的预览图像"""
    size = (300, 300)
    img = Image.new('RGB', size, (150, 200, 255))  # 天蓝色背景
    draw = ImageDraw.Draw(img)
    
    # 模拟印象派点彩效果
    for _ in range(5000):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        radius = random.randint(1, 3)
        color = generate_random_color()
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)
    
    return img

def create_pop_style():
    """创建波普艺术风格的预览图像"""
    size = (300, 300)
    img = Image.new('RGB', size, (255, 255, 0))  # 黄色背景
    draw = ImageDraw.Draw(img)
    
    # 模拟波普艺术的大胆色彩和重复图案
    colors = [(255, 0, 0), (0, 0, 255), (255, 0, 255)]
    
    # 绘制波普风格的点阵
    dot_size = 20
    for x in range(0, size[0], dot_size*2):
        for y in range(0, size[1], dot_size*2):
            color = random.choice(colors)
            draw.ellipse((x, y, x+dot_size, y+dot_size), fill=color)
    
    return img

def create_horror_style():
    """创建恐怖艺术风格的预览图像"""
    size = (300, 300)
    img = Image.new('RGB', size, (10, 10, 10))  # 几乎黑色的背景
    draw = ImageDraw.Draw(img)
    
    # 添加血红色的飞溅效果
    for _ in range(100):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        radius = random.randint(1, 8)
        # 血红色，带有一些变化
        red = 150 + random.randint(0, 105)
        color = (red, random.randint(0, 20), random.randint(0, 20))
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)
    
    # 添加一些不规则裂缝
    for _ in range(15):
        points = []
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        for i in range(random.randint(3, 7)):
            points.append((x + random.randint(-50, 50), y + random.randint(-50, 50)))
        # 灰白色的裂缝
        intensity = random.randint(90, 150)
        color = (intensity, intensity, intensity)
        draw.line(points, fill=color, width=random.randint(1, 3))
    
    return img

def create_candy_style():
    """创建糖果艺术风格的预览图像"""
    size = (300, 300)
    img = Image.new('RGB', size, (255, 200, 220))  # 粉红色背景
    draw = ImageDraw.Draw(img)
    
    # 模拟糖果艺术的鲜艳色彩
    colors = [(255, 50, 150), (100, 200, 255), (255, 255, 100), (150, 255, 150)]
    
    # 创建糖果般的斑点和条纹
    for _ in range(80):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        width = random.randint(5, 20)
        height = random.randint(10, 40)
        color = random.choice(colors)
        if random.random() < 0.5:
            # 圆形糖果斑点
            draw.ellipse((x-width, y-height, x+width, y+height), fill=color)
        else:
            # 漩涡线条 - 修改为使用椭圆而不是arc，以兼容所有版本的Pillow
            for i in range(5):
                r = i * 3
                # 使用椭圆轮廓代替arc，移除width参数
                draw.ellipse((x-r, y-r, x+r, y+r), outline=color)
    
    return img

def create_mosaic_style():
    """创建马赛克艺术风格的预览图像"""
    size = (300, 300)
    img = Image.new('RGB', size, (200, 200, 200))  # 灰色背景
    draw = ImageDraw.Draw(img)
    
    # 创建马赛克方块效果
    block_size = 15
    for x in range(0, size[0], block_size):
        for y in range(0, size[1], block_size):
            color = generate_random_color()
            draw.rectangle((x, y, x+block_size-1, y+block_size-1), fill=color)
    
    return img

def create_rain_princess_style():
    """创建雨公主艺术风格的预览图像"""
    size = (300, 300)
    img = Image.new('RGB', size, (80, 100, 140))  # 蓝灰色背景
    draw = ImageDraw.Draw(img)
    
    # 创建雨效果的垂直线条
    for _ in range(200):
        x = random.randint(0, size[0])
        y1 = random.randint(0, size[1] // 2)
        y2 = y1 + random.randint(10, 50)
        # 淡蓝色的雨线
        intensity = 200 + random.randint(0, 55)
        color = (intensity, intensity, 255)
        width = random.randint(1, 2)
        draw.line([(x, y1), (x, y2)], fill=color, width=width)
    
    # 添加模糊的光晕效果
    for _ in range(10):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        radius = random.randint(10, 30)
        # 柔和的光晕
        color = (220, 220, 255, 100)  # 半透明的淡蓝色
        for r in range(radius, 0, -2):
            alpha = int(100 * (r / radius))
            c = (220, 220, 255, alpha)
            draw.ellipse((x-r, y-r, x+r, y+r), fill=c)
    
    return img

def create_udnie_style():
    """创建Udnie艺术风格的预览图像"""
    size = (300, 300)
    img = Image.new('RGB', size, (170, 150, 120))  # 米褐色背景
    draw = ImageDraw.Draw(img)
    
    # 创建抽象的线条和色块
    colors = [(220, 170, 50), (70, 130, 180), (190, 90, 40)]
    
    # 绘制抽象色块
    for _ in range(20):
        x1 = random.randint(0, size[0])
        y1 = random.randint(0, size[1])
        width = random.randint(30, 80)
        height = random.randint(30, 80)
        color = random.choice(colors)
        # 添加一些透明度
        alpha = random.randint(100, 200)
        c = (*color, alpha)
        draw.rectangle((x1, y1, x1+width, y1+height), fill=c)
    
    # 添加一些动态的线条
    for _ in range(30):
        points = []
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        for i in range(4):
            points.append((x + random.randint(-80, 80), y + random.randint(-80, 80)))
        color = random.choice(colors)
        draw.line(points, fill=color, width=random.randint(2, 5))
    
    return img

def create_style_previews():
    """创建所有风格预览图像"""
    # 确保目录存在
    output_dir = os.path.join('static', 'img', 'styles')
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建并保存所有风格预览图像
    style_creators = {
        'vangogh': create_vangogh_style,
        'picasso': create_picasso_style,
        'ink': create_ink_style,
        'impression': create_impression_style,
        'pop': create_pop_style,
        'horror': create_horror_style,
        'candy': create_candy_style,
        'mosaic': create_mosaic_style,
        'rain-princess': create_rain_princess_style,
        'udnie': create_udnie_style
    }
    
    for style_id, create_func in style_creators.items():
        output_path = os.path.join(output_dir, f'{style_id}.jpg')
        try:
            img = create_func()
            img.save(output_path)
            print(f"创建风格预览图像: {output_path}")
        except Exception as e:
            print(f"创建风格预览图像失败 {style_id}: {e}")
            # 创建一个简单的彩色矩形作为替代
            simple_img = Image.new('RGB', (300, 300), generate_random_color())
            simple_img.save(output_path)
            print(f"创建简单替代图像: {output_path}")

if __name__ == "__main__":
    create_style_previews()
