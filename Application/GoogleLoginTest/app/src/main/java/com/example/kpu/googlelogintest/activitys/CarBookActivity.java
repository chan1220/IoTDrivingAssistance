package com.example.kpu.googlelogintest.activitys;

import android.app.DatePickerDialog;
import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;

import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.listview.RecordData;
import com.example.kpu.googlelogintest.utills.PHPRequest;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.ArrayList;

public class CarBookActivity extends AppCompatActivity {

    Button start_time, end_time;
    Button button_search;
    ArrayList<RecordData> recordArray;
    EditText testEdt;
    double total_fuel = 0;
    double total_dis = 0;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_car_book);


        start_time = findViewById(R.id.start_date);
        end_time = findViewById(R.id.end_date);
        button_search = findViewById(R.id.search);
        testEdt = findViewById(R.id.edtTest);
        recordArray = new ArrayList<RecordData>();

        DatePickerDialog.OnDateSetListener startDateListener = new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int i, int i1, int i2) {
                start_time.setText(i + "-" + String.format("%02d",(i1+1)) + "-" + String.format("%02d",i2));
            }
        };
        final DatePickerDialog startDateDialog = new DatePickerDialog(this,startDateListener,2018,03,01);

        DatePickerDialog.OnDateSetListener endtDateListener = new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int i, int i1, int i2) {
                end_time.setText(i + "-" + String.format("%02d",(i1+1)) + "-" + String.format("%02d",i2));
            }
        };
        final DatePickerDialog endDateDialog = new DatePickerDialog(this,endtDateListener,2018,03,01);



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
                new BackgroundTask().execute();
            }
        });



    }



    private boolean setData() {
        String userid = getIntent().getStringExtra("id");
        String json_result = PHPRequest.execute(getText(R.string.server_url)+"/drive_record.php","usr_id",userid,"start_time",start_time.getText().toString(),"end_time",end_time.getText().toString());
        try {
            if(json_result == null)
                return false;
            JSONArray json = new JSONArray(json_result);
            if(json.length() <= 0) {
                //Toast.makeText(this, "찾는 결과가 없습니다.", Toast.LENGTH_LONG).show();
                return false;
            }
            for(int i=0;i<json.length();i++) {


                RecordData dto = new RecordData();
                //String json_position = PHPRequest.execute(getText(R.string.server_url)+"/get_position.php","car_id",json.getJSONObject(i).get("CAR_ID").toString(),"START_TIME",json.getJSONObject(i).get("START_TIME").toString(),"end_time",json.getJSONObject(i).get("END_TIME").toString());
                dto.setCar_id(json.getJSONObject(i).get("CAR_ID").toString());
                dto.setStart_time(json.getJSONObject(i).get("START_TIME").toString());
                dto.setEnd_time(json.getJSONObject(i).get("END_TIME").toString());
                dto.setFuel_eft(json.getJSONObject(i).get("FUEL_EFI").toString());
                dto.setSpeed(json.getJSONObject(i).get("SPEED").toString());
                dto.setRpm(json.getJSONObject(i).get("RPM").toString());
                dto.setBreak_num(json.getJSONObject(i).get("BRK_NUM").toString());
                dto.setAccel_num(json.getJSONObject(i).get("ACL_NUM").toString());
                dto.setScore(json.getJSONObject(i).get("SCORE").toString());
                dto.setDistance(json.getJSONObject(i).get("DISTANCE").toString());
                //dto.setPosition_json(json_position);
                Log.d("차계부 테스트",json.getJSONObject(i).get("FUEL_EFI").toString());
                recordArray.add(dto);
            }


        } catch (JSONException e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }


    public class BackgroundTask extends AsyncTask<Void, Void, Boolean>
    {
        ProgressDialog progressDialog = new ProgressDialog(CarBookActivity.this);


        @Override // 여기에 할 작업
        protected Boolean doInBackground(Void... voids) {
            return setData();
        }


        @Override
        protected void onPreExecute() {
            super.onPreExecute();

            progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
            progressDialog.setMessage("검색중입니다...");
            progressDialog.show();
        }


        @Override
        protected void onPostExecute(Boolean aBoolean) {
            super.onPostExecute(aBoolean);
            progressDialog.dismiss();
            Log.d("Background","프로그레스 바 종료");

            total_dis = 0;
            total_fuel = 0;
            for(RecordData rd : recordArray)
            {
                total_fuel += Double.parseDouble(rd.getDistance()) / Double.parseDouble(rd.getFuel_eft());
                total_dis += Double.parseDouble(rd.getDistance());
            }

            testEdt.setText("평균연비 : "+ total_dis / total_fuel + "Km/L, 총 주행거리 : "+total_dis + "Km, 기름 사용량 : "+total_fuel+"L");
        }
    }
}
