package fr.ensta.sysportapp.overview

import android.os.Bundle
import android.view.*
import androidx.fragment.app.Fragment
import androidx.navigation.findNavController
import fr.ensta.sysportapp.R
import fr.ensta.sysportapp.databinding.FragmentParametersBinding
import fr.ensta.sysportapp.Parameters

/**
 * A simple [Fragment] subclass.
 * Use the [ParametersFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class ParametersFragment : Fragment() {

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?,
                              savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val binding: FragmentParametersBinding = FragmentParametersBinding.inflate(inflater)

        binding.btnParameters.setOnClickListener {
            Parameters.framerate = binding.editFramerate.text.toString().toInt()
            Parameters.bitrate = binding.editBitrate.text.toString().toInt()
            Parameters.delay = binding.editDelay.text.toString().toInt()

        }

        return binding.root
    }

}