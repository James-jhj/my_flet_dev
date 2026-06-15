import flet as ft
import flet.canvas as cv
import flet_audio as ftaudio
from flet_audio import AudioState
import asyncio
import threading
import time
import json
import os
import platform
import requests
import re
import mutagen
import html
import datetime
import math
import asyncio
import datetime as dt
import calendar
from datetime import datetime, timedelta
from pathlib import Path
from lunardate import LunarDate
from urllib.parse import quote
from typing import Optional
from zhdate import ZhDate
import openpyxl
from openpyxl import Workbook, load_workbook
from datetime import timezone, timedelta
from chinese_calendar import is_workday as cn_is_workday
from android_notify import Notification

import hashlib
import subprocess
import uuid
import sys

# ========== 2. 版本信息 ==========
APP_VERSION = "1.0.44"
APP_VERSION_CODE = 44
# =============================

class ReminderApp:
    def __init__(self):
        self.page = None
        self.debug_text = None  # 用于显示调试信息
        
    def log(self, message, is_error=False):
        """在界面上显示日志"""
        if self.debug_text:
            color = ft.Colors.RED if is_error else ft.Colors.BLACK
            self.debug_text.value += f"\n{message}"
            self.debug_text.color = color
            self.page.update()
        print(message)  # 同时也打印，方便adb查看
        
    def start_foreground_service(self):
        """启动前台服务 - 带界面调试"""
        self.log("=== 开始启动前台服务 ===")
        
        if platform.system() != "Linux":
            self.log("警告：不是Android平台", True)
            return False
        
        try:
            # 步骤1: 检查 pyjnius
            self.log("步骤1: 检查 pyjnius...")
            try:
                from jnius import autoclass
                self.log("✅ pyjnius 导入成功")
            except ImportError as e:
                self.log(f"❌ pyjnius 导入失败: {str(e)}", True)
                self.log("解决方案: 在 pyproject.toml 中添加 pyjnius 依赖", True)
                return False
            
            # 步骤2: 获取 Activity
            self.log("步骤2: 获取 Android Activity...")
            try:
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                context = PythonActivity.mActivity
                self.log(f"✅ Activity 获取成功")
            except Exception as e:
                self.log(f"❌ 获取 Activity 失败: {str(e)}", True)
                return False
            
            # 步骤3: 检查服务类
            self.log("步骤3: 检查 ForegroundService 类...")
            try:
                ServiceClass = autoclass('com.jianghuajie.event_reminder.ForegroundService')
                self.log("✅ 服务类存在")
            except Exception as e:
                self.log(f"❌ 找不到服务类: {str(e)}", True)
                self.log("可能原因: .flet 目录配置不正确", True)
                return False
            
            # 步骤4: 启动服务
            self.log("步骤4: 启动服务...")
            Intent = autoclass('android.content.Intent')
            intent = Intent(context, ServiceClass)
            intent.setAction('START_FOREGROUND')
            
            sdk_version = context.getApplicationInfo().targetSdkVersion
            self.log(f"目标 SDK 版本: {sdk_version}")
            
            if sdk_version >= 26:
                context.startForegroundService(intent)
                self.log("✅ 使用 startForegroundService 启动")
            else:
                context.startService(intent)
                self.log("✅ 使用 startService 启动")
            
            self.log("=== 服务启动成功 ===")
            return True
            
        except Exception as e:
            error_msg = traceback.format_exc()
            self.log(f"❌ 错误: {str(e)}", True)
            self.log(f"详细: {error_msg}", True)
            return False

def main(page: ft.Page):
    page.title = "事件提醒助手"
    page.scroll = ft.ScrollMode.AUTO  # 允许滚动
    
    app = ReminderApp()
    app.page = page
    
    # 创建调试信息显示区域
    app.debug_text = ft.Text("等待操作...", selectable=True, size=12)
    
    status_text = ft.Text("⚪ 服务未启动", size=16)
    
    def start_service(e):
        # 清空之前的调试信息
        app.debug_text.value = ""
        page.update()
        
        # 显示启动中状态
        status_text.value = "🟡 正在启动..."
        status_text.color = ft.Colors.ORANGE
        page.update()
        
        # 启动服务
        result = app.start_foreground_service()
        
        if result:
            status_text.value = "✅ 前台服务已启动"
            status_text.color = ft.Colors.GREEN
        else:
            status_text.value = "❌ 启动失败（详见下方调试信息）"
            status_text.color = ft.Colors.RED
        
        page.update()

    def show_snack_bar(page, message, is_error=False):
        """显示 SnackBar（兼容不同 Flet 版本）"""
        try:
            if hasattr(page, 'show_snack_bar'):
                page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text(message),
                        bgcolor=ft.Colors.RED_700 if is_error else ft.Colors.GREEN_700,
                    )
                )
            else:
                snack = ft.SnackBar(
                    content=ft.Text(message),
                    bgcolor=ft.Colors.RED_700 if is_error else ft.Colors.GREEN_700,
                    open=True,
                )
                page.overlay.append(snack)
                page.update()
                def close_snack():
                    time.sleep(3)
                    if snack in page.overlay:
                        page.overlay.remove(snack)
                        page.update()
                threading.Thread(target=close_snack, daemon=True).start()
        except Exception as e:
            print(f"显示 SnackBar 失败: {e}")
    
    def test_notification(e):
        """测试：只显示通知，不启动服务"""
        if platform.system() == "Linux":
            try:
                from jnius import autoclass
                
                # 获取当前 Activity
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                context = PythonActivity.mActivity
                
                # 获取系统服务
                NotificationManager = autoclass('android.app.NotificationManager')
                NotificationChannel = autoclass('android.app.NotificationChannel')
                
                # 创建通知渠道 (Android 8.0+)
                channel_id = "test_channel"
                channel_name = "测试频道"
                
                # 使用系统图标（更可靠）
                # 注意：这里需要使用应用的资源ID，或者用简单的数字
                # 下面的代码改用更简单的方式
                
                # 方法1：使用 NotificationCompat.Builder 的简单方式
                # 但由于 Flet 环境可能没有 NotificationCompat，改用原生 Notification
                
                if hasattr(context, 'getSystemService'):
                    manager = context.getSystemService(NotificationManager)
                    
                    # 创建渠道
                    if hasattr(NotificationManager, 'IMPORTANCE_HIGH'):
                        channel = NotificationChannel(
                            channel_id, 
                            channel_name, 
                            NotificationManager.IMPORTANCE_HIGH
                        )
                        manager.createNotificationChannel(channel)
                    
                    # 创建通知
                    # 使用简单的方式，不依赖资源ID
                    from android import Android
                    droid = Android()
                    
                    # 使用 webview 的方式显示一个简单的提示
                    app.log("尝试发送通知...")
                    
                    # 更简单的方式：直接用 Flet 的 SnackBar
                    page.show_dialog(
                        ft.SnackBar(
                            content=ft.Text("通知功能需要配置，但服务启动测试请查看上方调试信息"),
                            duration=3000
                        )
                    )
                    
                    app.log("如果看到这条日志，说明代码执行到了这里")
                    
            except Exception as e:
                error_msg = traceback.format_exc()
                app.log(f"通知测试失败: {str(e)}", True)
                app.log(f"详细: {error_msg}", True)
                page.show_dialog(
                    ft.SnackBar(
                        content=ft.Text(f"通知失败: {str(e)[:50]}"),
                        bgcolor=ft.Colors.RED
                    )
                )
        else:
            page.show_dialog(
                ft.SnackBar(
                    content=ft.Text("当前不是Android平台"),
                    bgcolor=ft.Colors.ORANGE
                )
            )
    
    start_btn = ft.ElevatedButton("🚀 启动前台服务", on_click=start_service)
    test_btn = ft.OutlinedButton("🔔 测试通知", on_click=test_notification)
    
    # 布局
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
                    height=300,
                ),
            ], spacing=15),
            padding=20,
        )
    )
    
    # 页面加载时显示环境信息
    app.log(f"Flet 版本: {ft.__version__}")
    app.log(f"平台: {platform.system()}")
    app.log(f"Python: {sys.version}")

ft.app(target=main)