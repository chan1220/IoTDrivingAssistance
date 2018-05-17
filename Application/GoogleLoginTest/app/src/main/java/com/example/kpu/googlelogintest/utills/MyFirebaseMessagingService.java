package com.example.kpu.googlelogintest.utills;

import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.media.RingtoneManager;
import android.net.Uri;
import android.support.v4.app.NotificationCompat;
import android.util.Log;

import com.example.kpu.googlelogintest.activitys.LoginActivity;
import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.activitys.NotifyActivity;
import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

/**
 * Created by KPU on 2018-02-19.
 */

public class MyFirebaseMessagingService extends FirebaseMessagingService {
    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        Log.d("누구", "From: " + remoteMessage.getFrom());


        if (remoteMessage.getData().size() > 0) {
            sendNotification(remoteMessage.getData().get("message"));
        }


        // Check if message contains a notification payload.
        if (remoteMessage.getNotification() != null) {
            Log.d("포그라운드에서 받은 메세지", remoteMessage.getNotification().getBody());
            sendNotification(remoteMessage.getNotification().getBody());
        }
        // Also if you intend on generating your own notifications as a result of a received FCM
        // message, here is where that should be initiated. See sendNotification method below.
    }

    private void sendNotification(String messageBody) {
        Intent intent = new Intent(this, NotifyActivity.class); // 눌렀을 때 실행할 액티비티
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        intent.putExtra("message", messageBody); //여기에 넘겨줄 데이터를 추가

        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0 /* Request code */, intent,
                PendingIntent.FLAG_ONE_SHOT);

        Uri defaultSoundUri= RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
        NotificationCompat.Builder notificationBuilder = new NotificationCompat.Builder(this)
                .setSmallIcon(R.drawable.img_doraemon)
                .setContentTitle("주행 종료")
                .setContentText(messageBody)
                .setAutoCancel(true)
                .setSound(defaultSoundUri)
                .setContentIntent(pendingIntent);

        NotificationManager notificationManager =
                (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);

        notificationManager.notify(0 /* ID of notification */, notificationBuilder.build());
    }



}
