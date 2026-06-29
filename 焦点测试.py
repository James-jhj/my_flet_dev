import flet as ft

# 用于存储当前获得焦点的TextField实例
current_focused_textfield: ft.TextField | None = None

def main(page: ft.Page):
    page.title = "Flet TextField 焦点与虚拟键盘示例"
    page.vertical_alignment = ft.CrossAxisAlignment.START

    def on_textfield_focus(e: ft.ControlEvent):
        """
        当TextField获得焦点时调用的处理函数。
        将当前获得焦点的TextField实例存储到全局变量中。
        """
        #nonlocal current_focused_textfield
        current_focused_textfield = e.control
        print(f"当前焦点: {current_focused_textfield.label}")
        # 可选：为获得焦点的TextField添加视觉反馈
        for tf in [text_field1, text_field2, text_field3]:
            if tf == current_focused_textfield:
                tf.border_color = ft.Colors.BLUE_500
                tf.border_width = 2
            else:
                tf.border_color = ft.Colors.GREY_400
                tf.border_width = 1
        page.update()

    def on_key_press(e: ft.ControlEvent):
        """
        虚拟键盘按键点击事件处理函数。
        将按键文本追加到当前焦点TextField的值中。
        """
        if current_focused_textfield:
            key_char = e.control.text
            if key_char == "清空":
                current_focused_textfield.value = ""
            elif key_char == "退格":
                if current_focused_textfield.value:
                    current_focused_textfield.value = current_focused_textfield.value[:-1]
            else:
                current_focused_textfield.value += key_char
            page.update()
        else:
            print("没有TextField获得焦点，无法输入。")

    # 创建多个TextField控件，并绑定on_focus事件
    text_field1 = ft.TextField(label="姓名", on_focus=on_textfield_focus, width=300)
    text_field2 = ft.TextField(label="年龄", on_focus=on_textfield_focus, width=300)
    text_field3 = ft.TextField(label="地址", on_focus=on_textfield_focus, width=300)

    # 创建虚拟键盘布局
    keyboard_row1 = ft.Row(
        [
            ft.ElevatedButton("1", on_click=on_key_press),
            ft.ElevatedButton("2", on_click=on_key_press),
            ft.ElevatedButton("3", on_click=on_key_press),
            ft.ElevatedButton("清空", on_click=on_key_press, color=ft.Colors.RED_500),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    keyboard_row2 = ft.Row(
        [
            ft.ElevatedButton("A", on_click=on_key_press),
            ft.ElevatedButton("B", on_click=on_key_press),
            ft.ElevatedButton("C", on_click=on_key_press),
            ft.ElevatedButton("退格", on_click=on_key_press, color=ft.Colors.AMBER_700),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    keyboard_row3 = ft.Row(
        [
            ft.ElevatedButton(" ", on_click=on_key_press, width=150), # 空格键
            ft.ElevatedButton(".", on_click=on_key_press),
            ft.ElevatedButton("@", on_click=on_key_press),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.add(
        ft.Column(
            [
                ft.Text("请点击下方文本框以获得焦点:", size=18, weight=ft.FontWeight.BOLD),
                text_field1,
                text_field2,
                text_field3,
                ft.Divider(),
                ft.Text("虚拟键盘:", size=18, weight=ft.FontWeight.BOLD),
                keyboard_row1,
                keyboard_row2,
                keyboard_row3,
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # 首次加载时，尝试让第一个TextField获得焦点
    # 注意：直接设置focus()可能在某些平台或首次渲染时无效，
    # 更好的做法是在on_page_load或用户交互后设置
    # text_field1.focus() # 尝试设置初始焦点
    # page.update()


if __name__ == "__main__":
    ft.app(target=main)