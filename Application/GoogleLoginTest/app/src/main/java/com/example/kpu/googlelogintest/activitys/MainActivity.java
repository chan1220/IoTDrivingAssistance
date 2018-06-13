package com.example.kpu.googlelogintest.activitys;

import android.app.FragmentManager;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.os.StrictMode;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.NavigationView;
import android.support.design.widget.Snackbar;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.utills.DBRequester;
import com.github.mikephil.charting.charts.PieChart;
import com.github.mikephil.charting.data.PieData;
import com.github.mikephil.charting.data.PieDataSet;
import com.github.mikephil.charting.data.PieEntry;
import com.github.mikephil.charting.formatter.PercentFormatter;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolylineOptions;
import com.google.firebase.auth.FirebaseAuth;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener, OnMapReadyCallback, DBRequester.Listener {

    private Intent intent;
    private TextView textView_greet;
    private GoogleMap parking_map;
    private GoogleMap course_map;
    private TextView recent_drive, recent_drive_values;
    private PieChart drive_total_chart;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView_greet = findViewById(R.id.textView_greet);
        recent_drive = findViewById(R.id.textView_recent_drive);
        recent_drive_values = findViewById(R.id.textView_recent_drive_values);
        drive_total_chart = findViewById(R.id.drive_total_chart);
        // google map init
        FragmentManager fragmentManager = getFragmentManager();
        MapFragment mapFragment1 = (MapFragment)fragmentManager.findFragmentById(R.id.parking_map);
        mapFragment1.getMapAsync(this);
        MapFragment mapFragment2 = (MapFragment)fragmentManager.findFragmentById(R.id.course_map);
        mapFragment2.getMapAsync(onMapReadyCallback());
        //


        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "메롱 -_-", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });
        setTitle(" ");

        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);

        textView_greet.setText(getIntent().getStringExtra("name")+" 님 환영합니다!");



        intent = new Intent(this.getIntent());

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        try {
            JSONObject param = new JSONObject();
            param.put("usr_id", getIntent().getStringExtra("id"));

            new DBRequester.Builder(MainActivity.this, "http://49.236.136.179:5000", this)
                    .attach("request/chart")
                    .streamPost(param)
                    .request("request chart");

        } catch (JSONException e) {
            e.printStackTrace();
        }

    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            FirebaseAuth.getInstance().signOut();
            Intent intent = new Intent(MainActivity.this, LoginActivity.class);
            startActivity(intent);
            finish();
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_reg_car) {
            // 차량 등록 버튼
            Intent intent_reg=new Intent(MainActivity.this, CarRegisterActivity.class);
            intent_reg.putExtra("id",intent.getStringExtra("id"));
            startActivity(intent_reg);
        } else if (id == R.id.nav_record) {
            // 주행 기록
            Intent intent_rec=new Intent(MainActivity.this, DrivingRecordActivity.class);
            intent_rec.putExtra("id",intent.getStringExtra("id"));
            intent_rec.putExtra("name",intent.getStringExtra("name"));
            startActivity(intent_rec);
        } else if (id == R.id.nav_car_info) {
            // 차량 정보
            Intent intent_car=new Intent(MainActivity.this, CarInfoActivity.class);
            intent_car.putExtra("id",intent.getStringExtra("id"));
            intent_car.putExtra("name",intent.getStringExtra("name"));
            startActivity(intent_car);

        } else if (id == R.id.nav_efi) {
            // 연비 확인
            Intent intent_fef=new Intent(MainActivity.this, FuelefficiencyActivity.class);
            intent_fef.putExtra("id",intent.getStringExtra("id"));
            startActivity(intent_fef);
        } else if (id == R.id.nav_score) {
            // 주행 점수
        } else if (id == R.id.nav_book) {
            // 차계부
            Intent intent_carbook=new Intent(MainActivity.this, CarBookActivity.class);
            intent_carbook.putExtra("id",intent.getStringExtra("id"));
            intent_carbook.putExtra("name",intent.getStringExtra("name"));
            startActivity(intent_carbook);
        } else if (id == R.id.nav_info) {
            Intent intent_info=new Intent(MainActivity.this, InformationActivity.class);
            startActivity(intent_info);
            // 어플 정보
        }

        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }


    @Override
    public void onMapReady(GoogleMap googleMap) {
        parking_map = googleMap;
        try {
            JSONObject param = new JSONObject();
            param.put("usr_id", getIntent().getStringExtra("id"));

            new DBRequester.Builder(MainActivity.this, "http://49.236.136.179:5000", this)
                    .attach("request/parking")
                    .streamPost(param)
                    .request("request parking");

        } catch (JSONException e) {
            e.printStackTrace();
        }

    }

    public OnMapReadyCallback onMapReadyCallback(){
        return new OnMapReadyCallback() {
            @Override
            public void onMapReady(GoogleMap googleMap) {
                course_map = googleMap;
                try {
                    JSONObject param = new JSONObject();
                    param.put("usr_id", getIntent().getStringExtra("id"));

                    new DBRequester.Builder(MainActivity.this, "http://49.236.136.179:5000", MainActivity.this)
                            .attach("request/record_recent")
                            .streamPost(param)
                            .request("request record_recent");

                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        };
    }
    @Override
    public void onResponse(String id, JSONObject json, Object... params) {
        try {
            if (json.getBoolean("success") == false) {
                Toast.makeText(this, "로드 실패", Toast.LENGTH_SHORT).show();
                return;
            }

            switch (id) {
                case "request parking":
                    JSONArray jsonArray = json.getJSONArray("data");
                    parking_map.addMarker(new MarkerOptions().position(new LatLng(jsonArray.getJSONObject(0).getDouble("pos_x"),jsonArray.getJSONObject(0).getDouble("pos_y"))).title(jsonArray.getJSONObject(0).getString("pos_time")));
                    parking_map.moveCamera(CameraUpdateFactory.newLatLng(new LatLng(jsonArray.getJSONObject(0).getDouble("pos_x"),jsonArray.getJSONObject(0).getDouble("pos_y"))));
                    parking_map.animateCamera(CameraUpdateFactory.zoomTo(18));
                    break;

                case "request record_recent":
                    JSONArray jsonRecordArray = json.getJSONArray("data");


                    PolylineOptions polylineOptions = new PolylineOptions();

                    try {
                        JSONArray recentPosition = new JSONArray(jsonRecordArray.getJSONObject(0).getString("position"));
                        for(int i=0;i<recentPosition.length();i++) {
                            polylineOptions.add(new LatLng(recentPosition.getJSONObject(i).getDouble("lat"),recentPosition.getJSONObject(i).getDouble("lon")));
                        }
                        polylineOptions.color(Color.RED);
                        course_map.addMarker(new MarkerOptions().position(new LatLng(recentPosition.getJSONObject(0).getDouble("lat"),recentPosition.getJSONObject(0).getDouble("lon"))).title("Start!"));
                        course_map.addMarker(new MarkerOptions().position(new LatLng(recentPosition.getJSONObject(recentPosition.length()-1).getDouble("lat"),recentPosition.getJSONObject(recentPosition.length()-1).getDouble("lon"))).title("End!"));
                        course_map.moveCamera(CameraUpdateFactory.newLatLng(new LatLng(recentPosition.getJSONObject(recentPosition.length()-1).getDouble("lat"),recentPosition.getJSONObject(recentPosition.length()-1).getDouble("lon"))));

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                    course_map.animateCamera(CameraUpdateFactory.zoomTo(11));
                    course_map.addPolyline(polylineOptions);
                    recent_drive.setText("- 최근 주행 기록(" + jsonRecordArray.getJSONObject(0).getString("start_time") + ")");
                    recent_drive_values.setText("거리 : " + String.format("%.2f", jsonRecordArray.getJSONObject(0).getDouble("distance")) + "km, 연비 : " + String.format("%.2f" ,jsonRecordArray.getJSONObject(0).getDouble("fuel_efi")) + "L/Km");
                    break;

                case "request chart":
                    JSONArray chartJson = json.getJSONArray("data");

                    List<PieEntry> entries = new ArrayList<>();

                    entries.add(new PieEntry((float) chartJson.getJSONObject(0).getDouble("idle"), "공회전"));
                    entries.add(new PieEntry((float) chartJson.getJSONObject(0).getDouble("bad"), "비경제운전"));
                    entries.add(new PieEntry((float) chartJson.getJSONObject(0).getDouble("normal"), "보통운전"));
                    entries.add(new PieEntry((float) chartJson.getJSONObject(0).getDouble("good"), "경제운전"));

                    PieDataSet pieDataSet = new PieDataSet(entries, "주행그래프");
                    PieData pieData = new PieData(pieDataSet);

                    int color_arr[] = { Color.BLACK, Color.RED, Color.YELLOW, Color.GREEN };
                    pieDataSet.setColors(color_arr, 60); // 속성색깔

                    pieData.setValueFormatter(new PercentFormatter());
                    drive_total_chart.setData(pieData);
                    drive_total_chart.animateY(2000);



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
