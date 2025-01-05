from PIL import Image, ImageDraw, ImageFont
import os

def get_display_text(name):
    """获取要显示的文本"""
    name_map = {
        'chatgpt': 'GPT',
        'claude': 'CLD',
        'bard': 'BARD',
        'perplexity': 'PPX',
        'character': 'CHR',
        'youchat': 'YOU',
        'copilot': 'COP',
        'cursor': 'CUR',
        'codewhisperer': 'CW',
        'tabnine': 'TAB',
        'replit': 'RPL',
        'codegeex': 'CGX',
        'codeium': 'CDM',
        'midjourney': 'MJ',
        'dalle': 'DALL',
        'stable-diffusion': 'SD',
        'leonardo': 'LEO',
        'canva': 'CNV',
        'firefly': 'FF',
        'bing-image': 'BING',
        'runway': 'RUN',
        'synthesia': 'SYN',
        'pika': 'PIKA',
        'heygen': 'HEY',
        'descript': 'DESC',
        'kapwing': 'KAP',
        'beautiful': 'BTF',
        'gamma': 'GAM',
        'slidesai': 'SAI',
        'tome': 'TOME',
        'pitch': 'PTCH'
    }
    return name_map.get(name, name[:3].upper())

def create_logo(name, color, size=256):
    padding = 4
    total_size = size + padding * 2
    image = Image.new('RGBA', (total_size, total_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (255,)
    
    # 创建渐变色
    bg_color = hex_to_rgb(color)
    darker_color = tuple(int(c * 0.7) for c in bg_color[:3]) + (bg_color[3],)  # 30% darker
    lighter_color = tuple(min(int(c * 1.2), 255) for c in bg_color[:3]) + (bg_color[3],)  # 20% lighter
    
    corner_radius = size // 6
    
    def create_gradient_background(base_offset=0):
        # 创建渐变背景
        gradient = Image.new('RGBA', (total_size, total_size), (0, 0, 0, 0))
        gradient_draw = ImageDraw.Draw(gradient)
        
        # 创建从左上到右下的渐变效果
        for i in range(total_size):
            # 计算渐变进度
            progress = i / total_size
            if progress < 0.5:
                # 上半部分使用亮色到主色的渐变
                ratio = progress * 2
                current_color = tuple(
                    int(l * (1 - ratio) + m * ratio)
                    for l, m in zip(lighter_color[:3], bg_color[:3])
                ) + (bg_color[3],)
            else:
                # 下半部分使用主色到暗色的渐变
                ratio = (progress - 0.5) * 2
                current_color = tuple(
                    int(m * (1 - ratio) + d * ratio)
                    for m, d in zip(bg_color[:3], darker_color[:3])
                ) + (bg_color[3],)
            
            # 绘制渐变线
            gradient_draw.line([(0, i + base_offset), (total_size, i + base_offset)], 
                             fill=current_color)
        
        return gradient
    
    # 创建立体效果
    def draw_rounded_rect_with_depth():
        # 绘制底部阴影
        shadow_offset = 8
        shadow_color = (0, 0, 0, 50)
        draw_rounded_rect(shadow_offset, shadow_offset, shadow_color)
        
        # 绘制主体渐变背景
        gradient = create_gradient_background()
        
        # 创建遮罩用于圆角
        mask = Image.new('L', (total_size, total_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        draw_rounded_rect(0, 0, 255, mask_draw)
        
        # 应用遮罩到渐变背景
        image.paste(gradient, (0, 0), mask)
        
        # 添加顶部高光
        highlight = Image.new('RGBA', (total_size, total_size), (0, 0, 0, 0))
        highlight_draw = ImageDraw.Draw(highlight)
        
        # 绘制顶部渐变高光
        for i in range(total_size // 3):
            alpha = int(255 * (1 - i / (total_size // 3)) * 0.3)
            highlight_color = (*lighter_color[:3], alpha)
            highlight_draw.line([(0, i), (total_size, i)], fill=highlight_color)
        
        # 应用高光
        image.alpha_composite(highlight)
        
        # 添加边缘光效
        edge_light = Image.new('RGBA', (total_size, total_size), (0, 0, 0, 0))
        edge_draw = ImageDraw.Draw(edge_light)
        edge_width = 2
        edge_color = (*lighter_color[:3], 100)
        draw_rounded_rect(edge_width, edge_width, edge_color, edge_draw)
        image.alpha_composite(edge_light)
    
    def draw_rounded_rect(x_offset, y_offset, color, target_draw=draw):
        target_draw.rectangle([corner_radius + x_offset, y_offset, 
                               total_size - corner_radius - padding + x_offset, total_size - padding], 
                               fill=color)
        target_draw.rectangle([x_offset, corner_radius + y_offset, 
                               total_size - padding + x_offset, total_size - corner_radius - padding], 
                               fill=color)
        target_draw.pieslice([x_offset, y_offset, 
                              corner_radius * 2 + x_offset, corner_radius * 2 + y_offset], 
                              180, 270, fill=color)
        target_draw.pieslice([total_size - corner_radius * 2 - padding + x_offset, y_offset, 
                              total_size - padding + x_offset, corner_radius * 2 + y_offset], 
                              270, 360, fill=color)
        target_draw.pieslice([x_offset, total_size - corner_radius * 2 - padding, 
                              corner_radius * 2 + x_offset, total_size - padding], 
                              90, 180, fill=color)
        target_draw.pieslice([total_size - corner_radius * 2 - padding + x_offset, 
                              total_size - corner_radius * 2 - padding, 
                              total_size - padding + x_offset, total_size - padding], 
                              0, 90, fill=color)
    
    # 绘制立体背景
    draw_rounded_rect_with_depth()
    
    # 文字处理
    text = get_display_text(name)
    font_paths = [
        # macOS 字体
        "/System/Library/Fonts/SFPro-Bold.ttf",
        "/System/Library/Fonts/HelveticaNeue-Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/Library/Fonts/Arial.ttf",
        
        # Windows 字体
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        
        # Linux 字体
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        
        # 通用路径
        "arial.ttf",
        "Arial.ttf",
        "DejaVuSans.ttf"
    ]
    
    # 计算初始字体大小
    initial_size = int(size * 0.5)
    print(f"\n{'='*50}")
    print(f"Generating logo for {name}:")
    print(f"Text to display: {text}")
    print(f"Initial font size: {initial_size}px")
    
    # 尝试加载字体
    font = None
    used_font_path = None
    
    for path in font_paths:
        try:
            font = ImageFont.truetype(path, initial_size)
            used_font_path = path
            print(f"Using font: {os.path.basename(path)}")
            break
        except (OSError, IOError):
            continue
    
    # 如果所有字体都失败，使用默认字体
    if font is None:
        try:
            # 尝试使用系统默认字体
            font = ImageFont.load_default()
            print("Warning: Using default font")
        except:
            # 如果默认字体也失败，尝试使用系统Arial字体
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", initial_size)
                print("Warning: Using Arial font")
            except:
                # 如果Arial也失败，使用默认字体并降低字号
                font = ImageFont.load_default()
                initial_size = int(initial_size * 0.5)  # 降低字号以适应默认字体
                print("Warning: Using default font with reduced size")
    
    # 调整字体大小的代码
    def adjust_font_size(size):
        nonlocal font, used_font_path
        try:
            if used_font_path:
                return ImageFont.truetype(used_font_path, size)
            # 如果没有可用的字体文件，使用默认字体
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()
    
    # 调整字体大小
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # 调整目标尺寸 - 让文字更大，更居中
    target_width = size * 0.95   # 允许宽度达到95%
    target_height = size * 0.7   # 增大高度占比到70%
    
    print(f"Initial text dimensions: {text_width}x{text_height}px")
    print(f"Target dimensions: {target_width}x{target_height}px")
    
    # 如果文字太大，逐步缩小
    while (text_width > target_width or text_height > target_height) and initial_size > 10:
        initial_size -= 2
        font = adjust_font_size(initial_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    
    # 如果文字太小，逐步放大
    while (text_width < target_width * 0.8 and text_height < target_height * 0.8) and initial_size < size:
        initial_size += 2
        font = adjust_font_size(initial_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    
    # 计算填充比例
    width_ratio = text_width / size
    height_ratio = text_height / size
    
    print(f"\nFinal Results:")
    print(f"- Font size: {initial_size}px ({initial_size/size:.1%} of icon size)")
    print(f"- Text dimensions: {text_width}x{text_height}px")
    print(f"- Fill ratios: Width {width_ratio:.1%}, Height {height_ratio:.1%}")
    
    # 调整文字渲染效果
    def draw_text_with_effects(x, y, text, font, main_color='white'):
        # 添加深度阴影
        shadow_color = (0, 0, 0, 60)
        shadow_offset = 6
        for i in range(3):
            offset = shadow_offset - i
            alpha = int(60 * (1 - i/3))
            current_shadow = (*shadow_color[:3], alpha)
            draw.text((x + offset, y + offset), text, 
                     font=font, fill=current_shadow)
        
        # 绘制主文字描边
        outline_color = darker_color
        outline_width = 3
        for offset_x in range(-outline_width, outline_width + 1):
            for offset_y in range(-outline_width, outline_width + 1):
                if offset_x != 0 or offset_y != 0:
                    draw.text((x + offset_x, y + offset_y), 
                            text, font=font, fill=outline_color)
        
        # 绘制主文字 - 使用更亮的颜色
        main_text_color = (255, 255, 255)  # 纯白色
        draw.text((x, y), text, font=font, fill=main_text_color)
        
        # 添加顶部高光 - 增强亮度
        highlight_color = (255, 255, 255, 140)  # 更亮的高光
        draw.text((x, y-1), text, font=font, fill=highlight_color)
        
        # 添加额外的光泽效果
        glow_color = (255, 255, 255, 30)  # 柔和的光晕
        for offset in range(1, 3):
            draw.text((x, y-offset), text, font=font, fill=glow_color)
    
    # 精确计算文字位置以确保居中
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # 计算精确的居中位置，并上移10px
    x = (total_size - text_width) / 2
    y = (total_size - text_height) / 2 - 10  # 上移10px
    
    # 添加阴影效果 - 调整阴影位置
    shadow_offset = 4
    shadow_color = (0, 0, 0, 70)  # 稍微加深阴影
    draw.text((x + shadow_offset, y + shadow_offset), 
             text, font=font, fill=shadow_color)
    
    # 绘制带效果的文字
    draw_text_with_effects(x, y, text, font)
    
    # 裁剪到原始尺寸
    final_image = image.crop((padding, padding, total_size - padding, total_size - padding))
    
    # 保存图片
    filename = f'images/logos/{name}.png'
    final_image.save(filename, 'PNG')
    print(f"Saved: {filename}")
    print(f"{'='*50}")

# 更新工具列表，添加更多品牌色
TOOLS = {
    # 聊天对话类
    'chatgpt': '#10a37f',  # OpenAI绿色
    'claude': '#7c3aed',   # 紫色
    'bard': '#4285f4',     # Google蓝色
    'perplexity': '#00a4dc',
    'character': '#ff6b6b',
    'pi': '#38bdf8',
    'youchat': '#2563eb',
    'poe': '#6366f1',
    
    # 编程开发类
    'copilot': '#238636',  # GitHub绿色
    'cursor': '#0ea5e9',
    'codewhisperer': '#ff9900',  # AWS橙色
    'tabnine': '#6b7280',
    'replit': '#f97316',
    'codegeex': '#22c55e',
    'codeium': '#3b82f6',
    
    # 图像生成类
    'midjourney': '#0284c7',
    'dalle': '#10b981',
    'stable-diffusion': '#818cf8',
    'leonardo': '#f43f5e',
    'canva': '#06b6d4',
    'firefly': '#0ea5e9',
    'bing-image': '#0ea5e9',
    
    # 视频生成类
    'runway': '#8b5cf6',
    'synthesia': '#f59e0b',
    'pika': '#ec4899',
    'did': '#6366f1',
    'heygen': '#14b8a6',
    'descript': '#f43f5e',
    'kapwing': '#f97316',
    
    # PPT生成类
    'beautiful': '#0ea5e9',
    'gamma': '#8b5cf6',
    'slidesai': '#f97316',
    'tome': '#22c55e',
    'pitch': '#3b82f6'
}

def main():
    if not os.path.exists('images/logos'):
        os.makedirs('images/logos')
    
    for name, color in TOOLS.items():
        create_logo(name, color)
    print(f'Generated {len(TOOLS)} logos in images/logos directory')

if __name__ == '__main__':
    main() 