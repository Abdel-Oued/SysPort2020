package fr.ensta.sysportapp

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.databinding.DataBindingUtil
import androidx.navigation.findNavController
import androidx.navigation.ui.NavigationUI
import fr.ensta.sysportapp.databinding.ActivityMain3Binding
import net.majorkernelpanic.streaming.rtsp.RtspServer

class MainActivity : AppCompatActivity() {

    /**
     * Our MainActivity is only responsible for setting the content view that contains the
     * Navigation Host.
     */
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        //setContentView(R.layout.activity_main)
        val binding = DataBindingUtil.setContentView<ActivityMain3Binding>(this, R.layout.activity_main3)
        val navController = this.findNavController(R.id.nav_host_fragment)
        NavigationUI.setupActionBarWithNavController(this, navController)
        //BaseURL.baseURL = "http://192.168.0.24:8080/"
    }

    override fun onSupportNavigateUp(): Boolean {
        val navController = this.findNavController(R.id.nav_host_fragment)
        return navController.navigateUp()
    }

    public override fun onDestroy() {
        super.onDestroy()
        stopService(Intent(this, RtspServer::class.java))
    }
}
