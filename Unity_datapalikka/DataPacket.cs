using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[Serializable]
public class DataPacket
{
    public string deviceID;
    public string time;
    public string map; // This data isn't used anywhere, a placeholder template
    public int points; // This data isn't used anywhere, a placeholder template
    public int maxStreak; // This data isn't used anywhere, a placeholder template
    public List<float> time_data;
    public List<Vector3> spatial_data;
    public List<Vector3> acceleration_data;
    public List<Vector3> velocity_data;

    public string ToJSON(){
        string json = JsonUtility.ToJson(this);
        return json;
    }

}
