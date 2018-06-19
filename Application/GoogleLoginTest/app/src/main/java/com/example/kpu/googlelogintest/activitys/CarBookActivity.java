package com.example.kpu.googlelogintest.activitys;

import android.app.DatePickerDialog;
import android.app.ProgressDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.Toast;

import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.listview.RecordData;
import com.example.kpu.googlelogintest.utills.DBRequester;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class CarBookActivity extends AppCompatActivity implements DBRequester.Listener {

    Button start_time, end_time;
    Button button_search;
    ArrayList<RecordData> recordArray;
    EditText edt_fef, edt_fuel, edt_distance, edt_date;
    ProgressDialog progressDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_car_book);
        setTitle("차계부");

        start_time = findViewById(R.id.start_date);
        end_time = findViewById(R.id.end_date);

        edt_fef = findViewById(R.id.edt_fef);
        edt_fuel = findViewById(R.id.edt_fuel);
        edt_distance = findViewById(R.id.edt_distance);
        button_search = findViewById(R.id.search);
        edt_date = findViewById(R.id.edt_date);

        progressDialog = new ProgressDialog(CarBookActivity.this);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setMessage("검색중입니다...");

        recordArray = new ArrayList<RecordData>();

        DatePickerDialog.OnDateSetListener startDateListener = new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int i, int i1, int i2) {
                start_time.setText(i + "-" + String.format("%02d", (i1 + 1)) + "-" + String.format("%02d", i2));
            }
        };
        final DatePickerDialog startDateDialog = new DatePickerDialog(this, startDateListener, 2018, 03, 01);

        DatePickerDialog.OnDateSetListener endtDateListener = new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int i, int i1, int i2) {
                end_time.setText(i + "-" + String.format("%02d", (i1 + 1)) + "-" + String.format("%02d", i2));
            }
        };
        final DatePickerDialog endDateDialog = new DatePickerDialog(this, endtDateListener, 2018, 03, 01);


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
                recordArray.clear();
                progressDialog.show();
                try {
                    JSONObject param = new JSONObject();
                    param.put("usr_id", getIntent().getStringExtra("id"));
                    param.put("start_date", start_time.getText().toString());
                    param.put("end_date", end_time.getText().toString());

                    new DBRequester.Builder(CarBookActivity.this, "http://49.236.136.179:5000", CarBookActivity.this)
                            .attach("request/record")
                            .streamPost(param)
                            .request("request record");

                } catch (JSONException e) {
                    e.printStackTrace();
                }

            }
        });

    }

    @Override
    public void onResponse(String id, JSONObject json, Object... params) {
        try {
            if (json.getBoolean("success") == false) {
                Toast.makeText(this, "로드 실패", Toast.LENGTH_SHORT).show();
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

                        recordArray.add(dto);
                    }

                    double total_fuel = 0;
                    double total_dis = 0;


                    for (RecordData rd : recordArray) {
                        total_fuel += Double.parseDouble(rd.getDistance()) / Double.parseDouble(rd.getFuel_eft());
                        total_dis += Double.parseDouble(rd.getDistance());
                    }
                    progressDialog.dismiss();

                    edt_date.setText("< " + start_time.getText().toString() + " ~ " + end_time.getText().toString() + " >");
                    edt_distance.setText("총 주행거리 : " + String.format("%.1f", total_dis) + " Km");
                    edt_fuel.setText("기름 사용량 : " + String.format("%.2f", total_fuel) + " L");
                    if(total_fuel == 0)
                        edt_fef.setText("주행 기록이 없습니다.");
                    else
                        edt_fef.setText("평균연비 : " + String.format("%.2f", total_dis / total_fuel) + " Km/L");
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