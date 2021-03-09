package fr.ensta.sysportapp

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import fr.ensta.sysportapp.network.BaseURL
import net.majorkernelpanic.streaming.rtsp.RtspServer

class MainActivity : AppCompatActivity() {

    /**
     * Our MainActivity is only responsible for setting the content view that contains the
     * Navigation Host.
     */
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        BaseURL.baseURL = "http://192.168.10.97:8080/"
    }

    public override fun onDestroy() {
        super.onDestroy()
        stopService(Intent(this, RtspServer::class.java))
    }
}
