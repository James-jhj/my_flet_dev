import flet as ft

APP_VERSION = "1.0.141"
APP_VERSION_CODE = 141

def main(page: ft.Page):
    # 设置页面属性以支持更好的键盘处理
    page.scroll = ft.ScrollMode.AUTO
    
    def on_focus(e):
        print("TextField 获得焦点")
        try:
            snack = ft.SnackBar(
                content=ft.Text("键盘即将弹出（焦点获取）"),
                bgcolor=ft.Colors.BLUE_700,
                duration=2000,
                open=True,
            )
            page.overlay.append(snack)
            page.update()
        except:
            pass
        
    def on_blur(e):
        print("TextField 失去焦点")
        try:
            snack = ft.SnackBar(
                content=ft.Text("键盘即将收起（焦点丢失）"),
                bgcolor=ft.Colors.BLUE_700,
                duration=2000,
                open=True,
            )
            page.overlay.append(snack)
            page.update()
        except:
            pass
    
    # 使用状态变量避免重复触发
    keyboard_visible = False
    
    def on_resize(e):
        nonlocal keyboard_visible
        
        # 获取 view_insets
        bottom_inset = page.media.view_insets.bottom
        # 获取 padding（可能需要）
        bottom_padding = page.media.padding.bottom
        
        #print(f"bottom_inset: {bottom_inset}, bottom_padding: {bottom_padding}")

        try:
            snack = ft.SnackBar(
                content=ft.Text(f"bottom_inset: {bottom_inset}, bottom_padding: {bottom_padding}"),
                bgcolor=ft.Colors.GREEN_700,
                duration=2000,
                open=True,
            )
            page.overlay.append(snack)
            page.update()
        except:
            pass
        
        # 判断键盘状态（使用多个指标）
        is_keyboard_open = bottom_inset > 50
        
        if is_keyboard_open and not keyboard_visible:
            keyboard_visible = True
            try:
                snack = ft.SnackBar(
                    content=ft.Text(f"✅ 键盘已弹出（inset: {bottom_inset}）"),
                    bgcolor=ft.Colors.GREEN_700,
                    duration=2000,
                    open=True,
                )
                page.overlay.append(snack)
                page.update()
            except:
                pass
                
        elif not is_keyboard_open and keyboard_visible:
            keyboard_visible = False
            try:
                snack = ft.SnackBar(
                    content=ft.Text("❌ 键盘已收起"),
                    bgcolor=ft.Colors.RED_700,
                    duration=2000,
                    open=True,
                )
                page.overlay.append(snack)
                page.update()
            except:
                pass

    page.on_resize = on_resize

    # 添加一个点击页面空白处失去焦点的功能
    def on_click_container(e):
        # 移除所有TextField的焦点
        page.focused_control = None
        page.update()
        print("点击空白区域，失去焦点")

    # 创建一个容器覆盖整个页面来捕捉点击事件
    container = ft.Container(
        content=ft.Column([
            ft.Text("点击下方输入框测试键盘", size=20),
            ft.TextField(
                label="点击输入",
                on_focus=on_focus,
                on_blur=on_blur,
            ),
            ft.Text("点击空白区域可失去焦点", italic=True, size=14),
        ]),
        expand=True,
        on_click=on_click_container,  # 点击容器触发失去焦点
        padding=20,
    )

    page.add(container)

ft.app(target=main)