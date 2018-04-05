package com.example.kpu.googlelogintest.activitys;

import android.app.DatePickerDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.media.audiofx.Visualizer;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.listview.DetailActivity;
import com.example.kpu.googlelogintest.listview.RecordAdapter;
import com.example.kpu.googlelogintest.listview.RecordData;
import com.example.kpu.googlelogintest.utills.PHPRequest;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.Date;

public class DrivingRecordActivity extends AppCompatActivity {

    private RecordAdapter adapter;
    private ListView listView;
    private Button button_search;
    Button start_time, end_time;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_driving_record);

        adapter = new RecordAdapter();
        listView = findViewById(R.id.listView);
        button_search = findViewById(R.id.button_search);
        start_time = findViewById(R.id.input_start);
        end_time = findViewById(R.id.input_end);

        listView.setAdapter(adapter);

        DatePickerDialog.OnDateSetListener startDateListener = new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int i, int i1, int i2) {
                start_time.setText(i + "-" + String.format("%02d",(i1+1)) + "-" + String.format("%02d",i2));
            }
        };ra
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
                adapter.clearItem();
                new BackgroundTask().execute();
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
                RecordData recordData = (RecordData)adapter.getItem(position);

                // new Intent(현재 Activity의 Context, 시작할 Activity 클래스)
                Intent intent = new Intent(DrivingRecordActivity.this, DetailActivity.class);
                // putExtra(key, value)
                intent.putExtra("data", recordData);
                startActivity(intent);
            }
        });






    }


    private boolean setData() {
        String userid = getIntent().getStringExtra("id");
        String json_result = PHPRequest.execute(getText(R.string.server_url)+"/drive_record.php","usr_id",userid,"start_time",start_time.getText().toString(),"end_time",end_time.getText().toString());
        try {
            JSONArray json = new JSONArray(json_result);
            if(json.length() <= 0) {
                //Toast.makeText(this, "찾는 결과가 없습니다.", Toast.LENGTH_LONG).show();
                return false;
            }
            for(int i=0;i<json.length();i++) {

                RecordData dto = new RecordData();
                String json_position = PHPRequest.execute(getText(R.string.server_url)+"/get_position.php","car_id",json.getJSONObject(i).get("CAR_ID").toString(),"START_TIME",json.getJSONObject(i).get("START_TIME").toString(),"end_time",json.getJSONObject(i).get("END_TIME").toString());

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
                dto.setPosition_json(json_position);
                adapter.addItem(dto);
            }

        } catch (JSONException e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }


    public class BackgroundTask extends AsyncTask<Void, Void, Boolean>
    {
        ProgressDialog progressDialog = new ProgressDialog(DrivingRecordActivity.this);


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
            adapter.notifyDataSetChanged();
            progressDialog.dismiss();
            Log.d("Background","프로그레스 바 종료");
        }
    }
}
