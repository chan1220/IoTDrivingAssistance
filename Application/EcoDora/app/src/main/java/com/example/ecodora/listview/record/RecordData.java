package com.example.ecodora.listview.record;

import java.io.Serializable;

/**
 * Created by KPU on 2018-03-15.
 */

public class RecordData implements Serializable {
    private String car_id;
    private String start_time;
    private String end_time;
    private String fuel_eft;
    private String speed;
    private String rpm;
    private String break_num;
    private String accel_num;
    private String score;
    private String distance;
    private String position_json;
    private String drive_json;
    public String getCar_id() {
        return car_id;
    }

    public void setCar_id(String car_id) {
        this.car_id = car_id;
    }

    public String getStart_time() {
        return start_time;
    }

    public void setStart_time(String start_time) {
        this.start_time = start_time;
    }

    public String getEnd_time() {
        return end_time;
    }

    public void setEnd_time(String end_time) {
        this.end_time = end_time;
    }

    public String getSpeed() {
        return speed;
    }

    public void setSpeed(String speed) {
        this.speed = speed;
    }

    public String getRpm() {
        return rpm;
    }

    public void setRpm(String rpm) {
        this.rpm = rpm;
    }

    public String getBreak_num() {
        return break_num;
    }

    public void setBreak_num(String break_num) {
        this.break_num = break_num;
    }

    public String getAccel_num() {
        return accel_num;
    }

    public void setAccel_num(String accel_num) {
        this.accel_num = accel_num;
    }

    public String getScore() {
        return score;
    }

    public void setScore(String score) {
        this.score = score;
    }

    public String getDistance() {
        return distance;
    }

    public void setDistance(String distance) {
        this.distance = distance;
    }

    public String getFuel_eft() {
        return fuel_eft;
    }

    public void setFuel_eft(String fuel_eft) {
        this.fuel_eft = fuel_eft;
    }

    public String getPosition_json() {
        return position_json;
    }

    public void setPosition_json(String position_json) {
        this.position_json = position_json;
    }

    public String getDrive_json() {
        return drive_json;
    }

    public void setDrive_json(String drive_json) {
        this.drive_json = drive_json;
    }
}
