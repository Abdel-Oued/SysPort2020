package com.example.kotlinfacedetectpython.Retrofit

import android.widget.EditText
import com.example.kotlinfacedetectpython.R
import retrofit2.Retrofit
import retrofit2.converter.scalars.ScalarsConverterFactory
//import androidx.appcompat.app.AppCompatActivity

object RetrofitClient {
    private var retrofitClient: Retrofit?=null
//    lateinit var ip_address: String
//    val addressText = AppCompatActivity.findViewById<EditText>(R.id.adress_edit)
//    ip_address = addressText.text.toString()

    val client:Retrofit
        get() {
            if(retrofitClient == null)
                retrofitClient = Retrofit.Builder()
                    .baseUrl("http://192.168.0.36:5000")
                    //.baseUrl("http://192.168.10.139:5000")
                    .addConverterFactory(ScalarsConverterFactory.create())
                    .build()
            return retrofitClient!!
        }
}