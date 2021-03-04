package fr.ensta.sysportapp.detail

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import fr.ensta.sysportapp.network.PersonInformation

/**
 * The [ViewModel] that is associated with the [DetailFragment].
 */
class DetailViewModel(personInformation: PersonInformation, app: Application) : AndroidViewModel(app) {
    private val _selectedPerson = MutableLiveData<PersonInformation>()

    val selectedPerson: LiveData<PersonInformation>
        get() = _selectedPerson

    init {
        _selectedPerson.value = personInformation
    }
}
