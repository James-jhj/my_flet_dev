import flet as ft

# ========== 2. 版本信息 ==========
APP_VERSION = "1.0.140"
APP_VERSION_CODE = 140
# =============================

def main(page: ft.Page):
    def on_focus(e):
        # 在此处执行键盘弹出后的逻辑，如调整布局
        try:
            snack = ft.SnackBar(
                content=ft.Text(f"键盘即将弹出（焦点获取）"),
                bgcolor=ft.Colors.BLUE_700,
                duration=2000,
                open=True,
            )
            page.overlay.append(snack)
            page.update()
        except:
            pass
        
    def on_blur(e):
        # 在此处执行键盘收起后的逻辑
        try:
            snack = ft.SnackBar(
                content=ft.Text(f"键盘即将收起（焦点丢失）"),
                bgcolor=ft.Colors.BLUE_700,
                duration=2000,
                open=True,
            )
            page.overlay.append(snack)
            page.update()
        except:
            pass
    
    
    def on_resize(e):
        # 监听移动端的虚拟键盘弹出或收起
        bottom_inset = page.media.view_insets.bottom
        if bottom_inset > 50:  # 阈值判断，避免误触
            try:
                snack = ft.SnackBar(
                    content=ft.Text(f"检测到键盘弹出（高度变化）：{bottom_inset}"),
                    bgcolor=ft.Colors.BLUE_700,
                    duration=2000,
                    open=True,
                )
                page.overlay.append(snack)
                page.update()
            except:
                pass
        else:
            try:
                snack = ft.SnackBar(
                    content=ft.Text(f"键盘已收起：{bottom_inset}"),
                    bgcolor=ft.Colors.BLUE_700,
                    duration=2000,
                    open=True,
                )
                page.overlay.append(snack)
                page.update()
            except:
                pass
        
        
    

    """ 
    def on_resize(e):
        # 监听Windows当前窗口的宽度和高度
        current_width = page.window.width
        current_height = page.window.height
        print(f"窗口大小已改变: {current_width} x {current_height}")
    """

    page.on_resize = on_resize



    tf = ft.TextField(
        label="点击输入",
        on_focus=on_focus,
        on_blur=on_blur
    )




    page.add(tf)



ft.app(target=main)
