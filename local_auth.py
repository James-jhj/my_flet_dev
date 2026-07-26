# local_auth.py
import flet as ft
import asyncio

class LocalAuth:
    """Flet 生物识别桥接类"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        
    def is_available(self) -> bool:
        """检查生物识别是否可用"""
        try:
            if hasattr(self.page, 'invoke_method'):
                result = self.page.invoke_method(
                    'local_auth_bridge.isAvailable',
                    {}
                )
                print(f"[LocalAuth] is_available: {result}")
                return result
        except Exception as e:
            print(f"[LocalAuth] 检查可用性失败: {e}")
        return False
    
    def get_available_biometrics(self) -> list:
        """获取可用的生物识别类型"""
        try:
            if hasattr(self.page, 'invoke_method'):
                result = self.page.invoke_method(
                    'local_auth_bridge.getAvailableBiometrics',
                    {}
                )
                print(f"[LocalAuth] 可用生物识别: {result}")
                return result
        except Exception as e:
            print(f"[LocalAuth] 获取类型失败: {e}")
        return []
    
    async def authenticate(self, reason: str = "验证身份") -> bool:
        """执行生物识别认证"""
        try:
            # 先检查可用性
            if not self.is_available():
                print("[LocalAuth] 生物识别不可用")
                return False
            
            if hasattr(self.page, 'invoke_method'):
                result = await self.page.invoke_method_async(
                    'local_auth_bridge.authenticate',
                    {'reason': reason}
                )
                print(f"[LocalAuth] authenticate: {result}")
                return result
        except Exception as e:
            print(f"[LocalAuth] 认证失败: {e}")
        return False