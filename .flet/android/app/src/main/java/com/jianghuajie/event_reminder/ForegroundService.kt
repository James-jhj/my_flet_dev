// .flet/android/app/src/main/java/com/jianghuajie/event_reminder/ForegroundService.kt
package com.jianghuajie.event_reminder

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat

class ForegroundService : Service() {
    
    companion object {
        const val CHANNEL_ID = "event_reminder_channel"
        const val NOTIFICATION_ID = 1001
        const val ACTION_START = "START_FOREGROUND"
        const val ACTION_STOP = "STOP_FOREGROUND"
    }
    
    override fun onBind(intent: Intent?): IBinder? = null
    
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_START -> startForegroundService()
            ACTION_STOP -> stopForegroundService()
        }
        return START_STICKY
    }
    
    private fun startForegroundService() {
        createNotificationChannel()
        startForeground(NOTIFICATION_ID, buildNotification())
    }
    
    private fun stopForegroundService() {
        stopForeground(true)
        stopSelf()
    }
    
    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "事件提醒助手",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "接收事件提醒和通知"
                setSound(null, null)  // 不播放默认声音，让 Python 代码控制
                enableVibration(true)
                vibrationPattern = longArrayOf(0, 500, 200, 500)
            }
            
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }
    }
    
    private fun buildNotification(): Notification {
        // 点击通知打开 App
        val intent = packageManager.getLaunchIntentForPackage(packageName)
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("事件提醒助手")
            .setContentText("正在后台运行，准备提醒您的事件")
            .setSmallIcon(android.R.drawable.ic_menu_edit)
            .setContentIntent(pendingIntent)
            .setOngoing(true)  // 用户无法滑动清除
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()
    }
}