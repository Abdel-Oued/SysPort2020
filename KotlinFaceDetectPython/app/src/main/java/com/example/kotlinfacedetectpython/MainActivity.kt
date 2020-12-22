package com.example.kotlinfacedetectpython

import android.app.Activity
import android.app.ProgressDialog
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.view.View
import android.view.inputmethod.InputMethodManager
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.FileProvider
import com.example.kotlinfacedetectpython.Retrofit.IUploadAPI
import com.example.kotlinfacedetectpython.Retrofit.RetrofitClient
import com.example.kotlinfacedetectpython.Utils.Common
import com.example.kotlinfacedetectpython.Utils.IUploadCallback
import com.example.kotlinfacedetectpython.Utils.ProgressRequestBody
import com.karumi.dexter.Dexter
import com.karumi.dexter.PermissionToken
import com.karumi.dexter.listener.PermissionDeniedResponse
import com.karumi.dexter.listener.PermissionGrantedResponse
import com.karumi.dexter.listener.PermissionRequest
import com.karumi.dexter.listener.single.PermissionListener
import com.squareup.picasso.Picasso
import okhttp3.MultipartBody
import java.io.File
import java.io.IOException
import java.net.URISyntaxException
import java.text.SimpleDateFormat
import java.util.*

class MainActivity : AppCompatActivity(), IUploadCallback {

    //properties
    lateinit var mService:IUploadAPI
    lateinit var dialog:ProgressDialog
    lateinit var image_view: ImageView
    lateinit var btn_upload: Button
    lateinit var ip_address: String
    lateinit var photoFile: File
    lateinit var photoPath: String
    lateinit var photoUri: Uri
    

    companion object{
        private val TAKE_PICTURE_REQUEST:Int = 2000
    }

    private val apiUpload:IUploadAPI
        get() = RetrofitClient.client.create(IUploadAPI::class.java)

    // Cette fonction se lance au lancement de l'app
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        //Request permission
        Dexter.withContext(this)
            .withPermission(android.Manifest.permission.READ_EXTERNAL_STORAGE)
            .withListener(object:PermissionListener{
                override fun onPermissionGranted(response: PermissionGrantedResponse?) {

                }

                override fun onPermissionRationaleShouldBeShown(
                    permission: PermissionRequest?,
                    token: PermissionToken?
                ) {

                }

                override fun onPermissionDenied(response: PermissionDeniedResponse?) {
                    Toast.makeText(this@MainActivity,"You must grant permission",Toast.LENGTH_LONG).show()
                }

            }).check()


        // Initialisation des vues
        image_view = findViewById(R.id.image_view)
        btn_upload = findViewById(R.id.btn_upload)

        findViewById<Button>(R.id.btn_address).setOnClickListener {
            addAddress(it)
        }

        //Service
        mService = apiUpload

        //View event (opération à réaliser lorsqu'on clique sur une vue)
        image_view.setOnClickListener { takePicture() }
        btn_upload.setOnClickListener { uploadFile() }

    }

    // Entrer l'adresse IP du serveur
    private fun addAddress(view: View) {
        val addressText = findViewById<EditText>(R.id.adress_edit)
        ip_address = addressText.text.toString()  // on récupère le texte entré dans ip_adress
        addressText.visibility = View.GONE        // on cache le champ IP adress
        view.visibility = View.GONE               // on cache le bouton Add
        image_view.visibility = View.VISIBLE      // on affiche le l'image view
        //btn_upload.visibility = View.VISIBLE

//       // Hide the keyboard
        val imm = getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager
        imm.hideSoftInputFromWindow(view.windowToken, 0)

    }

    // prise de la photo
    private fun takePicture() {
        //create an intent
        var intent:Intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        var time = SimpleDateFormat("yyyyMMdd_HHmmss").format(Date())
        var photoDir: File? = getExternalFilesDir(Environment.DIRECTORY_PICTURES)
        try{
            photoFile = File.createTempFile("photo"+time, ".jpg", photoDir)
            photoPath = photoFile.absolutePath
            photoUri = FileProvider.getUriForFile(this, "com.example.provider", photoFile)
            // Transfert uri vers l'intent pour enregistrement photo dans le fichier temporaire
            intent.putExtra(MediaStore.EXTRA_OUTPUT, photoUri)
            startActivityForResult(intent, TAKE_PICTURE_REQUEST)

        } catch (e : IOException) {
            e.printStackTrace()
        }

        btn_upload.visibility = View.VISIBLE        // on affiche le le bouton upload
    }

    private fun uploadFile() {
        //if (selectedUri != null){
        if (photoFile != null){
            // Affichage de la barre de progression
            dialog = ProgressDialog(this@MainActivity)
            dialog.setProgressStyle(ProgressDialog.STYLE_HORIZONTAL)
            dialog.setMessage("Uploading...")
            dialog.isIndeterminate=false
            dialog.max=100
            dialog.setCancelable(false)
            dialog.show()

            var file: File?= null
            try{
                //file = File(Common.getFilePath(this, selectedUri!!))
                file = photoFile
            }catch (e:URISyntaxException){e.printStackTrace()}
            if(file != null){
                val requestBody = ProgressRequestBody(file,this)
                val body = MultipartBody.Part.createFormData("image",file.name,requestBody)

                // l'envoie du fichier au serveur se fait en arrière plan (thread)
                Thread(Runnable{
                    mService.uploadFile(body)
                        .enqueue(object: retrofit2.Callback<String> {
                            override fun onFailure(call: retrofit2.Call<String>, t: Throwable) {
                                dialog.dismiss()
                                Toast.makeText(this@MainActivity, t.message,Toast.LENGTH_SHORT).show()
                            }

                            override fun onResponse(call: retrofit2.Call<String>, response: retrofit2.Response<String>) {
                                dialog.dismiss()
                                //val image_processed_link = StringBuilder("http://192.168.0.36:5000/").append(response.body()!!.replace("\"","")).toString()
                                val image_processed_link = StringBuilder("http://"+ip_address+":5000/").append(response.body()!!.replace("\"","")).toString()
                                Picasso.get().load(image_processed_link).into(image_view)
                                Toast.makeText(this@MainActivity, "Face Detected!!!",Toast.LENGTH_SHORT).show()
                            }
                        })
                }).start()
            }
            else {
                Toast.makeText(this@MainActivity, "Cannot upload this file!!!",Toast.LENGTH_SHORT).show()
            }

        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        // Si la photo a bien été prise
        if (resultCode == Activity.RESULT_OK){


            if (requestCode == TAKE_PICTURE_REQUEST){
                val image: Bitmap = BitmapFactory.decodeFile(photoPath)
                image_view.setImageBitmap(image)

            }
        }
    }

    override fun onProgressUpdate(percent: Int) {

    }
}