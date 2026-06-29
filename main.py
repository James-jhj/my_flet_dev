import flet as ft
import time

APP_VERSION = "1.0.145"
APP_VERSION_CODE = 145

def main(page: ft.Page):
    # 存储控件引用
    main_textfield = None
    keyboard_visible = False
    
    def on_focus(e):
        global keyboard_visible
        keyboard_visible = True
        print("✅ 键盘弹出")
        try:
            snack = ft.SnackBar(
                content=ft.Text("键盘已弹出"),
                bgcolor=ft.Colors.BLUE_700,
                duration=2000,
                open=True,
            )
            page.overlay.append(snack)
            page.update()
        except:
            pass
    
    def on_blur(e):
        global keyboard_visible
        keyboard_visible = False
        print("❌ 键盘收起")
        try:
            snack = ft.SnackBar(
                content=ft.Text("键盘已收起"),
                bgcolor=ft.Colors.GREEN_700,
                duration=2000,
                open=True,
            )
            page.overlay.append(snack)
            page.update()
        except:
            pass
    
    def hide_keyboard(e):
        """通过临时禁用文本框来强制隐藏键盘"""
        print("尝试隐藏键盘")
        if main_textfield:
            try:
                # 步骤1: 禁用文本框
                main_textfield.disabled = True
                page.update()
                print("⏳ 已禁用文本框")
                
                # 步骤2: 等待系统响应
                time.sleep(0.1)
                
                # 步骤3: 重新启用文本框
                main_textfield.disabled = False
                page.update()
                print("✅ 键盘已隐藏（通过禁用/启用）")
                
                # 显示成功提示
                try:
                    snack = ft.SnackBar(
                        content=ft.Text("键盘已隐藏"),
                        bgcolor=ft.Colors.GREEN_700,
                        duration=1500,
                        open=True,
                    )
                    page.overlay.append(snack)
                    page.update()
                except:
                    pass
                    
            except Exception as ex:
                print(f"❌ 隐藏键盘失败: {ex}")
    
    # 创建主 TextField
    main_tf = ft.TextField(
        label="点击输入",
        on_focus=on_focus,
        on_blur=on_blur,
        hint_text="点击我弹出键盘",
    )
    main_textfield = main_tf
    
    # 创建隐藏键盘的按钮
    hide_btn = ft.ElevatedButton(
        content="🔽 隐藏键盘",
        on_click=hide_keyboard,
        #icon=ft.icons.KEYBOARD_HIDE_ROUNDED,
    )
    
    # 点击页面空白隐藏键盘
    def on_container_click(e):
        print("点击页面空白")
        hide_keyboard(e)
    
    # 创建布局
    container = ft.Container(
        content=ft.Column([
            ft.Text("键盘控制测试", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("点击输入框弹出键盘", size=16),
            ft.Divider(height=20),
            main_tf,
            ft.Divider(height=20),
            hide_btn,
            ft.Divider(height=10),
            ft.Text("点击按钮或空白区域隐藏键盘", size=14),
            ft.Divider(height=5),
            ft.Text(f"Flet 版本: {ft.__version__}", size=12, color=ft.Colors.GREY_600),
            ft.Text(f"应用版本: {APP_VERSION}", size=12, color=ft.Colors.GREY_600),
        ]),
        expand=True,
        on_click=on_container_click,
        padding=20,
    )
    
    page.add(container)
    page.update()
    print("✅ 页面加载完成")

ft.app(target=main)