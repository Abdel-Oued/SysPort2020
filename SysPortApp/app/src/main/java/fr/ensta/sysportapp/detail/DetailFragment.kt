package fr.ensta.sysportapp.detail

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import fr.ensta.sysportapp.databinding.FragmentDetailBinding

/**
 * This [Fragment] will show the detailed information about a selected person.
 */
class DetailFragment : Fragment() {
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?,
                              savedInstanceState: Bundle?): View? {

        val application = requireNotNull(activity).application
        val binding = FragmentDetailBinding.inflate(inflater)
        binding.lifecycleOwner = this

        val personInformation = DetailFragmentArgs.fromBundle(arguments!!).selectedPerson

        val viewModelFactory = DetailViewModelFactory(personInformation, application)
        binding.viewModel = ViewModelProvider(
            this, viewModelFactory).get(DetailViewModel::class.java)

        return binding.root
    }
}
