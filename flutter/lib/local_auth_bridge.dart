// flutter/lib/local_auth_bridge.dart
import 'package:flutter/services.dart';
import 'package:local_auth/local_auth.dart';

class LocalAuthBridge {
  static const MethodChannel _channel = MethodChannel('local_auth_bridge');
  static final LocalAuthentication _localAuth = LocalAuthentication();

  static void register() {
    _channel.setMethodCallHandler(_handleMethodCall);
  }

  static Future<dynamic> _handleMethodCall(MethodCall call) async {
    switch (call.method) {
      case 'isAvailable':
        // 直接返回 true，让 Python 端跳过检查
        return true;
      case 'authenticate':
        return await _authenticate(call.arguments);
      default:
        throw PlatformException(
          code: 'Unimplemented',
          details: 'Method ${call.method} not implemented',
        );
    }
  }

  static Future<bool> _authenticate(dynamic arguments) async {
    try {
      final reason = arguments['reason'] ?? '验证身份';
      
      // 直接尝试认证
      final bool authenticated = await _localAuth.authenticate(
        localizedReason: reason,
        options: const AuthenticationOptions(
          biometricOnly: true,
          stickyAuth: true,
        ),
      );
      return authenticated;
    } catch (e) {
      print('[LocalAuthBridge] 认证失败: $e');
      return false;
    }
  }
}