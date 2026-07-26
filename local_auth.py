# local_auth.py
import flet as ft
import asyncio
import json

class LocalAuth:
    """Flet 生物识别桥接类"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self._initialized = False
        
    def _ensure_initialized(self):
        """确保 Flutter 端已初始化"""
        if not self._initialized:
            try:
                # 调用 Flutter 端的注册方法
                if hasattr(self.page, 'call_method'):
                    self.page.call_method('local_auth_bridge_register')
                self._initialized = True
                print("[LocalAuth] ✅ 桥接已初始化")
            except Exception as e:
                print(f"[LocalAuth] ❌ 初始化失败: {e}")
    
    def is_available(self) -> bool:
        """检查生物识别是否可用"""
        try:
            self._ensure_initialized()
            
            # 使用 Flet 的 MethodChannel 调用
            if hasattr(self.page, 'call_method'):
                result = self.page.call_method(
                    'local_auth_bridge_isAvailable',
                    {}
                )
                print(f"[LocalAuth] is_available 结果: {result}")
                return result
        except Exception as e:
            print(f"[LocalAuth] 检查可用性失败: {e}")
        return False
    
    async def authenticate(self, reason: str = "验证身份") -> bool:
        """执行生物识别认证"""
        try:
            self._ensure_initialized()
            
            if hasattr(self.page, 'call_method'):
                result = await self.page.call_method_async(
                    'local_auth_bridge_authenticate',
                    {'reason': reason}
                )
                print(f"[LocalAuth] authenticate 结果: {result}")
                return result
        except Exception as e:
            print(f"[LocalAuth] 认证失败: {e}")
        return False
    
    def get_available_biometrics(self) -> list:
        """获取可用的生物识别类型"""
        try:
            self._ensure_initialized()
            
            if hasattr(self.page, 'call_method'):
                result = self.page.call_method(
                    'local_auth_bridge_getAvailableBiometrics',
                    {}
                )
                print(f"[LocalAuth] 可用生物识别: {result}")
                return result
        except Exception as e:
            print(f"[LocalAuth] 获取类型失败: {e}")
        return []