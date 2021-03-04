package fr.ensta.sysportapp.network

import android.os.Parcel
import android.os.Parcelable
import com.squareup.moshi.Json
import kotlinx.android.parcel.Parcelize

/**
 * This data class defines a person information which includes a name, the image URL, the alcolism rate
 * and canServe boolean which is false if the alcolism rate is high.
 * The property names of this data class are used by Moshi to match the names of values in JSON.
 */
@Parcelize
data class PersonInformation(
        //@Json(name = "type")
    val nom: String?,
        //@Json(name = "img_src")
    val prenom: String?,
        //@Json(name = "price")
    val dette: Double,
        //@Json(name = "id")
    val tauxAlcool: Double) : Parcelable {}