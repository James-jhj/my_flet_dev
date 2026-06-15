// .flet/android/app/src/main/java/com/jianghuajie/event_reminder/MainActivity.kt
package com.jianghuajie.event_reminder

import android.content.Intent
import android.os.Bundle
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {
    private val CHANNEL = "com.jianghuajie.event_reminder/service"
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
    }
    
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
            .setMethodCallHandler { call, result ->
                when (call.method) {
                    "startService" -> {
                        startForegroundService()
                        result.success(true)
                    }
                    "stopService" -> {
                        stopForegroundService()
                        result.success(true)
                    }
                    else -> result.notImplemented()
                }
            }
    }
    
    private fun startForegroundService() {
        val intent = Intent(this, ForegroundService::class.java).apply {
            action = ForegroundService.ACTION_START
        }
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
    }
    
    private fun stopForegroundService() {
        val intent = Intent(this, ForegroundService::class.java).apply {
            action = ForegroundService.ACTION_STOP
        }
        stopService(intent)
    }
}