package fr.ensta.sysportapp.overview

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.databinding.DataBindingUtil
import androidx.navigation.Navigation
import androidx.navigation.findNavController
import fr.ensta.sysportapp.R
import fr.ensta.sysportapp.databinding.FragmentConnectionBinding
import fr.ensta.sysportapp.network.BaseURL

/**
 * A simple [Fragment] subclass.
 * Use the [ConnectionFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class ConnectionFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
//        val binding: FragmentConnectionBinding = DataBindingUtil.inflate(
//            inflater, R.layout.fragment_connection, container, false)
        val binding: FragmentConnectionBinding = FragmentConnectionBinding.inflate(inflater)

//        binding.btnAddress.setOnClickListener (
//            Navigation.createNavigateOnClickListener(R.id.action_connectionFragment_to_overviewFragment))
                binding.btnAddress.setOnClickListener {
                    BaseURL.baseURL = "http://"+binding.editAdress.text.toString()+":8080/"
                    view?.findNavController()?.navigate(R.id.action_connectionFragment_to_overviewFragment)
        }
        return binding.root
    }

//    companion object {
//        /**
//         * Use this factory method to create a new instance of
//         * this fragment using the provided parameters.
//         *
//         * @param param1 Parameter 1.
//         * @param param2 Parameter 2.
//         * @return A new instance of fragment ConnectionFragment.
//         */
//        // TODO: Rename and change types and number of parameters
//        @JvmStatic
//        fun newInstance(param1: String, param2: String) =
//            ConnectionFragment().apply {
//                arguments = Bundle().apply {
//                    putString(ARG_PARAM1, param1)
//                    putString(ARG_PARAM2, param2)
//                }
//            }
//    }
}