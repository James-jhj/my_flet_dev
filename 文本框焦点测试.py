import flet as ft

def main(page: ft.Page):
    text_field = ft.TextField(label="点击此处输入")

    # 定义点击空白区域的处理函数
    def dismiss_focus(e):
        # 方法 A: 直接让当前焦点失去 (适用于单文本框场景)
        text_field.focus() 
        text_field.on_blur() # 注意：Flet 中通常通过更新状态或调用底层 Flutter 方法，更通用的是下面的方法 B
        
        # 方法 B (通用): 清除所有焦点 (Flet 0.21+ 支持较好，旧版本需 workaround)
        # 最稳妥方式：将焦点移到一个不可见的 dummy 控件，或直接重置页面焦点状态
        page.focus_control(None) 
        page.update()

    # 创建一个覆盖全屏的透明容器用于捕获点击
    overlay = ft.Container(
        expand=True,
        on_click=dismiss_focus,
        #bgcolor=ft.Colors.TRANSPARENT # 确保透明不影响视觉
    )

    page.add(
        #overlay, # 先添加遮罩层，确保能捕获点击
        ft.Column([text_field], spacing=20, expand=True)
    )

ft.app(target=main)
