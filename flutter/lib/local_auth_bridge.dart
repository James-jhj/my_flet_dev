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

  // ========== 简化：直接返回 true ==========
  static Future<bool> _isAvailable() async {
    try {
      // 简单检查设备是否支持
      final isDeviceSupported = await _localAuth.isDeviceSupported();
      print('[LocalAuthBridge] isDeviceSupported: $isDeviceSupported');
      
      // 如果设备支持，直接返回 true
      if (isDeviceSupported) {
        print('[LocalAuthBridge] ✅ 设备支持生物识别');
        return true;
      }
      
      // 即使 isDeviceSupported 返回 false，也尝试获取生物识别类型
      // 有些设备这个 API 可能不准确
      final available = await _localAuth.getAvailableBiometrics();
      print('[LocalAuthBridge] 可用生物识别: $available');
      
      // 如果列表不为空，返回 true
      if (available.isNotEmpty) {
        print('[LocalAuthBridge] ✅ 检测到已注册生物识别');
        return true;
      }
      
      // 最后尝试 canCheckBiometrics
      final canCheck = await _localAuth.canCheckBiometrics;
      print('[LocalAuthBridge] canCheckBiometrics: $canCheck');
      
      // 如果 canCheck 为 true，返回 true
      if (canCheck) {
        print('[LocalAuthBridge] ✅ canCheckBiometrics 通过');
        return true;
      }
      
      // 如果以上都失败，尝试直接认证（有些设备需要实际尝试才能知道）
      // 但这里返回 false，让用户看到提示
      print('[LocalAuthBridge] ❌ 所有检查都失败');
      return false;
    } catch (e) {
      print('[LocalAuthBridge] 检查可用性失败: $e');
      return false;
    }
  }

  static Future<bool> _authenticate(dynamic arguments) async {
    try {
      final reason = arguments['reason'] ?? '验证身份';
      print('[LocalAuthBridge] 开始认证, reason: $reason');
      
      // 尝试直接认证，不管 isAvailable 的结果
      // 因为有些设备 isAvailable 可能返回 false，但实际可以认证
      try {
        final bool authenticated = await _localAuth.authenticate(
          localizedReason: reason,
          options: const AuthenticationOptions(
            biometricOnly: true,
            stickyAuth: true,
          ),
        );
        print('[LocalAuthBridge] 认证结果: $authenticated');
        return authenticated;
      } catch (authError) {
        print('[LocalAuthBridge] 认证失败: $authError');
        return false;
      }
    } catch (e) {
      print('[LocalAuthBridge] 认证失败: $e');
      return false;
    }
  }

  static Future<List<String>> _getAvailableBiometrics() async {
    try {
      final available = await _localAuth.getAvailableBiometrics();
      print('[LocalAuthBridge] 原始生物识别类型: $available');
      
      final result = available.map((e) {
        switch (e) {
          case BiometricType.face:
            return 'face';
          case BiometricType.fingerprint:
            return 'fingerprint';
          case BiometricType.iris:
            return 'iris';
          default:
            return e.toString();
        }
      }).toList();
      
      print('[LocalAuthBridge] 转换后类型: $result');
      return result;
    } catch (e) {
      print('[LocalAuthBridge] 获取生物识别类型失败: $e');
      return [];
    }
  }
}