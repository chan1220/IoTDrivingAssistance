package com.example.kpu.googlelogintest.listview;

import android.app.FragmentManager;
import android.app.ProgressDialog;
import android.graphics.Color;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.EditText;
import android.widget.TextView;
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

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.ExecutionException;

public class DetailActivity extends AppCompatActivity implements OnMapReadyCallback {

    GoogleMap mMap;
    RecordData recordData;
    TextView tv_speed, tv_start, tv_end, tv_distance, tv_score, tv_accel, tv_break, tv_fuel;
    PolylineOptions polylineOptions;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getSupportActionBar().hide(); // 엑션 바 감추기
        setContentView(R.layout.activity_detail);


        tv_start = findViewById(R.id.tv_start);
        tv_end = findViewById(R.id.tv_end);
        tv_distance = findViewById(R.id.tv_distance);
        tv_fuel = findViewById(R.id.tv_fuel);
        tv_score = findViewById(R.id.tv_score);
        tv_speed = findViewById(R.id.tv_speed);
        tv_accel = findViewById(R.id.tv_accel);
        tv_break = findViewById(R.id.tv_break);

        recordData = (RecordData)getIntent().getSerializableExtra("data");
        Date start=null, end = null;
        try {
            start = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").parse(recordData.getStart_time());
            end = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").parse(recordData.getEnd_time());
        } catch (ParseException e) {
            e.printStackTrace();
        }

        tv_start.setText(new SimpleDateFormat("yyyy년MM월dd일 HH시mm분").format(start));
        tv_end.setText(new SimpleDateFormat("yyyy년MM월dd일 HH시mm분").format(end));
        tv_distance.setText(String.format("%.1f",Double.parseDouble(recordData.getDistance())) + " Km");
        tv_fuel.setText(String.format("%.1f",Double.parseDouble(recordData.getFuel_eft())) + " Km/L");
        tv_score.setText(recordData.getScore() + " 점");
        tv_speed.setText(String.format("%.1f",Double.parseDouble(recordData.getSpeed())) + " Km/h");
        tv_accel.setText(recordData.getAccel_num() + " 번");
        tv_break.setText(recordData.getBreak_num() + " 번");

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
                polylineOptions.add(new LatLng(json.getJSONObject(i).getDouble("pos_x"),json.getJSONObject(i).getDouble("pos_y")));
            }
            polylineOptions.color(Color.RED);
            mMap.addMarker(new MarkerOptions().position(new LatLng(json.getJSONObject(0).getDouble("pos_x"),json.getJSONObject(0).getDouble("pos_y"))).title("Start!"));
            mMap.addMarker(new MarkerOptions().position(new LatLng(json.getJSONObject(json.length()-1).getDouble("pos_x"),json.getJSONObject(json.length()-1).getDouble("pos_y"))).title("End!"));
            mMap.moveCamera(CameraUpdateFactory.newLatLng(new LatLng(json.getJSONObject(json.length()-1).getDouble("pos_x"),json.getJSONObject(json.length()-1).getDouble("pos_y"))));

        } catch (JSONException e) {
            e.printStackTrace();
        }

        mMap.animateCamera(CameraUpdateFactory.zoomTo(11));
        mMap.addPolyline(polylineOptions);
    }


}
