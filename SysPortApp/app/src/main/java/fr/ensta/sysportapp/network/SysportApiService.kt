package fr.ensta.sysportapp.network

//import com.jakewharton.retrofit2.adapter.kotlin.coroutines.CoroutineCallAdapterFactory
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import retrofit2.http.*
import fr.ensta.sysportapp.Parameters
//import retrofit2.converter.scalars.ScalarsConverterFactory

// import kotlinx.coroutines.Deferred


/**
 * Build the Moshi object that network will be using, making sure to add the Kotlin adapter for
 * full Kotlin compatibility.
 */
private val moshi = Moshi.Builder()
    .add(KotlinJsonAdapterFactory())
    .build()

/**
 * Use the network builder to build a retrofit object using a Moshi converter with our Moshi
 * object.
 */
private val retrofit by lazy { Retrofit.Builder()
    .addConverterFactory(MoshiConverterFactory.create(moshi)) //ScalarsConverterFactory.create()  //MoshiConverterFactory.create(moshi)
    .baseUrl(Parameters.baseURL)
    .build() }

/**
 * A public interface that exposes the [getInformation] and [startCamera] methods
 */
interface SysportApiService {
    /**
     * The @GET annotation indicates that the "information" endpoint will be requested with the GET
     * HTTP method
     */
    @GET("information/")
    suspend fun getInformation(): List<PersonInformation>

    /**
     * The @POST annotation indicates that the "information" endpoint will be requested with the POST
     * HTTP method
     */
    @FormUrlEncoded
    @POST("startcamera/")
    fun startCamera(@Field("ip_adress") ip_adress:String): Call<String>
}

/**
 * A public Api object that exposes the lazy-initialized network service
 */
object SysportApi {
    val retrofitService : SysportApiService by lazy { retrofit.create(SysportApiService::class.java) }
}