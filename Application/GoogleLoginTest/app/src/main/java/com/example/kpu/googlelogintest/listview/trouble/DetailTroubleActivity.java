package com.example.kpu.googlelogintest.listview.trouble;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.TextView;
import android.widget.Toast;

import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.listview.record.RecordData;

public class DetailTroubleActivity extends Activity {
    private TextView code, description, time;
    private TroubleData troubleData;
    private WebView webView;
    private WebSettings webSettings;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail_trouble);
        code = findViewById(R.id.textView_trouble_code);
        description = findViewById(R.id.textView_trouble_description);
        time = findViewById(R.id.textView_trouble_time);
        webView = findViewById(R.id.webView_trouble);
        troubleData = (TroubleData)getIntent().getSerializableExtra("data");

        code.setText(troubleData.getTroubleCode());
        description.setText(troubleData.getTroubleContent());
        time.setText(troubleData.getTroubleTime());

        webView.setWebViewClient(new WebViewClient());
        webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webView.scrollTo(0,1100);
//        webView.loadUrl("https://www.obd-codes.com/"+ troubleData.getTroubleCode());

        webView.loadUrl("https://translate.google.com/translate?hl=en&tl=ko&u=https://www.obd-codes.com/" + troubleData.getTroubleCode());
        webView.setHorizontalScrollBarEnabled(false);
        webView.getSettings().setLayoutAlgorithm(WebSettings.LayoutAlgorithm.SINGLE_COLUMN);
        //        Toast.makeText(this, troubleData.getTroubleCode(), Toast.LENGTH_SHORT).show();

    }
}
