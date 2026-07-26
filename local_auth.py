# local_auth.py
import flet as ft
import asyncio

class LocalAuth:
    """Flet 生物识别桥接类"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self._debug_mode = True  # 调试模式
        
    def is_available(self) -> bool:
        """检查生物识别是否可用 - 调试模式始终返回 True"""
        if self._debug_mode:
            print("[LocalAuth] 调试模式：强制返回 True")
            return True
        
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
    
    async def authenticate(self, reason: str = "验证身份") -> bool:
        """执行生物识别认证"""
        try:
            print(f"[LocalAuth] 开始认证: {reason}")
            
            if hasattr(self.page, 'invoke_method'):
                result = await self.page.invoke_method_async(
                    'local_auth_bridge.authenticate',
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