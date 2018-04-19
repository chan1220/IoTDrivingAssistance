package com.example.kpu.googlelogintest.activitys;

import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.EditText;

import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.listview.RecordData;
import com.example.kpu.googlelogintest.utills.PHPRequest;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.ArrayList;

public class FuelefficiencyActivity extends AppCompatActivity {

    EditText edt_fef, edt_score, edt_break, edt_accel;
    ArrayList<RecordData> recordArray;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_fuelefficiency);

        edt_fef = findViewById(R.id.edt_fef);
        edt_score = findViewById(R.id.edt_score);
        edt_break = findViewById(R.id.edt_break);
        edt_accel = findViewById(R.id.edt_accel);

        recordArray = new ArrayList<RecordData>();

        new BackgroundTask().execute();
    }





    private boolean setData() {
        String userid = getIntent().getStringExtra("id");
        String json_result = PHPRequest.execute(getText(R.string.server_url)+"/drive_record.php","usr_id",userid,"start_time","1980-01-01","end_time","2100-12-31");
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
                dto.setCar_id(json.getJSONObject(i).get("car_id").toString());
                dto.setStart_time(json.getJSONObject(i).get("start_time").toString());
                dto.setEnd_time(json.getJSONObject(i).get("end_time").toString());
                dto.setFuel_eft(json.getJSONObject(i).get("fuel_efi").toString());
                dto.setSpeed(json.getJSONObject(i).get("speed").toString());
                dto.setRpm(json.getJSONObject(i).get("rpm").toString());
                dto.setBreak_num(json.getJSONObject(i).get("brk_num").toString());
                dto.setAccel_num(json.getJSONObject(i).get("acl_num").toString());
                dto.setScore(json.getJSONObject(i).get("score").toString());
                dto.setDistance(json.getJSONObject(i).get("distance").toString());
                //dto.setPosition_json(json_position);
                Log.d("차계부 테스트",json.getJSONObject(i).get("fuel_efi").toString());
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
        double total_fuel = 0;
        double total_dis = 0;
        int total_break = 0;
        int total_accel = 0;
        int total_score = 0;
        ProgressDialog progressDialog = new ProgressDialog(FuelefficiencyActivity.this);


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

            for(RecordData rd : recordArray)
            {
                total_fuel += Double.parseDouble(rd.getDistance()) / Double.parseDouble(rd.getFuel_eft());
                total_dis += Double.parseDouble(rd.getDistance());
                total_score += Integer.parseInt(rd.getScore());
                total_accel += Integer.parseInt(rd.getAccel_num());
            }
            edt_fef.setText("" + total_dis / total_fuel);
            edt_score.setText(""+total_score / recordArray.size());
            edt_break.setText(""+ total_break / total_dis);
            edt_accel.setText(""+total_break / total_dis);
        }
    }
}
