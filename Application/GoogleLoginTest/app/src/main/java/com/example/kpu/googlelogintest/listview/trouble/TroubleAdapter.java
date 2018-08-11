package com.example.kpu.googlelogintest.listview.trouble;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.kpu.googlelogintest.R;

import java.util.ArrayList;

public class TroubleAdapter extends BaseAdapter{
    private ArrayList<TroubleData> listCustom = new ArrayList<>();
    @Override
    public int getCount() {
        return listCustom.size();
    }

    @Override
    public Object getItem(int position) {
        return listCustom.get(position);
    }

    @Override
    public long getItemId(int position) {
        return 0;
    }

    public void addItem(TroubleData dto) {
        listCustom.add(dto);
    }

    public void clearItem()
    {
        listCustom.clear();
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        CustomViewHolder holder;
        if (convertView == null) {
            convertView = LayoutInflater.from(parent.getContext()).inflate(R.layout.list_custom, null, false);

            holder = new CustomViewHolder();
            holder.imageView = convertView.findViewById(R.id.imageView);
            holder.textTitle = convertView.findViewById(R.id.text_title);
            holder.textContent = convertView.findViewById(R.id.text_content);

            convertView.setTag(holder);
        } else {
            holder = (CustomViewHolder) convertView.getTag();
        }
        TroubleData dto = listCustom.get(position);

        holder.textTitle.setText("날짜 : "+dto.getTroubleTime());
        holder.textTitle.setTextColor(Color.rgb(217,67,116));
        holder.textContent.setText("코드 : " + dto.getTroubleCode());
        holder.textContent.setTextColor(Color.rgb(67,116,217));
        holder.imageView.setImageResource(R.drawable.car_scan);

        return convertView;
    }


    class CustomViewHolder{
        ImageView imageView;
        TextView textTitle;
        TextView textContent;
    }
}
