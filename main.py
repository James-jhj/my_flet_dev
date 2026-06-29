import flet as ft
import time

APP_VERSION = "1.0.149"
APP_VERSION_CODE = 149

def main(page: ft.Page):
    # 存储控件引用
    main_textfield = None
    hidden_textfield = None
    
    # 设置亮色主题
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    
    def on_focus(e):
        print("✅ 主输入框获得焦点 - 键盘弹出")
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
        print("❌ 主输入框失去焦点")
        try:
            snack = ft.SnackBar(
                content=ft.Text("主输入框失去焦点"),
                bgcolor=ft.Colors.ORANGE_700,
                duration=1500,
                open=True,
            )
            page.overlay.append(snack)
            page.update()
        except:
            pass
    
    def on_hidden_focus(e):
        """隐藏控件获得焦点时的回调"""
        print("🎯 隐藏控件获得焦点！")
        try:
            snack = ft.SnackBar(
                content=ft.Text("🎯 焦点已转移到隐藏控件"),
                bgcolor=ft.Colors.PURPLE_700,
                duration=1500,
                open=True,
            )
            page.overlay.append(snack)
            page.update()
        except:
            pass
    
    def on_hidden_blur(e):
        """隐藏控件失去焦点时的回调"""
        print("👋 隐藏控件失去焦点")
    
    def hide_keyboard(e):
        """通过转移焦点到隐藏控件来隐藏键盘"""
        print("尝试隐藏键盘")
        if main_textfield and hidden_textfield:
            try:
                # 步骤1: 清空主输入框内容
                main_textfield.value = ""
                page.update()
                print("⏳ 已清空输入框内容")
                
                # 步骤2: 禁用主输入框（强制失去焦点）
                main_textfield.disabled = True
                page.update()
                print("⏳ 主输入框已禁用")
                
                # 步骤3: 短暂延迟
                time.sleep(0.05)
                
                # 步骤4: 重新启用主输入框
                main_textfield.disabled = False
                page.update()
                print("⏳ 主输入框已重新启用")
                
                print("✅ 键盘已隐藏")
                
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
        label="主输入框（点击输入）",
        on_focus=on_focus,
        on_blur=on_blur,
        hint_text="点击我弹出键盘",
        bgcolor=ft.Colors.BLUE_50,
    )
    main_textfield = main_tf
    
    # 隐藏控件（用于调试，可见）
    hidden_tf = ft.TextField(
        label="🎯 隐藏控件（观察焦点是否转移到这里）",
        hint_text="这个控件用来接收焦点",
        on_focus=on_hidden_focus,
        on_blur=on_hidden_blur,
        disabled=False,
        bgcolor=ft.Colors.PURPLE_50,
        border_color=ft.Colors.PURPLE,
    )
    hidden_textfield = hidden_tf
    
    # 创建隐藏键盘的按钮
    hide_btn = ft.ElevatedButton(
        content="🔽 隐藏键盘",
        on_click=hide_keyboard,
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
    )
    
    # 点击页面空白隐藏键盘
    def on_container_click(e):
        print("点击页面空白")
        hide_keyboard(e)
    
    # 创建布局
    container = ft.Container(
        content=ft.Column([
            ft.Text("键盘控制测试 - 调试模式", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("点击输入框弹出键盘，点击按钮或空白区域隐藏", size=14, color=ft.Colors.GREY_700),
            ft.Divider(height=20),
            
            ft.Text("主输入框:", size=14, weight=ft.FontWeight.BOLD),
            main_tf,
            
            ft.Divider(height=20),
            ft.Text("焦点转移目标（可见，用于调试）:", size=14, weight=ft.FontWeight.BOLD),
            hidden_tf,
            
            ft.Divider(height=20),
            hide_btn,
            
            ft.Divider(height=10),
            ft.Text("注意：隐藏控件可能不会获得焦点，但键盘会收起", size=12, color=ft.Colors.GREY_600),
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