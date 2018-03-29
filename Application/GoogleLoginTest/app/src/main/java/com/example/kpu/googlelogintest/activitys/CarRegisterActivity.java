package com.example.kpu.googlelogintest.activitys;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.utills.PHPRequest;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.concurrent.ExecutionException;

public class CarRegisterActivity extends AppCompatActivity {
    Button btn_submit;
    EditText edt_userid, edt_carid, edt_carname, edt_volum, edt_fuelefi;
    Spinner spn_fuel;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_car_register);


        edt_userid  = findViewById(R.id.editText_userid);
        edt_carid   = findViewById(R.id.editText_carid);
        edt_carname = findViewById(R.id.editText_carname);
        edt_volum   = findViewById(R.id.editText_volum);
        edt_fuelefi = findViewById(R.id.editText_fuel_efi);
        spn_fuel    = findViewById(R.id.spinner_fuel);
        btn_submit = findViewById(R.id.button_submit);

        if(isRegestered())
        {
            Toast.makeText(getApplicationContext(), "이미 등록되어있습니다", Toast.LENGTH_LONG).show();
            finish();
        }
        else
            Toast.makeText(getApplicationContext(),"등록되있지 않네요",Toast.LENGTH_LONG).show();


        final Intent intent=new Intent(this.getIntent());

        edt_userid.setText(intent.getStringExtra("id"));

        btn_submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    String get_str  = new BackgroundTask().execute(
                            getString(R.string.server_url)+"/register_car.php",
                            "car_id",edt_carid.getText().toString(),
                            "usr_id",edt_userid.getText().toString(),
                            "car_name",edt_carname.getText().toString(),
                            "volume",edt_volum.getText().toString(),
                            "fuel",spn_fuel.getAdapter().getItem(spn_fuel.getSelectedItemPosition()).toString(),
                            "fuel_efi",edt_fuelefi.getText().toString()
                    ).get();
                    if(get_str.equals("-1")) {
                        Toast.makeText(getApplicationContext(), "헐 개망", Toast.LENGTH_LONG).show();
                    }
                    else {
                        Toast.makeText(getApplicationContext(), "등록 성공!!!", Toast.LENGTH_LONG).show();
                        finish();
                    }

                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (ExecutionException e) {
                    e.printStackTrace();
                }
            }
        });
    }






    public class BackgroundTask extends AsyncTask<String,Void,String>
    {
        ProgressDialog progressDialog = new ProgressDialog(CarRegisterActivity.this);

        @Override
        protected void onPostExecute(String s) {
            super.onPostExecute(s);
            progressDialog.dismiss();
        }

        @Override // 여기에 할 작업
        protected String doInBackground(String... strings) {
            return PHPRequest.execute(strings);



        }
        @Override
        protected void onPreExecute() {
            progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
            progressDialog.setMessage("Loading...");
            progressDialog.show();
            super.onPreExecute();
        }

    }


    private boolean isRegestered()
    {
        try {
            String json_str = PHPRequest.execute(getText(R.string.server_url)+"/is_registered.php","id",getIntent().getStringExtra("id"));
            if(json_str.equals("-1") || json_str == null)
                return false;

            JSONArray json = new JSONArray(json_str);
            if(json.length() > 0)
                return true;
            else
                return false;
        } catch (JSONException e) {
            e.printStackTrace();
            return false;
        }
    }






}
