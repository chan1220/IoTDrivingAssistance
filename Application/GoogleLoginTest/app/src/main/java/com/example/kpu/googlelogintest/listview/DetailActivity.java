package com.example.kpu.googlelogintest.listview;

import android.app.FragmentManager;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;

import com.example.kpu.googlelogintest.R;
import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.charts.PieChart;
import com.github.mikephil.charting.components.AxisBase;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.data.PieData;
import com.github.mikephil.charting.data.PieDataSet;
import com.github.mikephil.charting.data.PieEntry;
import com.github.mikephil.charting.formatter.IAxisValueFormatter;
import com.github.mikephil.charting.formatter.PercentFormatter;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolylineOptions;

import org.json.JSONArray;
import org.json.JSONException;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class DetailActivity extends AppCompatActivity implements OnMapReadyCallback {

    GoogleMap mMap;
    RecordData recordData;
    TextView tv_speed, tv_start, tv_end, tv_distance, tv_score, tv_accel, tv_break, tv_fuel;
    PolylineOptions polylineOptions;
    PieChart chart_drive;
    LineChart chart_speed;
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

        chart_drive = findViewById(R.id.drive_chart);
        chart_speed = findViewById(R.id.speed_chart);

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




        // 차트 테스트


        try {
            float idle = 0f;
            float bottom = 0f;
            float mid = 0f;
            float top = 0f;

            List<PieEntry> entries = new ArrayList<>();
            List<Entry> speed_entries = new ArrayList<>();

            JSONArray json = new JSONArray(recordData.getDrive_json());
            for(int i=0;i<json.length();i++) {
                int fef = json.getJSONObject(i).getInt("fuel_efi");
                if(fef == 0)
                    idle++;
                else if(fef < 10)
                    bottom++;
                else if(fef < 14)
                    mid++;
                else
                    top++;

                speed_entries.add(new Entry(i, json.getJSONObject(i).getInt("speed")));
            }

            entries.add(new PieEntry((idle/json.length())*100, "공회전"));
            entries.add(new PieEntry((bottom/json.length())*100, "비경제운전"));
            entries.add(new PieEntry((mid/json.length())*100, "보통운전"));
            entries.add(new PieEntry((top/json.length())*100, "경제운전"));

            PieDataSet pieDataSet = new PieDataSet(entries, "주행그래프");
            PieData pieData = new PieData(pieDataSet);

            int color_arr[] = { Color.BLACK, Color.RED, Color.YELLOW, Color.GREEN };
            pieDataSet.setColors(color_arr, 60); // 속성색깔

            pieData.setValueFormatter(new PercentFormatter());
            chart_drive.setData(pieData);
            chart_drive.animateY(2000);


            LineDataSet lineDataSet = new LineDataSet(speed_entries, "속도");
            LineData lineData = new LineData(lineDataSet);
            lineDataSet.setDrawCircles(false);
            lineDataSet.setDrawFilled(true);

            chart_speed.getXAxis().setValueFormatter(new IAxisValueFormatter() {

                private SimpleDateFormat mFormat = new SimpleDateFormat("HH:mm:ss");
                @Override
                public String getFormattedValue(float value, AxisBase axis) {

                    long millis = TimeUnit.SECONDS.toMillis((long) value - 32400);
                    return mFormat.format(new Date(millis));
                }
            });


            chart_speed.setData(lineData);


        } catch (JSONException e) {
            e.printStackTrace();
        }


    }


    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        // Add a marker in Sydney and move the camera


        polylineOptions = new PolylineOptions();

        try {
            JSONArray json = new JSONArray(recordData.getPosition_json());
            for(int i=0;i<json.length();i++) {
                polylineOptions.add(new LatLng(json.getJSONObject(i).getDouble("lat"),json.getJSONObject(i).getDouble("lon")));
            }
            polylineOptions.color(Color.RED);
            mMap.addMarker(new MarkerOptions().position(new LatLng(json.getJSONObject(0).getDouble("lat"),json.getJSONObject(0).getDouble("lon"))).title("Start!"));
            mMap.addMarker(new MarkerOptions().position(new LatLng(json.getJSONObject(json.length()-1).getDouble("lat"),json.getJSONObject(json.length()-1).getDouble("lon"))).title("End!"));
            mMap.moveCamera(CameraUpdateFactory.newLatLng(new LatLng(json.getJSONObject(json.length()-1).getDouble("lat"),json.getJSONObject(json.length()-1).getDouble("lon"))));

        } catch (JSONException e) {
            e.printStackTrace();
        }

        mMap.animateCamera(CameraUpdateFactory.zoomTo(11));
        mMap.addPolyline(polylineOptions);
    }


}
