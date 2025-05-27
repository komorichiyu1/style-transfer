import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random
import colorsys
import math

def create_vangogh_preview(size=(300, 300)):
    """创建梵高星空风格的预览图像"""
    # 创建深蓝色背景
    img = Image.new('RGB', size, color=(20, 30, 90))
    draw = ImageDraw.Draw(img)
    
    # 绘制漩涡星空
    for i in range(100):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        radius = random.randint(2, 8)
        brightness = random.randint(180, 255)
        color = (brightness, brightness, random.randint(100, 180))
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)
    
    # 绘制漩涡效果 - 修改为使用多个同心椭圆而不是arc
    for angle in range(0, 360, 10):
        center_x, center_y = size[0]//2, size[1]//2
        for r in range(10, 100, 5):
            rad = math.radians(angle)
            x = center_x + int(r * math.cos(rad))
            y = center_y + int(r * math.sin(rad))
            width = random.randint(2, 5)
            # 使用椭圆轮廓代替arc，移除width参数
            # 使用多个略微偏移的椭圆来模拟宽度
            for w in range(width):
                draw.ellipse((center_x-r+w, center_y-r+w, center_x+r-w, center_y+r-w), 
                             outline=(255, 255, 200))
    
    # 模拟梵高的笔触
    img = img.filter(ImageFilter.CONTOUR)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    
    return img

def create_picasso_preview(size=(300, 300)):
    """创建毕加索立体派风格的预览图像"""
    img = Image.new('RGB', size, color=(240, 220, 200))
    draw = ImageDraw.Draw(img)
    
    # 立体派特征：多角度视图、几何分割
    colors = [(220, 100, 50), (50, 100, 180), (240, 200, 80), (60, 180, 140)]
    
    # 绘制几何形状分割
    for _ in range(20):
        x1 = random.randint(0, size[0])
        y1 = random.randint(0, size[1])
        x2 = random.randint(0, size[0])
        y2 = random.randint(0, size[1])
        x3 = random.randint(0, size[0])
        y3 = random.randint(0, size[1])
        color = random.choice(colors)
        draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=color)
    
    # 添加立体派典型的脸部轮廓
    eye_x, eye_y = size[0]//3, size[1]//3
    draw.ellipse((eye_x-15, eye_y-15, eye_x+15, eye_y+15), fill=(0, 0, 0))
    draw.ellipse((eye_x*2-15, eye_y-15, eye_x*2+15, eye_y+15), fill=(0, 0, 0))
    draw.polygon([(size[0]//2, size[1]//2), (size[0]//3, size[1]*2//3), (size[0]*2//3, size[1]*2//3)], fill=(180, 100, 80))
    
    # 添加边缘线条
    img = img.filter(ImageFilter.FIND_EDGES)
    img = img.filter(ImageFilter.EDGE_ENHANCE)
    
    return img

def create_ink_preview(size=(300, 300)):
    """创建水墨画风格的预览图像"""
    img = Image.new('RGB', size, color=(245, 245, 245))
    draw = ImageDraw.Draw(img)
    
    # 绘制水墨画效果
    for _ in range(8):
        # 垂直笔触
        x = random.randint(size[0]//4, size[0]*3//4)
        y_start = random.randint(20, size[1]//3)
        y_end = random.randint(size[1]*2//3, size[1]-20)
        width = random.randint(5, 15)
        intensity = random.randint(30, 80)
        color = (intensity, intensity, intensity)
        draw.line([(x, y_start), (x, y_end)], fill=color, width=width)
        
        # 添加树枝效果
        branch_count = random.randint(2, 5)
        for i in range(branch_count):
            branch_y = random.randint(y_start, y_end)
            branch_length = random.randint(20, 50)
            branch_width = max(1, width // 2)
            branch_direction = 1 if random.random() > 0.5 else -1
            draw.line([(x, branch_y), (x + branch_length * branch_direction, branch_y - random.randint(5, 20))], 
                      fill=color, width=branch_width)
    
    # 转换为黑白效果并增强对比度
    img = img.convert('L').convert('RGB')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.8)
    
    return img

def create_impression_preview(size=(300, 300)):
    """创建印象派风格的预览图像"""
    # 创建天空和水面的基本背景
    img = Image.new('RGB', size, color=(180, 210, 240))
    draw = ImageDraw.Draw(img)
    
    # 绘制水面
    for y in range(size[1]//2, size[1], 2):
        for x in range(0, size[0], 4):
            blue_var = random.randint(-20, 20)
            color = (100 + blue_var, 140 + blue_var, 220 + blue_var)
            width = random.randint(2, 6)
            draw.line([(x, y), (x + width, y)], fill=color)
    
    # 添加印象派特有的点彩效果
    for _ in range(3000):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        r = random.randint(1, 3)
        
        # 上半部分为天空
        if y < size[1] // 2:
            # 天空颜色变化
            red = random.randint(180, 240)
            green = random.randint(200, 250)
            blue = random.randint(220, 255)
        else:
            # 水面颜色变化
            red = random.randint(80, 150)
            green = random.randint(120, 180)
            blue = random.randint(180, 240)
        
        color = (red, green, blue)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=color)
    
    # 柔化图像
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    
    return img

def create_pop_preview(size=(300, 300)):
    """创建波普艺术风格的预览图像"""
    img = Image.new('RGB', size, color=(255, 240, 0))
    draw = ImageDraw.Draw(img)
    
    # 添加波普艺术的典型网点效果
    colors = [(255, 0, 0), (0, 0, 255), (255, 0, 255), (0, 200, 0)]
    
    # 创建网格网点
    grid_size = 20
    for x in range(0, size[0], grid_size):
        for y in range(0, size[1], grid_size):
            if random.random() > 0.3:  # 70%的格子有点
                color = random.choice(colors)
                dot_size = random.randint(grid_size//3, grid_size-2)
                draw.ellipse((x+(grid_size-dot_size)//2, y+(grid_size-dot_size)//2, 
                              x+(grid_size+dot_size)//2, y+(grid_size+dot_size)//2), 
                             fill=color)
    
    # 添加典型的波普艺术线条
    for _ in range(5):
        x = random.randint(0, size[0])
        width = random.randint(5, 15)
        draw.line([(x, 0), (x, size[1])], fill=(0, 0, 0), width=width)
    
    for _ in range(5):
        y = random.randint(0, size[1])
        width = random.randint(5, 15)
        draw.line([(0, y), (size[0], y)], fill=(0, 0, 0), width=width)
    
    # 增强色彩饱和度
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.5)
    
    return img

def add_style_text(img, style_name):
    """在风格预览图像上添加样式名称文字"""
    draw = ImageDraw.Draw(img)
    size = img.size
    
    try:
        # 尝试加载字体，如果失败则使用默认字体
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # 获取文本尺寸
    try:
        # 新版本PIL使用textbbox获取文本尺寸
        left, top, right, bottom = draw.textbbox((0, 0), style_name, font=font)
        text_width = right - left
        text_height = bottom - top
    except AttributeError:
        # 如果没有textbbox，尝试使用textlength
        try:
            text_width = draw.textlength(style_name, font=font)
            text_height = font.getsize(style_name)[1]  # 尝试通过字体获取高度
        except (AttributeError, TypeError):
            # 如果所有方法都失败，使用估计值
            text_width = len(style_name) * 12
            text_height = 24
    
    # 创建文本背景
    text_bg_left = (size[0] - text_width) // 2 - 5
    text_bg_top = size[1] - text_height - 25
    text_bg_right = text_bg_left + text_width + 10
    text_bg_bottom = text_bg_top + text_height + 10
    
    # 绘制半透明文本背景
    draw.rectangle((text_bg_left, text_bg_top, text_bg_right, text_bg_bottom), 
                   fill=(0, 0, 0, 128))
    
    # 绘制文本
    position = ((size[0] - text_width) // 2, text_bg_top + 5)
    draw.text(position, style_name, fill=(255, 255, 255), font=font)
    
    return img

def create_style_preview(style_name, output_path, size=(300, 300)):
    """创建风格预览图像"""
    # 根据风格名称选择不同的预览生成函数
    style_id = output_path.split('/')[-1].split('.')[0]  # 从路径获取风格ID
    
    if style_id == 'vangogh':
        img = create_vangogh_preview(size)
    elif style_id == 'picasso':
        img = create_picasso_preview(size)
    elif style_id == 'ink':
        img = create_ink_preview(size)
    elif style_id == 'impression':
        img = create_impression_preview(size)
    elif style_id == 'pop':
        img = create_pop_preview(size)
    else:
        # 默认创建随机背景色
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        img = Image.new('RGB', size, color=(r, g, b))
    
    # 添加风格名称文字
    img = add_style_text(img, style_name)
    
    # 保存图像
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    
    return output_path

def create_all_style_previews():
    """创建所有风格预览图像"""
    styles = {
        'vangogh': '梵高星空',
        'picasso': '毕加索立体派',
        'ink': '水墨画',
        'impression': '印象派',
        'pop': '波普艺术'
    }
    
    for style_id, style_name in styles.items():
        output_path = os.path.join('static', 'img', 'styles', f'{style_id}.jpg')
        create_style_preview(style_name, output_path)
        print(f"Created style preview for {style_name} at {output_path}")

if __name__ == "__main__":
    create_all_style_previews()
