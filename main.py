import flet as ft
import time

APP_VERSION = "1.0.148"
APP_VERSION_CODE = 148

def main(page: ft.Page):
    # 存储控件引用
    global keyboard_visible
    main_textfield = None
    hidden_textfield = None
    keyboard_visible = False
    # 设置亮色主题
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE  # 设置背景色为白色
    
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
    
    def hide_keyboard(e):
        """通过转移焦点到隐藏控件来隐藏键盘"""
        print("尝试隐藏键盘")
        if main_textfield and hidden_textfield:
            try:
                # 步骤1: 清空主输入框内容
                main_textfield.value = ""
                page.update()
                print("⏳ 已清空输入框内容")

                # 步骤1: 将焦点转移到隐藏的 TextField
                hidden_textfield.focus()
                page.update()
                print("⏳ 焦点已转移到隐藏控件")
                
                # 步骤2: 短暂延迟
                time.sleep(0.05)
                
                # 步骤3: 禁用两个控件（让它们都失去焦点）
                
                main_textfield.disabled = True      # 🔑 关键：禁用主输入框
                hidden_textfield.disabled = True
                page.update()
                print("⏳ 两个控件已禁用")
                
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

                # 步骤4: 等待系统响应
                time.sleep(0.1)

                # 步骤5: 重新启用两个控件
                #main_textfield.disabled = False     # 🔑 关键：恢复主输入框
                #hidden_textfield.disabled = False
                #page.update()
                    
            except Exception as ex:
                print(f"❌ 隐藏键盘失败: {ex}")
    
    # 创建主 TextField
    main_tf = ft.TextField(
        label="点击输入",
        on_focus=on_focus,
        #on_blur=on_blur,
        hint_text="点击我弹出键盘",
    )
    main_textfield = main_tf
    
    # 创建隐藏的 TextField（用于转移焦点）
    hidden_tf = ft.TextField(
        width=0,
        height=0,
        opacity=0,
        disabled=False,  # 初始为启用状态
    )
    hidden_textfield = hidden_tf
    
    # 创建隐藏键盘的按钮
    hide_btn = ft.ElevatedButton(
        content="🔽 隐藏键盘",
        on_click=hide_keyboard,
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
            hidden_tf,  # 隐藏的 TextField（不可见）
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