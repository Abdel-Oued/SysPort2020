package fr.ensta.sysportapp.overview

import android.content.Intent
import android.content.pm.ActivityInfo
import android.os.Bundle
import android.preference.PreferenceManager
import android.view.*
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import fr.ensta.sysportapp.databinding.FragmentOverviewBinding
import fr.ensta.sysportapp.network.Parameters
import net.majorkernelpanic.streaming.SessionBuilder
import net.majorkernelpanic.streaming.gl.SurfaceView
import net.majorkernelpanic.streaming.rtsp.RtspServer
import net.majorkernelpanic.streaming.video.VideoQuality

/**
 * This fragment shows the the status of the Mars real-estate web services transaction.
 */
class OverviewFragment : Fragment() {

    private var mSurfaceView: SurfaceView? = null

    /** Default quality of video streams.  */
    //var videoQuality = VideoQuality(320, 240, 3, 128000)
    var videoQuality = VideoQuality(320, 240, Parameters.framerate, Parameters.bitrate)


    /**
     * Lazily initialize our [OverviewViewModel].
     */
    private val viewModel: OverviewViewModel by lazy {
        ViewModelProvider(this).get(OverviewViewModel::class.java)
    }

    /**
     * Inflates the layout with Data Binding, sets its lifecycle owner to the OverviewFragment
     * to enable Data Binding to observe LiveData, and sets up the RecyclerView with an adapter.
     */
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?,
                              savedInstanceState: Bundle?): View? {
        val binding = FragmentOverviewBinding.inflate(inflater)

        // Allows Data Binding to Observe LiveData with the lifecycle of this Fragment
        binding.lifecycleOwner = this

        // Giving the binding access to the OverviewViewModel
        binding.viewModel = viewModel

        // Sets the adapter of the photosGrid RecyclerView with clickHandler lambda that
        // tells the viewModel when our property is clicked
        binding.informationGrid.adapter = InformationGridAdapter(InformationGridAdapter.OnClickListener {
            viewModel.displayPersonDetails(it)
        })

        /**
         * Setup the RTSP server
         */
        this.activity?.window?.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        //binding = DataBindingUtil.setContentView(this, R.layout.activity_main)
        this.activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        mSurfaceView = binding.surfaceVideo as SurfaceView


        // Sets the port of the RTSP server to 1234
        val editor = PreferenceManager.getDefaultSharedPreferences(this.context).edit()
        editor.putString(RtspServer.KEY_PORT, 1234.toString())
        editor.commit()

        // Configures the SessionBuilder
        SessionBuilder.getInstance()
            .setSurfaceView(mSurfaceView)
            .setPreviewOrientation(90)
            .setContext(this.context)
            .setVideoQuality(videoQuality)
            .setAudioEncoder(SessionBuilder.AUDIO_NONE).videoEncoder = SessionBuilder.VIDEO_H264

        // Starts the RTSP server
        this.context?.startService(Intent(this.context, RtspServer::class.java))
        //----------------------------------------------------------//

        return binding.root
    }

}
