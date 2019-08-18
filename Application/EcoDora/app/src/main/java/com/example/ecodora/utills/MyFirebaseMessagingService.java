package com.example.ecodora.utills;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.media.RingtoneManager;
import android.util.Log;

import com.example.ecodora.R;
import com.example.ecodora.NotifyActivity;
import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

import org.json.JSONException;
import org.json.JSONObject;

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

    private void sendNotification(String messageBody){
        Intent intent = new Intent(this, NotifyActivity.class); // 눌렀을 때 실행할 액티비티
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        intent.putExtra("message", messageBody); //여기에 넘겨줄 데이터를 추가
        Log.d("받은 메세지" , messageBody);


        NotificationManager mNotificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        String id = "my_channel_01";
        CharSequence name = "test";
        int importance = NotificationManager.IMPORTANCE_HIGH;
        NotificationChannel mChannel = new NotificationChannel(id, name, importance);
        mChannel.enableLights(true);
        mChannel.setLightColor(Color.RED);
        mChannel.setSound(RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION), null);
        mChannel.enableVibration(true);
        mChannel.setVibrationPattern(new long[]{100, 200, 300, 400, 500, 400, 300, 200, 400});

        mChannel.setShowBadge(false);

        mNotificationManager.createNotificationChannel(mChannel);
        int notifyID = 1;
        String CHANNEL_ID = "my_channel_01";




        try {
            JSONObject jsonMeg = new JSONObject(messageBody);
            Notification notification = new Notification.Builder(this)
                    .setContentTitle("주행 종료")
                    .setContentText(String.format("주행연비 : %.2f Km/L    주행거리 : %.2f Km", jsonMeg.getDouble("fuel_efi"), jsonMeg.getDouble("distance")))
                    .setSmallIcon(R.drawable.img_car)
                    .setChannelId(CHANNEL_ID)
                    .build();
            mNotificationManager.notify(notifyID, notification);

        } catch (JSONException e) {
            e.printStackTrace();
        }


    }



}
