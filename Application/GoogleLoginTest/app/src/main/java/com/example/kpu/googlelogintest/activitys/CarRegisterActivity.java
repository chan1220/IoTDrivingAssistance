package com.example.kpu.googlelogintest.activitys;

import android.content.DialogInterface;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.utills.DBRequester;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class CarRegisterActivity extends AppCompatActivity implements DBRequester.Listener {
    private Button btn_submit;
    private EditText edt_usr_id, edt_car_id, edt_car_name, edt_volum, edt_fuel_efi, edt_fuel;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_car_register);
        setTitle("차량 등록");

        edt_usr_id = findViewById(R.id.cr_userid);
        edt_car_id = findViewById(R.id.cr_carid);
        edt_car_name = findViewById(R.id.cr_carname);
        edt_volum = findViewById(R.id.cr_volum);
        edt_fuel_efi = findViewById(R.id.cr_fuel_efi);
        edt_fuel = findViewById(R.id.cr_fuel);

        btn_submit = findViewById(R.id.cr_submit);


        edt_usr_id.setText(getIntent().getStringExtra("id"));

        // 등록된 차량 정보 확인
        try {
            JSONObject car = new JSONObject();
            car.put("usr_id", getIntent().getStringExtra("id"));
            new DBRequester.Builder(this, "http://49.236.136.179:5000", this)
                    .attach("request/car")
                    .streamPost(car)
                    .request("request car");


        } catch (JSONException e) {
            e.printStackTrace();
        }


        // 버튼클릭시 등록
        btn_submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    JSONObject car = new JSONObject();
                    car.put("car_id", edt_car_id.getText());
                    car.put("usr_id", edt_usr_id.getText());
                    car.put("car_name", edt_car_name.getText());
                    car.put("volume", edt_volum.getText());
                    car.put("fuel_efi", edt_fuel_efi.getText());
                    car.put("fuel", edt_fuel.getText());

                    new DBRequester.Builder(CarRegisterActivity.this, "http://49.236.136.179:5000", CarRegisterActivity.this)
                            .attach("update/car")
                            .streamPost(car)
                            .request("update car");

                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    @Override
    public void onResponse(String id, JSONObject json, Object... params) {
        try {

            switch (id){
                case "update car":
                    if(json.getBoolean("success") == false)
                        Toast.makeText(this, "등록 실패", Toast.LENGTH_SHORT).show();
                    else{
                        Toast.makeText(this, "정상적으로 등록되었습니다.", Toast.LENGTH_SHORT).show();
                        finish();
                    }
                    break;

                case "request car":
                    JSONArray jsonArray = json.getJSONArray("data");

                    if(jsonArray.length() > 0) {
                        AlertDialog.Builder alert_confirm = new AlertDialog.Builder(CarRegisterActivity.this);
                        alert_confirm.setMessage("이미 차량이 등록되어있습니다.\n 수정하시겠습니까?").setCancelable(false).setPositiveButton("네",
                                new DialogInterface.OnClickListener() {
                                    @Override
                                    public void onClick(DialogInterface dialog, int which) {
                                        // 'YES'
                                        return;
                                    }
                                }).setNegativeButton("아니요",
                                new DialogInterface.OnClickListener() {
                                    @Override
                                    public void onClick(DialogInterface dialog, int which) {
                                        finish();
                                        return;
                                    }
                                });
                        AlertDialog alert = alert_confirm.create();
                        alert.show();

                        JSONObject data = jsonArray.getJSONObject(0);
                        edt_car_id.setText(data.getString("car_id"));
                        edt_car_name.setText(data.getString("car_name"));
                        edt_volum.setText(data.getString("volume"));
//                        edt_fuel.setText(data.getString("fuel"));
                        edt_fuel_efi.setText(data.getString("fuel_efi"));
                    }
                    break;
            }

        } catch (JSONException e) {
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
