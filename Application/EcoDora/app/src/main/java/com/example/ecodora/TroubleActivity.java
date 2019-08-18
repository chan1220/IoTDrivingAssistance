package com.example.ecodora;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.ecodora.listview.trouble.DetailTroubleActivity;
import com.example.ecodora.listview.trouble.TroubleAdapter;
import com.example.ecodora.listview.trouble.TroubleData;
import com.example.ecodora.utills.DBRequester;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class TroubleActivity extends AppCompatActivity implements DBRequester.Listener {
    private ListView listView;
    private TroubleAdapter adapter;
    private ProgressDialog progressDialog;
    private String userID;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trouble);
        setTitle("고장 진단 이력");
        // widget init
        adapter = new TroubleAdapter();
        listView = findViewById(R.id.listView_trouble);
        progressDialog = new ProgressDialog(TroubleActivity.this);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setMessage("검색중입니다...");
        listView.setAdapter(adapter);
        userID = getIntent().getStringExtra("id");

        // 웹서버에 데이터 요청, progressBar 출력, 올때까지 대기
        try {
            JSONObject param = new JSONObject();
            param.put("usr_id", userID);
            new DBRequester.Builder(TroubleActivity.this, getString(R.string.server_ip_port), TroubleActivity.this)
                    .attach("request/code")
                    .streamPost(param)
                    .request("request trouble");
//            progressDialog.show();

        } catch (JSONException e) {
            e.printStackTrace();
        }

        // 리스트뷰를 클릭할때 동작
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            /**
             * @param parent 클릭이 발생한 AdapterView.
             * @param view 클릭 한 AdapterView 내의 View(Adapter에 의해 제공되는 View).
             * @param position 클릭 한 Item의 position
             * @param id 클릭 된 Item의 Id
             */
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                // adapter.getItem(position)의 return 값은 Object 형
                // 실제 Item의 자료형은 CustomDTO 형이기 때문에
                // 형변환을 시켜야 getResId() 메소드를 호출할 수 있습니다.
                TroubleData troubleData = (TroubleData) adapter.getItem(position);

                // new Intent(현재 Activity의 Context, 시작할 Activity 클래스)
//                Intent intent = new Intent(DrivingRecordActivity.this, DetailActivity.class);
                Intent intent = new Intent(TroubleActivity.this, DetailTroubleActivity.class);
                intent.putExtra("data", troubleData);
                startActivity(intent);
            }
        });



    }

    @Override
    public void onResponse(String id, JSONObject json, Object... params) {
        try {
            if (json.getBoolean("success") == false) {
                Toast.makeText(this, "검색 실패", Toast.LENGTH_SHORT).show();
                return;
            }

            switch (id) {
                case "request trouble":
                    JSONArray jsonArray = json.getJSONArray("data");
                    for (int i = 0; i < jsonArray.length(); i++) {

                        TroubleData dto = new TroubleData();
                        Log.d(jsonArray.getJSONObject(i).get("code").toString(), jsonArray.getJSONObject(i).get("description").toString());
                        dto.setTroubleTime(jsonArray.getJSONObject(i).get("code_time").toString());
                        dto.setTroubleCode(jsonArray.getJSONObject(i).get("code").toString());
                        dto.setTroubleContent(jsonArray.getJSONObject(i).get("description").toString());
                        adapter.addItem(dto);
                        adapter.notifyDataSetChanged();
                    }
                    progressDialog.dismiss();
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void onResponse(String id, JSONArray json, Object... params) {

    }

    @Override
    public void onError(String id, String message, Object... params) {

    }
}
