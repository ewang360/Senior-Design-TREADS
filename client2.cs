using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Netcode.Transports.WebSocket;

public class client2 : MonoBehaviour
{

    private string url = "ws://192.168.0.24:5777/ws";

    private IWebSocketClient client;

    // Start is called before the first frame update
    void Start()
    {
        client = WebSocketClientFactory.Create(url);
        client.Connect();
    }

    // Update is called once per frame
    void Update()
    {
        //make websocket if its not made yet
        if (client == null)
        {
            client = WebSocketClientFactory.Create(url);
            client.Connect();
            Debug.Log("client is null");
            return;
        }
        else{
            WebSocketEvent wsEvent = client.Poll();
            client.EventQueue.Clear();
            Debug.Log("ws event " + wsEvent.Type);
            if (wsEvent.Type == WebSocketEvent.WebSocketEventType.Payload)
            {
                Texture2D tex = new Texture2D(2, 2);
                tex.LoadImage(wsEvent.Payload);
                GetComponent<Renderer>().material.mainTexture = tex;
                Resources.UnloadUnusedAssets();
            }
            if (wsEvent.Type == WebSocketEvent.WebSocketEventType.Error)
            {
                Debug.Log("error " + wsEvent.Error);
            }
            if (wsEvent.Type == WebSocketEvent.WebSocketEventType.Open)
            {
                Debug.Log("ws connected");
            }
        }
    }
}
