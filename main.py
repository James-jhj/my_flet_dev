import flet as ft

APP_VERSION = "1.0.144"
APP_VERSION_CODE = 144

def main(page: ft.Page):
    # 存储控件引用
    main_textfield = None
    hidden_textfield = None
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
        print("尝试隐藏键盘")
        try:
            # 方法1：让隐藏的 TextField 获得焦点，然后立即让它失去焦点
            if hidden_textfield:
                # 先让隐藏的 TextField 获得焦点（这会触发键盘弹出）
                # 但是因为它太小了，键盘不会真正显示
                # 然后再让主 TextField 失去焦点
                page._focused_control = hidden_textfield
                page.update()
                
                # 然后再让页面本身获得焦点（如果有这个方法）
                # 如果没有，就只是保持隐藏 TextField 的焦点
                # 键盘会因为这个隐藏的 TextField 而不会显示
                print("✅ 键盘已隐藏（通过转移焦点）")
        except Exception as ex:
            print(f"方法1失败: {ex}")
            
            # 方法2：直接操作 DOM
            try:
                # 在移动端，可以通过 JavaScript 来隐藏键盘
                # 但 Flet 不直接支持，所以我们用另一个方法
                if main_textfield:
                    # 清空焦点状态
                    page._focused_control = None
                    page.update()
                    print("✅ 键盘已隐藏（通过清空焦点）")
            except Exception as ex2:
                print(f"方法2失败: {ex2}")
    
    # 创建主 TextField
    main_tf = ft.TextField(
        label="点击输入",
        on_focus=on_focus,
        on_blur=on_blur,
        hint_text="点击我弹出键盘",
    )
    main_textfield = main_tf
    
    # 创建隐藏的 TextField（尺寸极小，用于转移焦点）
    hidden_tf = ft.TextField(
        width=0,
        height=0,
        opacity=0,
        disabled=True,  # 禁用状态，但焦点仍然可以转移
    )
    hidden_textfield = hidden_tf
    
    # 创建隐藏键盘的按钮
    hide_btn = ft.ElevatedButton(
        content="隐藏键盘",
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
            hidden_tf,  # 隐藏的 TextField
            ft.Divider(height=20),
            hide_btn,
            ft.Divider(height=10),
            ft.Text("点击按钮或空白区域隐藏键盘", size=14),
            ft.Text(f"Flet 版本: {ft.__version__}", size=12, color=ft.Colors.GREY_600),
        ]),
        expand=True,
        on_click=on_container_click,
        padding=20,
    )
    
    page.add(container)
    page.update()
    print("✅ 页面加载完成")

ft.app(target=main)