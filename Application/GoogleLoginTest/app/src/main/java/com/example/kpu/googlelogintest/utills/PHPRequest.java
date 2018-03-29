package com.example.kpu.googlelogintest.utills;

import android.util.Log;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

/**
 * Created by KPU on 2018-02-20.
 */

public class PHPRequest {
    public static String execute(String... data) {
        OkHttpClient client = new OkHttpClient.Builder()
                .connectTimeout(10,TimeUnit.SECONDS)
                .readTimeout(10,TimeUnit.SECONDS)
                .writeTimeout(10,TimeUnit.SECONDS)
                .build();

        FormBody.Builder builder = new FormBody.Builder();


        for(int i=1; i<data.length; i+=2) {
            builder.add(data[i], data[i + 1]);
            Log.d("타입이름" + data[i], "속성 값 : "+ data[i+1]+", i값 : "+i);
        }
        RequestBody body = builder.build();
        //request
        Request request = new Request.Builder()
                .url(data[0])
                .post(body)
                .build();

        Response response;


        try {
            response = client.newCall(request).execute();
            return response.body().string();

        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
}
