package com.example.kpu.googlelogintest.utills;

import android.app.Activity;
import android.util.Log;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;

/**
 * Created by CSHYEON on 2017-05-20.
 */

public class DBRequester {

    private static class DBRequestThread extends Thread {

        public final int MAX_WAITING_TIME = 3000;

        private String _id;
        private String _host;
        private Activity _activity;
        private DBRequester.Listener _listener;
        private JSONObject _streamPost;
        private Object[] _params;

        public DBRequestThread(Activity activity, String host, String id, DBRequester.Listener listener, JSONObject streamPost, Object... params) {

            this._host = host;
            this._id = id;
            this._listener = listener;
            this._activity = activity;
            this._streamPost = streamPost;
            this._params = params;
        }

        private void post(String response, Listener listener) {

            // 1. Try parse to JSONObject
            try {

                if (listener != null)
                    listener.onResponse(this._id, new JSONObject(response), this._params);

                return;
            } catch (JSONException e) {


            } catch (Exception e) {

                if(listener != null)
                    listener.onError(this._id, response, this._params);

                return;
            }



            // 2. Try parse to JSONArray
            try {

                if(listener != null)
                    listener.onResponse(this._id, new JSONArray(response), this._params);

                return;

            } catch (Exception e) {

                if(listener != null)
                    listener.onError(this._id, response, this._params);
            }
        }

        @Override
        public void run() {

            try {
                URL url = new URL(this._host);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();

                if (conn == null)
                    throw new Exception();

                conn.setConnectTimeout(MAX_WAITING_TIME);
                conn.setUseCaches(false);
                if(_streamPost != null) {

                    conn.setRequestMethod("POST");
                    conn.setRequestProperty("Content-Type", "application/json; charset=utf-8");
                    conn.setRequestProperty("Accept", "application/json; charset=utf-8");
                    conn.setDoOutput(true);
                    conn.setDoInput(true);

                    OutputStream os = conn.getOutputStream();
                    os.write(this._streamPost.toString().getBytes("UTF-8"));
                    os.flush();
                }

                if (conn.getResponseCode() != HttpURLConnection.HTTP_OK)
                    throw new Exception();

                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                final StringBuilder builder = new StringBuilder();
                while (true) {

                    String line = reader.readLine();
                    if (line == null)
                        break;

                    builder.append(line);
                }
                reader.close();
                conn.disconnect();

                this._activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {

                        post(builder.toString(), _listener);
                    }
                });

            } catch (Exception e) {
                Log.e("ParkChan", e.getMessage());
                /*Toast.makeText(_activity, e.getMessage(), Toast.LENGTH_SHORT).show();*/

            }
        }
    }

    public interface Listener {

        void onResponse(String id, JSONObject json, Object... params);

        void onResponse(String id, JSONArray json, Object... params);

        void onError(String id, String message, Object... params);
    }

    public static class Builder {

        private StringBuilder _host;
        private Activity _activity;
        private JSONObject _streamPost;
        private DBRequester.Listener _listener;
        private ArrayList<Object> _params = new ArrayList<>();

        public Builder(Activity activity, String host) {

            this._activity = activity;
            this._host = new StringBuilder(host);
        }

        public Builder(Activity activity, String host, DBRequester.Listener listener) {

            this(activity, host);
            this.setListener(listener);
        }

        public Builder attach(String value) {

            this._host.append("/" + value);
            return this;
        }

        public Builder attach(int value) {

            return this.attach(Integer.toString(value));
        }

        public Builder setListener(DBRequester.Listener listener) {

            this._listener = listener;
            return this;
        }

        public Builder addParam(Object obj) {

            this._params.add(obj);
            return this;
        }

        public Builder streamPost(JSONObject stream) {

            this._streamPost = stream;
            return this;
        }

        public void request(String id) {

            DBRequestThread thread = new DBRequestThread(this._activity, this._host.toString(), id, this._listener, this._streamPost, this._params.toArray());
            thread.start();
        }
    }

    private Listener _listener;
    private Activity _activity;

    public DBRequester(Activity activity, Listener listener) {

        this._listener = listener;
        this._activity = activity;
    }

    public void request(final String id, final String host, JSONObject streamPost, Object... params) {

        try {
            new DBRequestThread(this._activity, host, id, this._listener, streamPost, params).start();
        } catch (Exception e) {


        }
    }
}