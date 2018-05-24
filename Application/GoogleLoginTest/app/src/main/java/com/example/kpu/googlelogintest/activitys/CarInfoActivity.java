package com.example.kpu.googlelogintest.activitys;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.EditText;

import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.utills.DBRequester;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class CarInfoActivity extends AppCompatActivity implements DBRequester.Listener{
    private String usr_id;

    EditText edt_name,edt_carname,edt_volume,edt_fuel,edt_fuel_efi,edt_carid;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_car_info);
        setTitle("차량 정보");
        edt_carid   = findViewById(R.id.editText_carid);
        edt_carname = findViewById(R.id.editText_carname);
        edt_fuel    = findViewById(R.id.editText_fuel);
        edt_fuel_efi = findViewById(R.id.editText_fuel_efi);
        edt_name    = findViewById(R.id.editText_username);
        edt_volume  = findViewById(R.id.editText_volum);

        edt_name.setText(getIntent().getStringExtra("name"));
        usr_id = getIntent().getStringExtra("id");

        // 실행!
        try {
            JSONObject car = new JSONObject();
            car.put("usr_id", usr_id);
            new DBRequester.Builder(this, "http://49.236.136.179:5000", this)
                    .attach("request/car")
                    .streamPost(car)
                    .request("request car");


        } catch (JSONException e) {
            e.printStackTrace();
        }

    }

    @Override
    public void onResponse(String id, JSONObject json, Object... params) {
        try {
            if(json.getBoolean("success") == false)
                return;

            switch(id) {
                case "request car":
                    JSONArray jsonArray = json.getJSONArray("data");
                    JSONObject data = jsonArray.getJSONObject(0);
                    edt_carid.setText(data.getString("car_id"));
                    edt_carname.setText(data.getString("car_name"));
                    edt_volume.setText(data.getString("volume"));
                    edt_fuel.setText(data.getString("fuel"));
                    edt_fuel_efi.setText(data.getString("fuel_efi"));
                    break;
            }
        } catch (Exception e) {
            Log.d("on response", e.getMessage());
        }
    }

    @Override
    public void onResponse(String id, JSONArray json, Object... params) {

    }

    @Override
    public void onError(String id, String message, Object... params) {

    }
}
