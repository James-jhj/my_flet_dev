import flet as ft
import time
import threading

APP_VERSION = "1.0.151"
APP_VERSION_CODE = 151

def main(page: ft.Page):
    # 存储控件引用
    main_textfield = None
    keyboard_visible = False
    
    # 使用字典存储状态
    state = {
        "is_textfield_disabled": False
    }
    
    # 设置亮色主题
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    
    def on_focus(e):
        nonlocal keyboard_visible
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
    
    def hide_keyboard(e=None):
        """隐藏键盘并禁用文本框"""
        print("尝试隐藏键盘")
        if main_textfield:
            try:
                # 步骤1: 禁用主输入框（强制失去焦点，键盘收起）
                main_textfield.disabled = True
                state["is_textfield_disabled"] = True
                page.update()
                print("⏳ 文本框已禁用")

                # 🔑 步骤2: 使用 threading.Timer 延迟重新启用
                def re_enable():
                    try:
                        main_textfield.disabled = False
                        state["is_textfield_disabled"] = False
                        page.update()
                        print("⏳ 文本框已重新启用")
                        print("✅ 键盘已隐藏")
                    except Exception as ex:
                        print(f"❌ 重新启用失败: {ex}")
                
                # 150ms 后重新启用
                timer = threading.Timer(0.15, re_enable)
                timer.daemon = True  # 设置为守护线程
                timer.start()
                
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
    
    def show_keyboard(e=None):
        """启用文本框并弹出键盘"""
        if main_textfield:
            try:
                # 确保文本框可用
                main_textfield.disabled = False
                state["is_textfield_disabled"] = False
                page.update()
                print("⏳ 文本框已启用")
                
                # 显示提示
                try:
                    snack = ft.SnackBar(
                        content=ft.Text("文本框已恢复，点击输入弹出键盘"),
                        bgcolor=ft.Colors.BLUE_700,
                        duration=1500,
                        open=True,
                    )
                    page.overlay.append(snack)
                    page.update()
                except:
                    pass
                    
            except Exception as ex:
                print(f"❌ 启用文本框失败: {ex}")
    
    def toggle_keyboard(e):
        """切换键盘状态：点击空白区域切换"""
        if state["is_textfield_disabled"]:
            print("🔄 切换：启用文本框")
            show_keyboard(e)
        else:
            print("🔄 切换：禁用文本框并隐藏键盘")
            hide_keyboard(e)
    
    # 点击主输入框：确保它可用并获得焦点
    def on_text_click(e):
        print("点击主输入框")
        if state["is_textfield_disabled"]:
            main_textfield.disabled = False
            state["is_textfield_disabled"] = False
            page.update()
            print("⏳ 文本框已启用")
    
    # 创建主 TextField
    main_tf = ft.TextField(
        label="点击输入",
        on_focus=on_focus,
        on_click=on_text_click,
        hint_text="点击我弹出键盘",
    )
    main_textfield = main_tf
    
    # 创建隐藏键盘的按钮
    hide_btn = ft.ElevatedButton(
        content="🔽 隐藏键盘",
        on_click=hide_keyboard,
    )
    
    # 创建启用文本框的按钮
    show_btn = ft.ElevatedButton(
        content="🔼 恢复键盘",
        on_click=show_keyboard,
        bgcolor=ft.Colors.BLUE_100,
    )
    
    # 点击页面空白：切换键盘状态
    def on_container_click(e):
        print("点击页面空白")
        toggle_keyboard(e)
    
    # 创建布局
    container = ft.Container(
        content=ft.Column([
            ft.Text("键盘控制测试", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("点击输入框弹出键盘，点击空白区域切换", size=14, color=ft.Colors.GREY_700),
            ft.Divider(height=20),
            
            ft.Text("状态信息:", size=14, weight=ft.FontWeight.BOLD),
            ft.Text(
                value="点击下方输入框或点击空白区域切换",
                size=12,
                color=ft.Colors.GREY_600,
            ),
            
            ft.Divider(height=20),
            main_tf,
            ft.Divider(height=20),
            
            ft.Row([
                hide_btn,
                show_btn,
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            
            ft.Divider(height=10),
            ft.Text("💡 点击空白区域切换键盘状态", size=12, color=ft.Colors.GREY_600),
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