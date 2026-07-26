// flutter/lib/local_auth_bridge.dart
import 'package:flutter/services.dart';
import 'package:local_auth/local_auth.dart';

class LocalAuthBridge {
  static const MethodChannel _channel = MethodChannel('local_auth_bridge');
  static final LocalAuthentication _localAuth = LocalAuthentication();

  static void register() {
    _channel.setMethodCallHandler(_handleMethodCall);
    print('[LocalAuthBridge] 已注册 MethodChannel');
  }

  static Future<dynamic> _handleMethodCall(MethodCall call) async {
    print('[LocalAuthBridge] 收到调用: ${call.method}');
    
    switch (call.method) {
      case 'isAvailable':
        return await _isAvailable();
      case 'authenticate':
        return await _authenticate(call.arguments);
      case 'getAvailableBiometrics':
        return await _getAvailableBiometrics();
      default:
        throw PlatformException(
          code: 'Unimplemented',
          details: 'Method ${call.method} not implemented',
        );
    }
  }

  static Future<bool> _isAvailable() async {
    try {
      final canCheck = await _localAuth.canCheckBiometrics;
      final isDeviceSupported = await _localAuth.isDeviceSupported();
      print('[LocalAuthBridge] canCheckBiometrics: $canCheck');
      print('[LocalAuthBridge] isDeviceSupported: $isDeviceSupported');
      return canCheck && isDeviceSupported;
    } catch (e) {
      print('[LocalAuthBridge] 检查可用性失败: $e');
      return false;
    }
  }

  static Future<bool> _authenticate(dynamic arguments) async {
    try {
      final reason = arguments['reason'] ?? '验证身份';
      final bool authenticated = await _localAuth.authenticate(
        localizedReason: reason,
        options: const AuthenticationOptions(
          biometricOnly: true,
          stickyAuth: true,
        ),
      );
      print('[LocalAuthBridge] 认证结果: $authenticated');
      return authenticated;
    } catch (e) {
      print('[LocalAuthBridge] 认证失败: $e');
      return false;
    }
  }

  static Future<List<String>> _getAvailableBiometrics() async {
    try {
      final available = await _localAuth.getAvailableBiometrics();
      print('[LocalAuthBridge] 可用生物识别: $available');
      return available.map((e) => e.toString()).toList();
    } catch (e) {
      print('[LocalAuthBridge] 获取生物识别类型失败: $e');
      return [];
    }
  }
}