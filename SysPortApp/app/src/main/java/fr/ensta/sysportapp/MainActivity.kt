package fr.ensta.sysportapp

//import android.app.Activity
import androidx.appcompat.app.AppCompatActivity
import android.content.Intent
import android.content.pm.ActivityInfo
import android.os.Bundle
import android.preference.PreferenceManager
import android.view.View
import android.view.WindowManager
import net.majorkernelpanic.streaming.SessionBuilder
import net.majorkernelpanic.streaming.gl.SurfaceView
import net.majorkernelpanic.streaming.rtsp.RtspServer
import net.majorkernelpanic.streaming.video.VideoQuality


/**
 * A straightforward example of how to use the RTSP server included in libstreaming.
 */
class MainActivity : AppCompatActivity() {
    private var mSurfaceView: SurfaceView? = null

    /** Default quality of video streams.  */
    var videoQuality = VideoQuality(320, 240, 10, 128000)


    companion object {
        private const val TAG = "MainActivity"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        setContentView(R.layout.activity_main)
        requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        mSurfaceView = findViewById<View>(R.id.surface) as SurfaceView

        // Sets the port of the RTSP server to 1234
        val editor = PreferenceManager.getDefaultSharedPreferences(this).edit()
        editor.putString(RtspServer.KEY_PORT, 1234.toString())
        editor.commit()

        // Configures the SessionBuilder
        SessionBuilder.getInstance()
                .setSurfaceView(mSurfaceView)
                .setPreviewOrientation(90)
                .setContext(applicationContext)
                .setVideoQuality(videoQuality)
                .setAudioEncoder(SessionBuilder.AUDIO_NONE).videoEncoder = SessionBuilder.VIDEO_H264

        // Starts the RTSP server
        startService(Intent(this, RtspServer::class.java))
    }

    public override fun onDestroy() {
        super.onDestroy()
        stopService(Intent(this, RtspServer::class.java))
    }


}


/*import android.app.AlertDialog
import android.content.pm.ActivityInfo
import android.os.Bundle
import android.util.Log
import android.view.SurfaceHolder
import android.view.View
import android.view.View.OnClickListener
import android.view.WindowManager
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.karumi.dexter.Dexter
import com.karumi.dexter.PermissionToken
import com.karumi.dexter.listener.PermissionDeniedResponse
import com.karumi.dexter.listener.PermissionGrantedResponse
import com.karumi.dexter.listener.PermissionRequest
import com.karumi.dexter.listener.single.PermissionListener
import net.majorkernelpanic.streaming.Session
import net.majorkernelpanic.streaming.SessionBuilder
import net.majorkernelpanic.streaming.audio.AudioQuality
import net.majorkernelpanic.streaming.gl.SurfaceView
import net.majorkernelpanic.streaming.video.VideoQuality*/





/*/**
 * A straightforward example of how to stream AMR and H.263 to some public IP using libstreaming.
 * Note that this example may not be using the latest version of libstreaming !
 */*/
/*class MainActivity : AppCompatActivity(), OnClickListener, Session.Callback, SurfaceHolder.Callback {
    private var mButton1: Button? = null
    private var mButton2: Button? = null
    private var mSurfaceView: SurfaceView? = null
    private var mEditText: EditText? = null
    private var mSession: Session? = null

    companion object {
        private const val TAG = "MainActivity"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        //Request permission
        Dexter.withContext(this)
            .withPermission(android.Manifest.permission.CAMERA)
            .withListener(object : PermissionListener {
                override fun onPermissionGranted(response: PermissionGrantedResponse?) {

                }

                override fun onPermissionRationaleShouldBeShown(
                        permission: PermissionRequest?,
                        token: PermissionToken?
                ) {

                }

                override fun onPermissionDenied(response: PermissionDeniedResponse?) {
                    Toast.makeText(this@MainActivity, "You must grant permission", Toast.LENGTH_LONG).show()
                }

            }).check()

        requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        mButton1 = findViewById<View>(R.id.button1) as Button
        mButton2 = findViewById<View>(R.id.button2) as Button
        mSurfaceView = findViewById<View>(R.id.surface) as SurfaceView
        mEditText = findViewById<View>(R.id.editText1) as EditText

        mSession = SessionBuilder.getInstance()
            .setCallback(this)
            .setSurfaceView(mSurfaceView)
            .setPreviewOrientation(90)
            .setContext(applicationContext)
            .setAudioEncoder(SessionBuilder.AUDIO_NONE)
            .setAudioQuality(AudioQuality(16000, 32000))
            .setVideoEncoder(SessionBuilder.VIDEO_H264)
            .setVideoQuality(VideoQuality(320, 240, 20, 500000))
            .build()

        mButton1!!.setOnClickListener(this)
        mButton2!!.setOnClickListener(this)

        mSurfaceView!!.holder.addCallback(this)
    }

    public override fun onResume() {
        super.onResume()
        if (mSession!!.isStreaming) {
            mButton1!!.setText(R.string.stop)
        } else {
            mButton1!!.setText(R.string.start)
        }
    }

    public override fun onDestroy() {
        super.onDestroy()
        mSession!!.release()
    }

    override fun onClick(v: View) {
        if (v.id == R.id.button1) {
            // Starts/stops streaming
            mSession!!.destination = mEditText!!.text.toString()
            if (!mSession!!.isStreaming) {
                mSession!!.configure()
            } else {
                mSession!!.stop()
            }
            mButton1!!.isEnabled = false
        } else {
            // Switch between the two cameras
            mSession!!.switchCamera()
        }
    }

    override fun onBitrateUpdate(bitrate: Long) {
        Log.d(TAG, "Bitrate: $bitrate")
    }

    override fun onSessionError(message: Int, streamType: Int, e: Exception) {
        mButton1!!.isEnabled = true
        if (e != null) {
            logError(e.message)
        }
    }

    override fun onPreviewStarted() {
        Log.d(TAG, "Preview started.")
    }

    override fun onSessionConfigured() {
        Log.d(TAG, "Preview configured.")
        // Once the stream is configured, you can get a SDP formated session description
        // that you can send to the receiver of the stream.
        // For example, to receive the stream in VLC, store the session description in a .sdp file
        // and open it with VLC while streaming.
        Log.d(TAG, mSession!!.sessionDescription)
        mSession!!.start()
    }

    override fun onSessionStarted() {
        Log.d(TAG, "Session started.")
        mButton1!!.isEnabled = true
        mButton1!!.setText(R.string.stop)
    }

    override fun onSessionStopped() {
        Log.d(TAG, "Session stopped.")
        mButton1!!.isEnabled = true
        mButton1!!.setText(R.string.start)
    }

    /** Displays a popup to report the eror to the user  */
    private fun logError(msg: String?) {
        val error = msg ?: "Error unknown"
        val builder = AlertDialog.Builder(this@MainActivity)
        builder.setMessage(error).setPositiveButton(
                "OK"
        ) { dialog, id -> }
        val dialog = builder.create()
        dialog.show()
    }

    override fun surfaceChanged(
            holder: SurfaceHolder, format: Int, width: Int,
            height: Int
    ) {
    }

    override fun surfaceCreated(holder: SurfaceHolder) {
        mSession!!.startPreview()
    }

    override fun surfaceDestroyed(holder: SurfaceHolder) {
        mSession!!.stop()
    }


}*/
