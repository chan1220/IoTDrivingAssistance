package com.example.kpu.googlelogintest.listview;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.kpu.googlelogintest.R;

import java.util.ArrayList;


public class RecordAdapter extends BaseAdapter {

    private ArrayList<RecordData> listCustom = new ArrayList<>();

    @Override
    public int getCount() {
        return listCustom.size();
    }

    // 하나의 Item(ImageView 1, TextView 2)
    @Override
    public Object getItem(int position) {
        return listCustom.get(position);
    }

    // Item의 id : Item을 구별하기 위한 것으로 position 사용
    @Override
    public long getItemId(int position) {
        return position;
    }

    // 실제로 Item이 보여지는 부분
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
        RecordData dto = listCustom.get(position);

        holder.textTitle.setText(dto.getStart_time());
        holder.textContent.setText(dto.getEnd_time());

        return convertView;
    }

    class CustomViewHolder {
        ImageView imageView;
        TextView textTitle;
        TextView textContent;
    }

    // MainActivity에서 Adapter에있는 ArrayList에 data를 추가시켜주는 함수
    public void addItem(RecordData dto) {
        listCustom.add(dto);
    }

    public void clearItem()
    {
        listCustom.clear();
    }
}
