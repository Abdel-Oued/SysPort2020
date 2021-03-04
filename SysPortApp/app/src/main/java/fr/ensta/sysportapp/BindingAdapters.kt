package fr.ensta.sysportapp

import android.annotation.SuppressLint
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import androidx.databinding.BindingAdapter
import androidx.recyclerview.widget.RecyclerView
import fr.ensta.sysportapp.network.PersonInformation
import fr.ensta.sysportapp.overview.InformationGridAdapter
import fr.ensta.sysportapp.overview.SysportApiStatus

/**
 * When there is no Person information data (data is null), hide the [RecyclerView], otherwise show it.
 */
@BindingAdapter("listData")
fun bindRecyclerView(recyclerView: RecyclerView, data: List<PersonInformation>?) {
    val adapter = recyclerView.adapter as InformationGridAdapter
    adapter.submitList(data)
}

///**
// * Uses the Glide library to load an image by URL into an [ImageView]
// */
//@BindingAdapter("imageUrl")
//fun bindImage(imgView: ImageView, imgUrl: String?) {
//    imgUrl?.let {
//        val imgUri = imgUrl.toUri().buildUpon().scheme("https").build()
//        Glide.with(imgView.context)
//            .load(imgUri)
//            .apply(RequestOptions()
//                .placeholder(R.drawable.loading_animation)
//                .error(R.drawable.ic_broken_image))
//            .into(imgView)
//    }
//}

@SuppressLint("SetTextI18n")
@BindingAdapter("information")
fun bindInformation(informationTextView: TextView, information: PersonInformation?) {
    information?.let { informationTextView.text = """
     ${information.nom}
     ${information.prenom}
     ${information.tauxAlcool}
     ${information.dette}
     
     """.trimIndent()
    }
}


/**
 * This binding adapter displays the [SysportApiStatus] of the network request in an image view.  When
 * the request is loading, it displays a loading_animation.  If the request has an error, it
 * displays a broken image to reflect the connection error.  When the request is finished, it
 * hides the image view.
 */
@BindingAdapter("sysportApiStatus")
fun bindStatus(statusImageView: ImageView, status: SysportApiStatus?) {
    when (status) {
        SysportApiStatus.LOADING -> {
            statusImageView.visibility = View.VISIBLE
            statusImageView.setImageResource(R.drawable.loading_animation)
        }
        SysportApiStatus.ERROR -> {
            statusImageView.visibility = View.VISIBLE
            statusImageView.setImageResource(R.drawable.ic_connection_error)
        }
        SysportApiStatus.DONE -> {
            statusImageView.visibility = View.GONE
        }
    }
}
