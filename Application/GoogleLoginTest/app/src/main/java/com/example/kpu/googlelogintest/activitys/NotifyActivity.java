package com.example.kpu.googlelogintest.activitys;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import com.example.kpu.googlelogintest.R;

public class NotifyActivity extends AppCompatActivity {
    private TextView textView_messagebody;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notify);

        textView_messagebody = findViewById(R.id.text_message);

        textView_messagebody.setText(getIntent().getStringExtra("message"));
    }
}
