package com.example.kpu.googlelogintest.activitys;

import android.app.ProgressDialog;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.EditText;
import android.widget.Toast;

import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.listview.RecordData;
import com.example.kpu.googlelogintest.utills.DBRequester;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class FuelefficiencyActivity extends AppCompatActivity implements DBRequester.Listener{

    private EditText edt_fef, edt_score, edt_break, edt_accel, edt_distance;
    private ArrayList<RecordData> recordArray;
    private ProgressDialog progressDialog;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_fuelefficiency);

        edt_fef = findViewById(R.id.edt_fef);
        edt_score = findViewById(R.id.edt_score);
        edt_break = findViewById(R.id.edt_break);
        edt_accel = findViewById(R.id.edt_accel);
        edt_distance = findViewById(R.id.edt_distance);
        progressDialog = new ProgressDialog(FuelefficiencyActivity.this);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setMessage("검색중입니다...");
        setTitle("연비 확인");

        recordArray = new ArrayList<RecordData>();

        progressDialog.show();
        try {
            JSONObject param = new JSONObject();
            param.put("usr_id", getIntent().getStringExtra("id"));
            param.put("start_date", "1981-12-20");
            param.put("end_date", "2100-12-20");

            new DBRequester.Builder(this, "http://49.236.136.179:5000", this)
                    .attach("request/record")
                    .streamPost(param)
                    .request("request record");

        } catch (JSONException e) {
            e.printStackTrace();
        }

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
                    int total_break = 0;
                    int total_accel = 0;
                    int total_score = 0;

                    for(RecordData rd : recordArray)
                    {
                        total_fuel += Double.parseDouble(rd.getDistance()) / Double.parseDouble(rd.getFuel_eft());
                        total_dis += Double.parseDouble(rd.getDistance());
                        total_score += Double.parseDouble(rd.getScore());
                        total_accel += Double.parseDouble(rd.getAccel_num());
                        total_break += Double.parseDouble(rd.getBreak_num());
                    }
                    progressDialog.dismiss();
                    edt_fef.setText("" + String.format("%.2f", total_dis / total_fuel));
                    edt_score.setText(""+total_score / recordArray.size());
                    edt_break.setText(""+ String.format("%.2f", total_break * 10 / total_dis));
                    edt_accel.setText(""+ String.format("%.2f", total_accel * 10 / total_dis));
                    edt_distance.setText("" + String.format("%.2f", total_dis));
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
