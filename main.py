import flet as ft

APP_VERSION = "1.0.142"
APP_VERSION_CODE = 142

def main(page: ft.Page):
    # 设置页面属性
    page.scroll = ft.ScrollMode.AUTO
    
    # 用于跟踪键盘状态
    keyboard_visible = False
    
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
        except Exception as ex:
            print(f"on_focus 错误: {ex}")
        
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
        except Exception as ex:
            print(f"on_blur 错误: {ex}")
    
    # 使用 on_keyboard_event（Flet 0.22+）
    def on_keyboard_event(e):
        nonlocal keyboard_visible
        print(f"键盘事件: {e.key}")
        
        try:
            if e.key == "KEYBOARD_OPEN":
                keyboard_visible = True
                print("✅ 键盘已打开")
                snack = ft.SnackBar(
                    content=ft.Text("✅ 键盘已打开"),
                    bgcolor=ft.Colors.GREEN_700,
                    duration=2000,
                    open=True,
                )
                page.overlay.append(snack)
                page.update()
                
            elif e.key == "KEYBOARD_CLOSED":
                keyboard_visible = False
                print("❌ 键盘已关闭")
                snack = ft.SnackBar(
                    content=ft.Text("❌ 键盘已关闭"),
                    bgcolor=ft.Colors.RED_700,
                    duration=2000,
                    open=True,
                )
                page.overlay.append(snack)
                page.update()
        except Exception as ex:
            print(f"键盘事件错误: {ex}")
    
    # 绑定键盘事件
    try:
        page.on_keyboard_event = on_keyboard_event
        print("✅ on_keyboard_event 已绑定")
    except AttributeError:
        print("⚠️ 当前版本不支持 on_keyboard_event")
    
    # 备选方案：使用 on_resize
    def on_resize(e):
        nonlocal keyboard_visible
        try:
            # 尝试多种检测方式
            bottom_inset = page.media.view_insets.bottom if hasattr(page.media, 'view_insets') else 0
            page_height = page.height if page.height else 0
            window_height = page.window.height if page.window and page.window.height else 0
            
            # 综合判断键盘是否弹出
            is_keyboard_open = bottom_inset > 50 or (window_height - page_height > 100)
            
            if is_keyboard_open and not keyboard_visible:
                keyboard_visible = True
                print(f"✅ 检测到键盘弹出 (bottom_inset: {bottom_inset})")
                try:
                    snack = ft.SnackBar(
                        content=ft.Text(f"键盘弹出 ({bottom_inset})"),
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
                print("❌ 检测到键盘收起")
                try:
                    snack = ft.SnackBar(
                        content=ft.Text("键盘已收起"),
                        bgcolor=ft.Colors.RED_700,
                        duration=2000,
                        open=True,
                    )
                    page.overlay.append(snack)
                    page.update()
                except:
                    pass
                    
        except Exception as ex:
            print(f"on_resize 错误: {ex}")
    
    page.on_resize = on_resize
    print("✅ on_resize 已绑定")
    
    # 点击空白区域失去焦点（修复版）
    def on_container_click(e):
        try:
            # 方法1：尝试使用 focus 方法（兼容性好）
            # 找到所有 TextField 并移除焦点
            for control in page.controls:
                if isinstance(control, ft.Container):
                    # 递归查找 TextField
                    def find_and_blur(ctrl):
                        if isinstance(ctrl, ft.TextField):
                            try:
                                ctrl.blur()
                            except:
                                pass
                        elif hasattr(ctrl, 'content') and ctrl.content:
                            find_and_blur(ctrl.content)
                        elif hasattr(ctrl, 'controls'):
                            for child in ctrl.controls:
                                find_and_blur(child)
                    
                    find_and_blur(control)
            
            page.update()
            print("点击空白，尝试失去焦点")
        except Exception as ex:
            print(f"点击容器错误: {ex}")
    
    # 创建 TextField 引用以便直接控制
    text_field = ft.TextField(
        label="点击输入",
        on_focus=on_focus,
        on_blur=on_blur,
        hint_text="点击我弹出键盘",
    )
    
    # 创建容器
    container = ft.Container(
        content=ft.Column([
            ft.Text("键盘事件测试", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("点击下方输入框测试键盘", size=16),
            ft.Divider(height=20),
            text_field,
            ft.Divider(height=20),
            ft.Text("点击空白区域可隐藏键盘", italic=True, size=14, color=ft.Colors.GREY_600),
            ft.Text(f"Flet版本: {ft.__version__}", size=12, color=ft.Colors.GREY_400),
        ]),
        expand=True,
        on_click=on_container_click,
        padding=20,
    )
    
    page.add(container)

if __name__ == "__main__":
    ft.app(target=main)