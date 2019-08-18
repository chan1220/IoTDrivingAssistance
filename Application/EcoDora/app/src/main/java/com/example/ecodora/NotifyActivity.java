package com.example.ecodora;

import android.os.Bundle;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

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
