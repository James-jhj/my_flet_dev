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
    // 先检查设备是否支持
    final isDeviceSupported = await _localAuth.isDeviceSupported();
    print('[LocalAuthBridge] isDeviceSupported: $isDeviceSupported');
    
    if (!isDeviceSupported) {
      return false;
    }
    
    // 尝试获取可用生物识别
    final availableBiometrics = await _getAvailableBiometrics();
    print('[LocalAuthBridge] availableBiometrics: $availableBiometrics');
    
    // 如果有可用生物识别，返回 true
    if (availableBiometrics.isNotEmpty) {
      return true;
    }
    
    // 某些设备 canCheckBiometrics 可能返回 false，但实际支持
    // 所以如果设备支持，但 canCheckBiometrics 返回 false，仍然返回 true
    final canCheck = await _localAuth.canCheckBiometrics;
    print('[LocalAuthBridge] canCheckBiometrics: $canCheck');
    
    // 如果设备支持，即使 canCheckBiometrics 为 false，也返回 true
    // 因为认证时 local_auth 会再次检查
    return isDeviceSupported;
  } catch (e) {
    print('[LocalAuthBridge] 检查可用性失败: $e');
    return false;
  }
}

  static Future<bool> _authenticate(dynamic arguments) async {
    try {
      final reason = arguments['reason'] ?? '验证身份';
      print('[LocalAuthBridge] 开始认证, reason: $reason');
      
      // 先检查是否可用
      final isAvailable = await _isAvailable();
      if (!isAvailable) {
        print('[LocalAuthBridge] 生物识别不可用');
        return false;
      }
      
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
      print('[LocalAuthBridge] 原始生物识别类型: $available');
      
      // 转换为字符串列表
      final result = available.map((e) {
        switch (e) {
          case BiometricType.face:
            return 'face';
          case BiometricType.fingerprint:
            return 'fingerprint';
          case BiometricType.iris:
            return 'iris';
          case BiometricType.strong:
            return 'strong';
          case BiometricType.weak:
            return 'weak';
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