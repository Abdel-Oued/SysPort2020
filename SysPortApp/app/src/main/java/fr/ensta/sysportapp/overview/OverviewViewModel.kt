package fr.ensta.sysportapp.overview

//import kotlinx.coroutines.CoroutineScope
//import kotlinx.coroutines.Dispatchers
import android.util.Log
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import fr.ensta.sysportapp.network.PersonInformation
import fr.ensta.sysportapp.network.SysportApi
import kotlinx.coroutines.launch
import net.majorkernelpanic.streaming.rtsp.RtspServer
import retrofit2.HttpException
import java.io.IOException
import java.util.concurrent.TimeoutException


enum class SysportApiStatus { LOADING, ERROR, DONE }
/**
 * The [ViewModel] that is attached to the [OverviewFragment].
 */
class OverviewViewModel : ViewModel() {

    // The internal MutableLiveData String that stores the most recent response status
    private val _status = MutableLiveData<SysportApiStatus>()

    // The external immutable LiveData for the status String
    val status: LiveData<SysportApiStatus>
        get() = _status

    // Internally, we use a MutableLiveData, because we will be updating the List of PersonInformation
    // with new values
    private val _persons = MutableLiveData<List<PersonInformation>>()

    // The external LiveData interface to the information is immutable, so only this class can modify
    val persons: LiveData<List<PersonInformation>>
        get() = _persons

    private val _navigateToSelectedPerson = MutableLiveData<PersonInformation>()

    val navigateToSelectedPerson: LiveData<PersonInformation>
        get() = _navigateToSelectedPerson

    /**
     * Call getPersonActualInformation() on init so we can display status immediately.
     */
    init {
        getPersonActualInformation()
    }

    /**
     * Gets Mars real estate property information from the Sysport API network service and updates the
     * [PersonInformation] [List] [LiveData]. The network service returns a coroutine Deferred, which we
     * await to get the result of the transaction.
     */
    private fun getPersonActualInformation() {
        viewModelScope.launch {
            _status.value = SysportApiStatus.LOADING
            while (true) {
                try {
                    _persons.value = SysportApi.retrofitService.getInformation()
                    _status.value = SysportApiStatus.DONE
                    Log.i("SysportApi", "Connection enabled !")
                    Thread.sleep(3000);
                } catch (e: HttpException) {
                    _status.value = SysportApiStatus.ERROR
                    _persons.value = ArrayList()
                    Log.i("SysportApi", "Connection error ! : HttpException " + e.message)
                } catch (e: TimeoutException) {
                    _status.value = SysportApiStatus.ERROR
                    _persons.value = ArrayList()
                    Log.i("SysportApi", "Connection error ! : TimeoutException " + e.message)
                }catch (e: IOException) {
                    _status.value = SysportApiStatus.ERROR
                    _persons.value = ArrayList()
                    e.message
                    Log.i("SysportApi", "Connection error ! : IOException " + e.message)
                } catch (e: Exception) {
                    _status.value = SysportApiStatus.ERROR
                    _persons.value = ArrayList()
                    Log.i("SysportApi", "Connection error ! : Indetermined exception " + e.message)
                }
            }

//            try {
//                _persons.value = SysportApi.retrofitService.getInformation()
//                _status.value = SysportApiStatus.DONE
//                Log.i("SysportApi", "Connection enabled !")
//                getPersonActualInformation()
//            } catch (e: HttpException) {
//                _status.value = SysportApiStatus.ERROR
//                _persons.value = ArrayList()
//                Log.i("SysportApi", "Connection error ! : HttpException " + e.message)
//                getPersonActualInformation()
//            } catch (e: TimeoutException) {
//                _status.value = SysportApiStatus.ERROR
//                _persons.value = ArrayList()
//                Log.i("SysportApi", "Connection error ! : TimeoutException " + e.message)
//                getPersonActualInformation()
//            }catch (e: IOException) {
//                _status.value = SysportApiStatus.ERROR
//                _persons.value = ArrayList()
//                e.message
//                Log.i("SysportApi", "Connection error ! : IOException " + e.message)
//                getPersonActualInformation()
//            } catch (e: Exception) {
//                _status.value = SysportApiStatus.ERROR
//                _persons.value = ArrayList()
//                Log.i("SysportApi", "Connection error ! : Indetermined exception " + e.message)
//                getPersonActualInformation()
//            }

        }
    }

    fun displayPersonDetails(personInformation: PersonInformation) {
        _navigateToSelectedPerson.value = personInformation
    }

    fun displayPersonDetailsComplete() {
        _navigateToSelectedPerson.value = null
    }

    /**
     */
}
