package com.example.kpu.googlelogintest.activitys;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
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
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.utills.PHPRequest;
import com.google.firebase.auth.FirebaseAuth;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.concurrent.ExecutionException;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {
    private EditText data1;
    private Button btn_send;
    private Intent intent;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "딱풀 건드리지마", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });

        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);






        data1 = findViewById(R.id.editText);
        btn_send = findViewById(R.id.btn_send);
        intent = new Intent(this.getIntent());

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);


        btn_send.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    String get_json_string = new BackgroundTask().execute(String.valueOf(data1.getText())).get();
                    JSONArray json = new JSONArray(get_json_string);
                    for(int i=0;i<json.length();i++) {
                        Toast.makeText(getApplicationContext(),json.getJSONObject(i).get("START_TIME").toString(),Toast.LENGTH_SHORT).show();
                        Toast.makeText(getApplicationContext(),json.getJSONObject(i).get("END_TIME").toString(),Toast.LENGTH_SHORT).show();
                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                    Toast.makeText(getApplicationContext(),"JSONException",Toast.LENGTH_SHORT).show();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (ExecutionException e) {
                    e.printStackTrace();
                }
            }
        });





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

        } else if (id == R.id.nav_score) {
            // 주행 점수
        } else if (id == R.id.nav_book) {
            // 차계부
        } else if (id == R.id.nav_info) {
            Intent intent_info=new Intent(MainActivity.this, InformationActivity.class);
            startActivity(intent_info);
            // 어플 정보
        }

        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }










    private class BackgroundTask extends AsyncTask<String,Void,String>
    {
        ProgressDialog progressDialog = new ProgressDialog(MainActivity.this);

        @Override
        protected void onPostExecute(String s) {
            super.onPostExecute(s);
            progressDialog.dismiss();
        }

        @Override // 여기에 할 작업
        protected String doInBackground(String... strings) {
            return PHPRequest.execute(getString(R.string.server_url)+"/qna.php", "Data1", strings[0]);


        }
        @Override
        protected void onPreExecute() {
            progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
            progressDialog.setMessage("Loading...");
            progressDialog.show();
            super.onPreExecute();
        }

    }





}