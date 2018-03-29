package com.example.kpu.googlelogintest.listview;

import android.app.FragmentManager;
import android.app.ProgressDialog;
import android.graphics.Color;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.EditText;
import android.widget.Toast;

import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.activitys.DrivingRecordActivity;
import com.example.kpu.googlelogintest.utills.PHPRequest;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolylineOptions;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.concurrent.ExecutionException;

public class DetailActivity extends AppCompatActivity implements OnMapReadyCallback {

    GoogleMap mMap;
    RecordData recordData;
    EditText t3,t4,t5,t6,t7,t8,t9,t10;
    PolylineOptions polylineOptions;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getSupportActionBar().hide(); // 엑션 바 감추기
        setContentView(R.layout.activity_detail);


        t3 = findViewById(R.id.editText_startTime);
        t4 = findViewById(R.id.editText_endTime);
        t5 = findViewById(R.id.editText_distance);
        t6 = findViewById(R.id.editText_fuel);
        t7 = findViewById(R.id.editText_score);
        t8 = findViewById(R.id.editText_speed);
        t9 = findViewById(R.id.editText_accel);
        t10 = findViewById(R.id.editText_break);
        recordData = (RecordData)getIntent().getSerializableExtra("data");


        t3.setText(recordData.getStart_time());
        t4.setText(recordData.getEnd_time());
        t5.setText(recordData.getDistance() + " Km");
        t6.setText(recordData.getFuel_eft() + " Km/L");
        t7.setText(recordData.getScore() + " 점");
        t8.setText(recordData.getSpeed() + " Km/h");
        t9.setText(recordData.getAccel_num() + " 번");
        t10.setText(recordData.getBreak_num() + " 번");

        FragmentManager fragmentManager = getFragmentManager();
        MapFragment mapFragment = (MapFragment)fragmentManager.findFragmentById(R.id.drive_map);
        mapFragment.getMapAsync(this);

    }


    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        // Add a marker in Sydney and move the camera




        polylineOptions = new PolylineOptions();

        try {
            JSONArray json = new JSONArray(recordData.getPosition_json());
            for(int i=0;i<json.length();i++) {
                polylineOptions.add(new LatLng(json.getJSONObject(i).getDouble("POS_X"),json.getJSONObject(i).getDouble("POS_Y")));
            }
            polylineOptions.color(Color.RED);
            mMap.addMarker(new MarkerOptions().position(new LatLng(json.getJSONObject(0).getDouble("POS_X"),json.getJSONObject(0).getDouble("POS_Y"))).title("Start!"));
            mMap.addMarker(new MarkerOptions().position(new LatLng(json.getJSONObject(json.length()-1).getDouble("POS_X"),json.getJSONObject(json.length()-1).getDouble("POS_Y"))).title("End!"));
            mMap.moveCamera(CameraUpdateFactory.newLatLng(new LatLng(json.getJSONObject(json.length()-1).getDouble("POS_X"),json.getJSONObject(json.length()-1).getDouble("POS_Y"))));

        } catch (JSONException e) {
            e.printStackTrace();
        }

        mMap.animateCamera(CameraUpdateFactory.zoomTo(11));
        mMap.addPolyline(polylineOptions);
    }


}
