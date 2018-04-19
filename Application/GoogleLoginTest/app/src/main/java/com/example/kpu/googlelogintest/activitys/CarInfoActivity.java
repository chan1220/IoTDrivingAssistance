package com.example.kpu.googlelogintest.activitys;

import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.EditText;
import android.widget.Toast;

import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.utills.PHPRequest;

import org.json.JSONArray;
import org.json.JSONException;

public class CarInfoActivity extends AppCompatActivity {
    private String id;

    EditText edt_name,edt_carname,edt_volume,edt_fuel,edt_fuel_efi,edt_carid;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_car_info);

        edt_carid   = findViewById(R.id.editText_carid);
        edt_carname = findViewById(R.id.editText_carname);
        edt_fuel    = findViewById(R.id.editText_fuel);
        edt_fuel_efi = findViewById(R.id.editText_fuel_efi);
        edt_name    = findViewById(R.id.editText_username);
        edt_volume  = findViewById(R.id.editText_volum);


        id = getIntent().getStringExtra("id");
        new BackgroundTask().execute();
        edt_name.setText(getIntent().getStringExtra("name"));

    }



    public class BackgroundTask extends AsyncTask<Void, Void, String>
    {
        ProgressDialog progressDialog = new ProgressDialog(CarInfoActivity.this);
        String car_info_json;

        @Override // 여기에 할 작업
        protected String doInBackground(Void... voids) {
            car_info_json = PHPRequest.execute(getString(R.string.server_url)+"/carinfo.php","id",id);
            return null;
        }


        @Override
        protected void onPreExecute() {
            super.onPreExecute();

            progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
            progressDialog.setMessage("검색중입니다...");
            progressDialog.show();
        }

        @Override
        protected void onPostExecute(String s) {
            super.onPostExecute(s);
            progressDialog.dismiss();
            JSONArray json = null;

            try {
                json = new JSONArray(car_info_json);
                if(json.length() <= 0) {
                    Toast.makeText(getApplicationContext(), "차량이 등록되있지 않습니다. \n먼저 차량을 등록해주세요.", Toast.LENGTH_LONG).show();
                    finish();
                }
                for(int i=0;i<json.length();i++) {
                    // json을 받아서 EdtiText에 설정
                    edt_carid.setText(json.getJSONObject(i).get("car_id").toString());
                    edt_carname.setText(json.getJSONObject(i).get("car_name").toString());
                    edt_volume.setText(json.getJSONObject(i).get("volume").toString() + " CC");
                    edt_fuel.setText(json.getJSONObject(i).get("fuel").toString());
                    edt_fuel_efi.setText(json.getJSONObject(i).get("fuel_efi").toString() + " Km/L");
                }
            } catch (JSONException e) {
                e.printStackTrace();
                Toast.makeText(getApplicationContext(), "Error!", Toast.LENGTH_LONG).show();
            }

        }

    }
}
