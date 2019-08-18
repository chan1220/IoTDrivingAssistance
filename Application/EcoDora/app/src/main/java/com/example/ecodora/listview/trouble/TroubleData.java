package com.example.ecodora.listview.trouble;
import java.io.Serializable;

public class TroubleData implements Serializable {
    public String troubleTime;
    public String troubleCode;
    public String troubleContent;

    public void setTroubleCode(String troubleCode) {
        this.troubleCode = troubleCode;
    }

    public String getTroubleCode() {
        return troubleCode;
    }

    public void setTroubleContent(String troubleContent) {
        this.troubleContent = troubleContent;
    }

    public String getTroubleContent() {
        return troubleContent;
    }

    public void setTroubleTime(String troubleTime) {
        this.troubleTime = troubleTime;
    }

    public String getTroubleTime() {
        return troubleTime;
    }
}
