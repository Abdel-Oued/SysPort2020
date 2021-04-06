package fr.ensta.sysportapp.overview

import android.os.Bundle
import android.util.Log
import android.view.*
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.findNavController
import androidx.navigation.ui.NavigationUI
import fr.ensta.sysportapp.R
import fr.ensta.sysportapp.databinding.FragmentConnectionBinding
import fr.ensta.sysportapp.network.Parameters
import fr.ensta.sysportapp.network.SysportApi
import retrofit2.Call
import retrofit2.Response
import java.net.InetAddress
import java.net.NetworkInterface
import java.net.SocketException
import java.util.*

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
        // recuperer l'adress du telephone pour l'envoyer
        val ipAdress = getIpAddress()
        binding.btnAddress.setOnClickListener {
            Parameters.baseURL = "http://"+binding.editAdress.text.toString()+":8080/"
            // envoyer l'address ip du telephone
            sendAdress(ipAdress)
            view?.findNavController()?.navigate(R.id.action_connectionFragment_to_overviewFragment)
        }

        //to indicate this fragment has a menu
        setHasOptionsMenu(true)

        return binding.root
    }

    /**
     * Inflates the overflow menu that contains filtering options.
     */
    override fun onCreateOptionsMenu(menu: Menu, inflater: MenuInflater) {
        inflater.inflate(R.menu.overflow_menu, menu)
        super.onCreateOptionsMenu(menu, inflater)
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return NavigationUI.onNavDestinationSelected(
                item!!,
                view!!.findNavController()
        )
                || super.onOptionsItemSelected(item)
    }

    fun sendAdress(ipAdress: String) {
        Thread(Runnable {
            SysportApi.retrofitService.startCamera(ipAdress)
                    .enqueue(object : retrofit2.Callback<String> {
                        override fun onResponse(call: Call<String>, response: Response<String>) {
                            val statusCode = response.code()
                            Log.d("networkServiceModule", "response Code : $statusCode, IP adress: $ipAdress")
                            if (response.isSuccessful) {
                                //val resultCode: String = response.getResult_code().toString()
                                Toast.makeText(this@ConnectionFragment.context, "connected !", Toast.LENGTH_SHORT).show()
                            }

                        }

                        override fun onFailure(call: Call<String>, t: Throwable) {

                        }

                    })
        }).start()
    }

    private fun getIpAddress(): String {
        var ip = ""
        try {
            val enumNetworkInterfaces: Enumeration<NetworkInterface> = NetworkInterface
                .getNetworkInterfaces()
            while (enumNetworkInterfaces.hasMoreElements()) {
                val networkInterface: NetworkInterface = enumNetworkInterfaces
                    .nextElement()
                val enumInetAddress: Enumeration<InetAddress> = networkInterface
                    .getInetAddresses()
                while (enumInetAddress.hasMoreElements()) {
                    val inetAddress: InetAddress = enumInetAddress.nextElement()
                    if (inetAddress.isSiteLocalAddress()) {
                        ip += inetAddress.getHostAddress()
                    }
                }
            }
        } catch (e: SocketException) {
            // TODO Auto-generated catch block
            e.printStackTrace()
            ip += """
            Something Wrong! ${e.toString().toString()}
            
            """.trimIndent()
        }
        return ip
    }

}