import pygame

# 初始化Pygame
pygame.init()

# 設定螢幕尺寸
screen_width = 800
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 設定按鈕
button_width = 80  # 調整按鈕寬度
button_height = 50
button_x_start = 50
button_y_start = 350  # 將按鈕往上移動 50 pixel
button_spacing = 90  # 調整按鈕間距

buttons = []
button_states = [False] * 8  # 追蹤按鈕狀態
for i in range(8):
    x = button_x_start + i * button_spacing
    y = button_y_start
    button = pygame.Rect(x, y, button_width, button_height)
    buttons.append(button)

# 設定按鈕文字
font = pygame.font.Font(None, 30)
button_labels = ["CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7", "CH8"]

# 設定狀態指示器 (LED燈)
led_radius = 20  # 調整LED燈大小
led_y_offset = -130  # LED燈在按鈕上方的偏移量 (原-100 再往上30)
text_y_offset = -180 + 50  # 文字在LED燈上方的偏移量 (原-150 再往上30, 再往下50)

# GPIO 腳位設定 (Raspberry Pi)
try:
    import RPi.GPIO as GPIO
    gpio_pins = [5, 6, 13, 16, 19, 20, 21, 26]  # 請根據您的實際連接修改
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_pins, GPIO.OUT)

    # 設定 GPIO 初始狀態為 HIGH
    for pin in gpio_pins:
        GPIO.output(pin, GPIO.HIGH)

except ImportError:
    print("RPi.GPIO not found. Running in non-GPIO mode.")
    gpio_pins = []

# 遊戲迴圈
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, button in enumerate(buttons):
                if button.colliderect(pygame.Rect(mouse_x, mouse_y, 1, 1)):
                    # 切換按鈕狀態
                    button_states[i] = not button_states[i]
                    print(f"Button {i+1} toggled")

                    # 控制 GPIO 腳位 (Raspberry Pi)
                    if gpio_pins:
                        # 反轉 GPIO 狀態 (LOW 表示 ON)
                        GPIO.output(gpio_pins[i], not button_states[i])

    # 清空螢幕
    screen.fill((255, 255, 255))

    # 繪製按鈕
    for i, button in enumerate(buttons):
        button_color = (0, 0, 255) if not button_states[i] else (0, 255, 0)  # 根據狀態改變顏色
        pygame.draw.rect(screen, button_color, button)
        text = font.render(button_labels[i], True, (255, 255, 255))
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)

    # 繪製狀態指示器 (LED燈)
    for i in range(8):
        x = buttons[i].centerx  # LED燈在按鈕中心上方
        y = buttons[i].top + led_y_offset
        # 顛倒 LED 顏色 (LOW 表示 ON)
        led_color = (255, 0, 0) if not button_states[i] else (0, 255, 0)  # 紅色表示ON 綠色表示OFF
        pygame.draw.circle(screen, led_color, (x, y), led_radius)

        # 繪製 ON/OFF 文字
        # 顛倒文字 (LOW 表示 ON)
        text_str = "OFF" if not button_states[i] else "ON"  # OFF表示ON, ON表示OFF
        text = font.render(text_str, True, (0, 0, 0))  # 文字顏色可調整
        text_rect = text.get_rect(center=(x, y + text_y_offset))
        screen.blit(text, text_rect)

    # 更新螢幕
    pygame.display.flip()

# 退出Pygame
pygame.quit()

# 清理 GPIO (Raspberry Pi)
try:
    GPIO.cleanup()
except NameError:
    pass