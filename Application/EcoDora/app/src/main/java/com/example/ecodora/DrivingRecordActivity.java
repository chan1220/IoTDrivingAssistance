package com.example.ecodora;

import android.app.DatePickerDialog;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.ListView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.ecodora.listview.record.DetailActivity;
import com.example.ecodora.listview.record.RecordAdapter;
import com.example.ecodora.listview.record.RecordData;
import com.example.ecodora.utills.DBRequester;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class DrivingRecordActivity extends AppCompatActivity implements DBRequester.Listener {

    private RecordAdapter adapter;
    private ListView listView;
    private Button button_search;
    private Button start_time, end_time;
    private String usr_id;
    private ProgressDialog progressDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_driving_record);

        // widget init
        adapter = new RecordAdapter();
        listView = findViewById(R.id.listView);
        button_search = findViewById(R.id.button_search);
        start_time = findViewById(R.id.input_start);
        end_time = findViewById(R.id.input_end);
        progressDialog = new ProgressDialog(DrivingRecordActivity.this);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setMessage("검색중입니다...");
        setTitle("주행 기록");

        listView.setAdapter(adapter);

        usr_id = getIntent().getStringExtra("id");


        DatePickerDialog.OnDateSetListener startDateListener = new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int i, int i1, int i2) {
                start_time.setText(i + "-" + String.format("%02d", (i1 + 1)) + "-" + String.format("%02d", i2));
            }
        };
        final DatePickerDialog startDateDialog = new DatePickerDialog(this, startDateListener, 2018, 9, 01);

        DatePickerDialog.OnDateSetListener endtDateListener = new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int i, int i1, int i2) {
                end_time.setText(i + "-" + String.format("%02d", (i1 + 1)) + "-" + String.format("%02d", i2));
            }
        };
        final DatePickerDialog endDateDialog = new DatePickerDialog(this, endtDateListener, 2018, 9, 31);


        start_time.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                startDateDialog.show();
            }
        });

        end_time.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                endDateDialog.show();
            }
        });


        button_search.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                adapter.clearItem();

                try {
                    JSONObject param = new JSONObject();
                    param.put("usr_id", usr_id);
                    param.put("start_date", start_time.getText().toString());
                    param.put("end_date", end_time.getText().toString());
                    new DBRequester.Builder(DrivingRecordActivity.this, getString(R.string.server_ip_port), DrivingRecordActivity.this)
                            .attach("request/record")
                            .streamPost(param)
                            .request("request record");
                    progressDialog.show();

                } catch (JSONException e) {
                    e.printStackTrace();
                }

            }
        });


        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            /**
             * ListView의 Item을 Click 할 때 수행할 동작
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
                RecordData recordData = (RecordData) adapter.getItem(position);

                // new Intent(현재 Activity의 Context, 시작할 Activity 클래스)
//                Intent intent = new Intent(DrivingRecordActivity.this, DetailActivity.class);
                Intent intent = new Intent(DrivingRecordActivity.this, DetailActivity.class);
                // putExtra(key, value)
                intent.putExtra("data", recordData);
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
                case "request record":
                    JSONArray jsonArray = json.getJSONArray("data");
                    for (int i = 0; i < jsonArray.length(); i++) {

                        RecordData dto = new RecordData();

                        dto.setCar_id(jsonArray.getJSONObject(i).get("car_id").toString());
                        dto.setStart_time(jsonArray.getJSONObject(i).get("start_time").toString());
                        dto.setEnd_time(jsonArray.getJSONObject(i).get("end_time").toString());
                        dto.setFuel_eft(jsonArray.getJSONObject(i).get("fuel_efi").toString());
                        dto.setSpeed(jsonArray.getJSONObject(i).get("speed").toString());
                        dto.setRpm(jsonArray.getJSONObject(i).get("rpm").toString());
                        dto.setBreak_num(jsonArray.getJSONObject(i).get("brk_num").toString());
                        dto.setAccel_num(jsonArray.getJSONObject(i).get("acl_num").toString());
                        dto.setScore(jsonArray.getJSONObject(i).get("score").toString());
                        dto.setDistance(jsonArray.getJSONObject(i).get("distance").toString());
                        dto.setPosition_json(jsonArray.getJSONObject(i).getJSONArray("position").toString());
                        dto.setDrive_json(jsonArray.getJSONObject(i).getJSONArray("drive").toString());
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