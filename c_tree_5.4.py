import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# 2.0 增加螺旋光带。
# 3.0 增加树顶灯球。
# 4.0 增加雪地，降低转速。
# 4.1 改变颜色。
# 4.2 圣诞树主体增加更大、透明度更低的灯球粒子。
# 5.0 增加文字Merry Christmas。更适配7s电脑的全屏视图。
    # 5.1 全屏视图。好看，但运行前后屏幕会异常，不建议使用。
    # 5.2 树顶灯球改为四芒星（但不好看）。
# 5.3 增加鼠标拖动视角功能。
# 5.4 改变文字为from 祁殳 to xxx Merry Christmas。粒子数量10750。

# 初始化pygame
pygame.init()
display = (1440, 840)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# 设置投影矩阵
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0) 

# 设置模型视图矩阵
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glTranslatef(0.0, -2, -7)  # 将相机向下向后移动一些，确保能看到整个树

# 启用点平滑和深度测试
glEnable(GL_POINT_SMOOTH)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)  # 启用混合以实现透明度
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # 设置混合函数
glPointSize(2.0)

# 创建文字对象（改）
font = pygame.font.SysFont('simsun', 36, italic=True)  # 宋体，字号36，斜体
line1_surface = font.render('from 7s to xxx', True, (255, 255, 255))
line2_surface = font.render('Merry Christmas', True, (255, 255, 255))

line1_data = pygame.image.tostring(line1_surface, "RGBA", True)
line2_data = pygame.image.tostring(line2_surface, "RGBA", True)

line1_width, line1_height = line1_surface.get_size()
line2_width, line2_height = line2_surface.get_size()

# 粒子数量
particle_count = 6000
particles = []

# 螺旋效果参数
spiral_turns = 5  # 螺旋的圈数
spiral_particles_count = 1500  # 螺旋粒子的数量

# 生成圣诞树粒子
for i in range(particle_count):
    # 随机选择粒子在树上的位置
    layer = random.uniform(0, 1)
    
    # 树冠部分  树冠高度从0到4.0
    y = random.uniform(0.0, 4.15)  # 原为(0.0,4.0)
    # 半径随高度增加而减小
    normalized_y = (y + 1.0) / 4.0  # 将y坐标归一化到0-1
    max_radius = 2.0 * (1 - normalized_y * 0.7)  # 顶部半径小，底部半径大
    r = random.uniform(0, max_radius)
    
    theta = math.radians(random.uniform(0, 360))
    
    x = r * math.cos(theta)
    z = r * math.sin(theta)
    
    # 粒子颜色（改）
    color = (
        random.uniform(0.5, 0.8),
        random.uniform(0.6, 0.8),
        random.uniform(0.9, 1.0) 
    )
    particles.append([x, y, z, color])

# 生成螺旋状树叶粒子
for i in range(spiral_particles_count):
    # 螺旋粒子的高度分布 - 增加厚度
    base_y = random.uniform(0.2, 3.8)  # 基准高度
    thickness = 0.1  # 螺旋厚度  0.1最佳
    y = base_y + random.uniform(-thickness/2, thickness/2)  # 在基准高度上下添加随机偏移
    
    # 计算螺旋角度 - 使用基准高度保持螺旋连续性
    spiral_angle = (base_y / 4.0) * spiral_turns * 2 * math.pi  # 根据基准高度计算螺旋角度
    
    # 螺旋半径 - 从底部到顶部逐渐减小
    normalized_y = base_y / 4.0  # 使用基准高度计算归一化值
    spiral_radius = 1.8 * (1 - normalized_y * 0.9)  # 与树冠相似的半径变化
    
    # 添加一些随机性使螺旋更自然
    radius_variation = random.uniform(0.9, 1.1)
    actual_radius = spiral_radius * radius_variation
    
    # 计算螺旋粒子的位置
    x = actual_radius * math.cos(spiral_angle)
    z = actual_radius * math.sin(spiral_angle)
    
    # 螺旋粒子使用不同的颜色（金色/黄色系）
    if random.random() < 0.7:  # 70%的金色粒子（改）
        color = (random.uniform(0.7, 1.0), random.uniform(0.7, 1.0), random.uniform(0.7, 1.0))  # 金色
    else:  # 30%的白色粒子，增加层次感
        color = (1.0, 1.0, random.uniform(0.8, 1.0))  # 白色
    
    particles.append([x, y, z, color])

# 圣诞树主体灯球粒子
tree_light_ball_count = 50  # 树主体灯球粒子数量
tree_light_balls = []

# 生成树主体灯球粒子
for i in range(tree_light_ball_count):
    # 随机分布在树的不同高度
    y = random.uniform(0.3, 3.6)
    
    # 根据高度确定半径
    normalized_y = y / 4.0
    max_radius = 1.8 * (1 - normalized_y * 0.9)
    r = random.uniform(0.4, max_radius)  # 从0.3开始，避免太靠近中心
    
    theta = math.radians(random.uniform(0, 360))
    
    x = r * math.cos(theta)
    z = r * math.sin(theta)
    
    # 灯球颜色 - 使用鲜艳的节日颜色（改）
    color_dq = (random.uniform(0.7, 1.0), random.uniform(0.7, 0.9), random.uniform(0.7, 1.0))
    
    # 添加透明度
    alpha = random.uniform(0.5, 0.7)  # 透明度较低（0.7-0.9，数值越大越不透明）
    
    tree_light_balls.append([x, y, z, color_dq, alpha])

# 雪景粒子
snow_particle_count = 1000  # 雪花数量
snow_particles = []

# 初始化雪花位置
for i in range(snow_particle_count):
    # 雪花分布在整个视野范围内
    x = random.uniform(-15, 15)  # 水平范围
    y = random.uniform(-10, 10)  # 垂直范围
    z = random.uniform(-20, 5)   # 深度范围
    
    # 雪花大小和下落速度
    size = random.uniform(1.0, 3.0)  # 雪花大小
    speed = random.uniform(0.01, 0.05)  # 下落速度
    
    # 雪花轻微的水平飘动
    drift_speed = random.uniform(-0.005, 0.005)
    
    snow_particles.append([x, y, z, size, speed, drift_speed])

# 树顶灯球参数
light_ball_particles = []
light_ball_radius = 0.3  # 灯球半径
light_ball_particle_count = 200  # 灯球粒子数量

# 生成灯球粒子（位于y轴4.4处）
for i in range(light_ball_particle_count):
    # 使用球坐标生成均匀分布的粒子
    theta = random.uniform(0, 2 * math.pi)  # 方位角
    phi = random.uniform(0, math.pi)  # 极角
    
    # 转换为笛卡尔坐标
    x = light_ball_radius * math.sin(phi) * math.cos(theta)
    y = light_ball_radius * math.sin(phi) * math.sin(theta)
    z = light_ball_radius * math.cos(phi)
    
    # 将灯球放置在树顶 (0, 4.4, 0)
    x_final = x
    y_final = y + 4.4  # y轴4.4处
    z_final = z
    
    # 灯球颜色 - 金色和白色混合，模拟发光效果
    if random.random() < 0.7:
        # 金色粒子 （改）
        color = (random.uniform(0.9, 1.0), random.uniform(0.9, 1.0), 1.0)
    else:
        # 白色粒子，增加闪烁效果
        color = (1.0, 1.0, random.uniform(0.9, 1.0))
    
    light_ball_particles.append([x_final, y_final, z_final, color])

# 雪地粒子参数
snow_ground_particles = []
snow_ground_count = 2000  # 雪地粒子数量
snow_ground_radius = 4.0  # 雪地半径

# 生成雪地粒子
for i in range(snow_ground_count):
    # 在圆形区域内随机分布
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(0, snow_ground_radius)
    
    x = distance * math.cos(angle)
    z = distance * math.sin(angle)
    
    # 水波纹效果 - 使用正弦函数创建高低起伏
    # 根据距离中心的远近创建不同的波纹频率
    wave_frequency = 1.0 + distance * 0.5  # 频率随距离增加
    wave_amplitude = 0.3 * (1 - distance / snow_ground_radius)  # 振幅随距离减小
    
    # 基础高度加上波纹效果
    base_y = 0.0  # y轴0处
    y = base_y + wave_amplitude * math.sin(wave_frequency * distance + angle * 2)
    
    # 添加一些随机噪声使雪地更自然
    y += random.uniform(-0.05, 0.05)
    
    # 雪地颜色 - 白色为主，稍微有些变化模拟光影效果
    brightness = random.uniform(0.9, 1.0)
    color = (brightness, brightness, brightness)
    
    snow_ground_particles.append([x, y, z, color])

# 旋转角度
rotation_angle = 0
# 灯球闪烁计时器
light_ball_timer = 0

# 新增：鼠标拖动视角控制变量
mouse_dragging = False
last_mouse_pos = (0, 0)
camera_rotation_x = 0  # 绕X轴旋转角度
camera_rotation_y = 0  # 绕Y轴旋转角度
camera_distance = 7    # 相机距离中心的距离

# 主循环
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键
                mouse_dragging = True
                last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 左键
                mouse_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_dragging:
                # 计算鼠标移动距离
                dx = event.pos[0] - last_mouse_pos[0]
                dy = event.pos[1] - last_mouse_pos[1]
                
                # 更新相机旋转角度
                camera_rotation_y += dx * 0.1
                camera_rotation_x += dy * 0.1
                
                # 限制X轴旋转角度，避免过度翻转
                camera_rotation_x = max(-90, min(90, camera_rotation_x))
                
                last_mouse_pos = event.pos

    # 清除屏幕
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # 重置模型视图矩阵
    glLoadIdentity()
    
    # 设置相机位置和视角
    # 首先将相机向后移动
    glTranslatef(0.0, 0, -camera_distance)
    
    # 应用鼠标拖动的旋转
    glRotatef(camera_rotation_x, 1, 0, 0)  # 绕X轴旋转
    glRotatef(camera_rotation_y, 0, 1, 0)  # 绕Y轴旋转
    
    # 将场景向下移动，使中心保持在(0,2,0)
    glTranslatef(0.0, -2, 0)
    
    # 应用自动旋转
    glRotatef(rotation_angle, 0, 1, 0)  # 绕Y轴旋转
    
    # 首先绘制雪地（作为背景）
    glPointSize(2.0)
    glBegin(GL_POINTS)
    for particle in snow_ground_particles:
        x, y, z, color = particle
        glColor3f(*color)
        glVertex3f(x, y, z)
    glEnd()
    
    # 绘制圣诞树粒子
    glBegin(GL_POINTS)
    for particle in particles:
        x, y, z, color = particle
        glColor3f(*color)
        glVertex3f(x, y, z)
    glEnd()
    
    # 绘制树主体灯球粒子（更大、透明度更低）
    glPointSize(20.0)  # 更大的点尺寸
    glBegin(GL_POINTS)
    for particle in tree_light_balls:
        x, y, z, color, alpha = particle
        r, g, b = color
        glColor4f(r, g, b, alpha)  # 使用带透明度的颜色
        glVertex3f(x, y, z)
    glEnd()
    glPointSize(2.0)  # 恢复原始点尺寸
    
    # 绘制树顶灯球（使用更大的点尺寸使其更明显）
    glPointSize(3.0)  #原为3.0
    glBegin(GL_POINTS)
    
    # 更新灯球闪烁效果
    light_ball_timer += 1
    pulse = (math.sin(light_ball_timer * 0.1) + 1) * 0.3 + 0.7  # 脉动效果
    
    for particle in light_ball_particles:
        x, y, z, color = particle
        
        # 应用脉动效果到颜色
        r, g, b = color
        pulsed_color = (
            min(1.0, r * pulse),
            min(1.0, g * pulse), 
            min(1.0, b * pulse)
        )
        
        glColor3f(*pulsed_color)
        glVertex3f(x, y, z)
    
    glEnd()
    glPointSize(2.0)  # 恢复原始点尺寸

    # 绘制雪花粒子
    snow_sizes = {}
    for snow in snow_particles:
        x, y, z, size, speed, drift_speed = snow
        size_key = round(size, 1)
        
        if size_key not in snow_sizes:
            snow_sizes[size_key] = []
        
        # 更新雪花位置
        y -= speed
        x += drift_speed
        
        # 如果雪花落出视野，重新从顶部随机位置出现
        if y < -10 or z < -20 or z > 5:
            y = random.uniform(8, 10)
            x = random.uniform(-15, 15)
            z = random.uniform(-10, 5)
        
        # 更新雪花位置
        snow[0], snow[1], snow[2] = x, y, z
        
        # 存储雪花位置和颜色
        brightness = random.uniform(0.8, 1.0)
        snow_sizes[size_key].append((x, y, z, brightness))
    
    # 按大小分组绘制雪花
    for size, snow_list in snow_sizes.items():
        glPointSize(2.0)  #原为size
        glBegin(GL_POINTS)
        for x, y, z, brightness in snow_list:
            glColor3f(brightness, brightness, brightness)
            glVertex3f(x, y, z)
        glEnd()
    
    # 绘制文字（不参与旋转）
    # 保存当前矩阵状态
    glPushMatrix()
    glLoadIdentity()  # 重置矩阵
    
    # 设置正交投影，使文字显示在屏幕固定位置
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, display[0], display[1], 0, -1, 1)  # 设置2D正交投影
    
    glMatrixMode(GL_MODELVIEW)
    
    # 禁用深度测试，确保文字显示在最前面
    glDisable(GL_DEPTH_TEST)
    
    # 绘制第一行文字
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, line1_width, line1_height, 0, 
                 GL_RGBA, GL_UNSIGNED_BYTE, line1_data)
    
    # 计算文字位置（左上角）
    text_x = 20  # 距离左边20像素
    text_y1 = 20  # 第一行距离顶部20像素
    text_y2 = text_y1 + line1_height + 10  # 第二行在第一行下面，增加10像素间距
    
    # 绘制第一行文字矩形（垂直翻转）
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(text_x, text_y1)  # 左下角
    glTexCoord2f(1, 1); glVertex2f(text_x + line1_width, text_y1)  # 右下角
    glTexCoord2f(1, 0); glVertex2f(text_x + line1_width, text_y1 + line1_height)  # 右上角
    glTexCoord2f(0, 0); glVertex2f(text_x, text_y1 + line1_height)  # 左上角
    glEnd()
    
    # 绘制第二行文字
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, line2_width, line2_height, 0, 
                 GL_RGBA, GL_UNSIGNED_BYTE, line2_data)
    
    # 绘制第二行文字矩形（垂直翻转）
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(text_x, text_y2)  # 左下角
    glTexCoord2f(1, 1); glVertex2f(text_x + line2_width, text_y2)  # 右下角
    glTexCoord2f(1, 0); glVertex2f(text_x + line2_width, text_y2 + line2_height)  # 右上角
    glTexCoord2f(0, 0); glVertex2f(text_x, text_y2 + line2_height)  # 左上角
    glEnd()
    
    # 清理纹理和状态
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    
    # 恢复投影矩阵
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
    # 更新旋转角度
    rotation_angle += 0.3
    
    pygame.display.flip()
    clock.tick(60)