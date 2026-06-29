import flet as ft

APP_VERSION = "1.0.146"
APP_VERSION_CODE = 146

def main(page: ft.Page):
    # 基准高度和键盘状态
    base_height = None
    is_keyboard_visible = False
    
    def on_resize(e: ft.PageResizeEvent):
        nonlocal base_height, is_keyboard_visible
        
        current_height = e.height
        
        # 1. 首次触发或基准为空：将当前高度设为基准
        if base_height is None:
            base_height = current_height
            print(f"📏 基准高度已设定: {base_height}")
            return
        
        # 2. 忽略过小的变化（防止抖动）
        #if abs(current_height - base_height) < 50:
            #return
            
        # 3. 判断键盘状态（阈值设为 100px，更接近 Android 原生建议）
        if current_height < base_height - 30:
            if not is_keyboard_visible:
                is_keyboard_visible = True
                #print("⌨️ 键盘弹出")
                try:
                    snack = ft.SnackBar(
                        content=ft.Text("⌨️ 键盘弹出"),
                        bgcolor=ft.Colors.GREEN_700,
                        duration=1500,
                        open=True,
                    )
                    page.overlay.append(snack)
                    page.update()
                except:
                    pass
                # 在这里更新 UI，例如调整底部按钮位置
                page.title = "键盘: 弹出"
                page.update()
        else:
            if is_keyboard_visible:
                is_keyboard_visible = False
                #print("👌 键盘收起")
                try:
                    snack = ft.SnackBar(
                        content=ft.Text("👌 键盘收起"),
                        bgcolor=ft.Colors.GREEN_700,
                        duration=1500,
                        open=True,
                    )
                    page.overlay.append(snack)
                    page.update()
                except:
                    pass
                # 在这里恢复 UI
                page.title = "键盘: 收起"
                page.update()

    # 绑定事件
    page.on_resize = on_resize

    # --- 你的页面布局代码 ---
    text_field = ft.TextField(hint_text="点击输入")
    page.add(
        ft.Column([
            ft.Text("键盘监听示例", size=30),
            text_field,
            ft.Container(expand=True),  # 占位，将输入框推到上方
            ft.ElevatedButton("隐藏键盘", on_click=lambda _: hide_keyboard(text_field, page))
        ], expand=True)
    )
    page.update()

def hide_keyboard(textfield, page):
    # 你已有的隐藏键盘逻辑
    if textfield:
        textfield.disabled = True
        page.update()
        import time
        time.sleep(0.1)
        textfield.disabled = False
        page.update()

ft.app(target=main)