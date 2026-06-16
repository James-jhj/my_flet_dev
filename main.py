import flet as ft
import sys
import traceback  # 添加这个导入
import platform
from jnius import autoclass

# ========== 2. 版本信息 ==========
APP_VERSION = "1.0.47"
APP_VERSION_CODE = 47
# =============================

class ReminderApp:
    def __init__(self):
        self.page = None
        self.debug_text = None
        
    def log(self, message, is_error=False):
        """在界面上显示日志"""
        if self.debug_text:
            color = ft.Colors.RED if is_error else ft.Colors.BLACK
            self.debug_text.value += f"\n{message}"
            self.debug_text.color = color
            self.page.update()
        print(message)
        
    def start_foreground_service(self):
        """启动前台服务 - 带界面调试"""
        self.log("=== 开始启动前台服务 ===")
        self.log(f"platform.system() = {platform.system()}")
        
        # Android 上 platform.system() 返回 "Linux"
        if platform.system() != "Linux":
            self.log("警告：不是Android平台", True)
            return False

        try:
            self.log("✅ pyjnius 导入成功")
            
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            context = PythonActivity.mActivity
            self.log("✅ Activity 获取成功")
            
            ServiceClass = autoclass('com.jianghuajie.event_reminder.ForegroundService')
            self.log("✅ 服务类存在")
            
            Intent = autoclass('android.content.Intent')
            intent = Intent(context, ServiceClass)
            intent.setAction('START_FOREGROUND')
            
            context.startService(intent)  # 先启动服务一次
            context.startForegroundService(intent) # 然后启动前台服务
            self.log("✅ 前台服务启动成功")
            return True
            
        except Exception as e:
            self.log(f"❌ 启动失败: {str(e)}", True)
            return False
        

def main(page: ft.Page):
    page.title = "事件提醒助手"
    page.scroll = ft.ScrollMode.AUTO
    
    app = ReminderApp()
    app.page = page
    
    app.debug_text = ft.Text("等待操作...", selectable=True, size=12)
    status_text = ft.Text("⚪ 服务未启动", size=16)
    
    def start_service(e):
        app.debug_text.value = ""
        page.update()
        
        status_text.value = "🟡 正在启动..."
        status_text.color = ft.Colors.ORANGE
        page.update()
        
        result = app.start_foreground_service()
        
        if result:
            status_text.value = "✅ 前台服务已启动"
            status_text.color = ft.Colors.GREEN
        else:
            status_text.value = "❌ 启动失败（详见下方调试信息）"
            status_text.color = ft.Colors.RED
        
        page.update()
    
    def test_notification(e):
        """测试通知"""
        if platform.system() == "Linux":
            try:
                from jnius import autoclass
                
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                context = PythonActivity.mActivity
                
                NotificationManager = autoclass('android.app.NotificationManager')
                NotificationChannel = autoclass('android.app.NotificationChannel')
                
                channel_id = "test_channel"
                channel_name = "测试频道"
                
                manager = context.getSystemService(NotificationManager)
                
                if hasattr(NotificationManager, 'IMPORTANCE_HIGH'):
                    channel = NotificationChannel(
                        channel_id, 
                        channel_name, 
                        NotificationManager.IMPORTANCE_HIGH
                    )
                    manager.createNotificationChannel(channel)
                
                app.log("尝试发送通知...")
                
                # 显示 SnackBar 提示
                page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text("通知测试执行成功，请查看通知栏"),
                        duration=3000
                    )
                )
                
            except Exception as e:
                app.log(f"通知测试失败: {str(e)}", True)
                page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text(f"通知失败: {str(e)[:50]}"),
                        bgcolor=ft.Colors.RED,
                        duration=3000
                    )
                )
        else:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("当前不是Android平台"),
                    bgcolor=ft.Colors.ORANGE,
                    duration=3000
                )
            )
    
    start_btn = ft.ElevatedButton("🚀 启动前台服务", on_click=start_service)
    test_btn = ft.OutlinedButton("🔔 测试通知", on_click=test_notification)
    
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("🎯 事件提醒助手", size=30, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Row([start_btn, test_btn], spacing=10),
                status_text,
                ft.Divider(),
                ft.Text("📋 调试信息:", weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=app.debug_text,
                    padding=10,
                    bgcolor=ft.Colors.GREY_100,
                    border_radius=5,
                    height=350,
                ),
            ], spacing=15),
            padding=20,
        )
    )
    
    app.log(f"Flet 版本: {ft.__version__}")
    app.log(f"platform.system(): {platform.system()}")
    app.log(f"Python: {sys.version}")
    app.log("")
    app.log("点击上方按钮启动前台服务")

ft.app(target=main)