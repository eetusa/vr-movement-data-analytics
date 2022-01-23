using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class trackControllerData : MonoBehaviour
{
    
    List<UnityEngine.XR.InputDevice> leftHandedControllers = new List<UnityEngine.XR.InputDevice>();
    List<Vector3> accelerationArray = new List<Vector3>();
    List<Vector3> velocityArray = new List<Vector3>();
    List<Vector3> positionArray = new List<Vector3>();
    List<float> timeArray = new List<float>();
    float captureStartTime = 0f;
    bool dataCaptureOn = false; // Data capture off by default
    string server = "http://127.0.0.1:3210/";   // Hard-coded server IP
    


    void Start()
    {
        // Get left-hand controller(s)
        var desiredCharacteristics = UnityEngine.XR.InputDeviceCharacteristics.HeldInHand | UnityEngine.XR.InputDeviceCharacteristics.Left | UnityEngine.XR.InputDeviceCharacteristics.Controller;
        UnityEngine.XR.InputDevices.GetDevicesWithCharacteristics(desiredCharacteristics, leftHandedControllers);
        
        foreach (var device in leftHandedControllers)
        {
            Debug.Log(string.Format("Device name '{0}' has characteristics '{1}'", device.name, device.characteristics.ToString()));
        }
        
    }

    
    void Update()
    {
        
        if (leftHandedControllers.Count > 0){
            leftHandedControllers[0].TryGetFeatureValue(UnityEngine.XR.CommonUsages.triggerButton, out bool trigger_down);
            if (trigger_down){
                if (!dataCaptureOn)
                    turnDataCaptureOn(true);
            } else {

                // If trigger isn't down but data is still being captured
                // end data capture and send the saved data to server
                if (dataCaptureOn){
                    turnDataCaptureOn(false);
                    string data = getJSONifiedData();
                    sendMessage(data);
                }
            }

            if (dataCaptureOn){
                recordData();
            }

        }

    }

    // recordData()
    // Save position, acceleration, velocity and the time from beginning of recording to arrays.
    void recordData(){
        Vector3 position = new Vector3();
        Vector3 acceleration = new Vector3();
        Vector3 velocity = new Vector3();

        leftHandedControllers[0].TryGetFeatureValue(UnityEngine.XR.CommonUsages.devicePosition, out position);
        leftHandedControllers[0].TryGetFeatureValue(UnityEngine.XR.CommonUsages.deviceAcceleration, out acceleration);
        leftHandedControllers[0].TryGetFeatureValue(UnityEngine.XR.CommonUsages.deviceVelocity, out velocity);

        accelerationArray.Add(acceleration);
        velocityArray.Add(velocity);
        positionArray.Add(position);
        timeArray.Add(Time.timeSinceLevelLoad - captureStartTime);
    }

    void turnDataCaptureOn(bool value){
        dataCaptureOn = value;
        if (value){
            captureStartTime = Time.timeSinceLevelLoad;
            Debug.Log("Data capture started");
            accelerationArray.Clear();
            velocityArray.Clear();
            positionArray.Clear();
            timeArray.Clear();
            
        } else {
            Debug.Log("Data capture stopped.");
            Debug.Log("Data collected: " +positionArray.Count);
        }
    }

    string getJSONifiedData(){
        string devID = UnityEngine.SystemInfo.deviceUniqueIdentifier;   // Unique device id
        DateTime baseDate = new DateTime(1970, 1, 1);
        TimeSpan diff = DateTime.Now - baseDate;
        string difms = diff.TotalMilliseconds.ToString();
        difms = difms.Split(',')[0];    // Current time in milliseconds since 1.1.1970
        
        // Using DataPacket class to contain the data and resolve the object to JSON
        DataPacket packet = new DataPacket();

        packet.acceleration_data = accelerationArray;
        packet.velocity_data = velocityArray;
        packet.spatial_data = positionArray;
        packet.time_data = timeArray;
        packet.deviceID = devID;
        packet.time = difms;
        
        return packet.ToJSON();
    }

    
    public void sendMessage(string message){
        StartCoroutine(Upload(message));
    }

    public IEnumerator Upload(string message) {
        Debug.Log("Uploading..");
        Debug.Log(message);
        byte[] barr = System.Text.Encoding.UTF8.GetBytes(message);
        using (UnityWebRequest www = UnityWebRequest.Put(server, barr))
            {
                yield return www.SendWebRequest();
        
                if (www.result != UnityWebRequest.Result.Success) {
                    Debug.Log(www.error);
                }
                else {
                    Debug.Log("Upload complete!");
                }
            }
    }


}
