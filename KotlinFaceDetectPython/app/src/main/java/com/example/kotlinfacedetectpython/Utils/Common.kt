package com.example.kotlinfacedetectpython.Utils

import android.annotation.SuppressLint
import android.content.ContentUris
import android.content.Context
import android.database.Cursor
import android.net.Uri
import android.os.Build
import android.os.Environment
import android.provider.DocumentsContract
import android.provider.DocumentsContract.isDocumentUri
import android.provider.MediaStore
import java.lang.Exception
import java.net.URISyntaxException

object Common{
    @SuppressLint("NewApi")
    @Throws(URISyntaxException::class)
    fun getFilePath(context: Context, uri: Uri):String?{
        var uri=uri
        var selection:String?=null
        var selectionArgs:Array<String>?=null

        if(Build.VERSION.SDK_INT >=19 && isDocumentUri(context,uri)){
            if(isExternalStorageDocument(uri)){
                val docID = DocumentsContract.getDocumentId(uri)
                val split = docID.split(":".toRegex()).dropLastWhile { it.isEmpty() }.toTypedArray()
                return Environment.getExternalStorageDirectory().toString()+"/"+split[1]
            }
            else if(isDownloadsDocument(uri)){
                val id = DocumentsContract.getDocumentId(uri)
                uri = ContentUris.withAppendedId(Uri.parse("content://downloads/public_downloads"), id.toLong())
            }
            else if(isMediaDocument(uri)){
                val docID = DocumentsContract.getDocumentId(uri)
                val split = docID.split(":".toRegex()).dropLastWhile { it.isEmpty() }.toTypedArray()
                val type = split[0]

                if("image".equals(type))
                    uri = MediaStore.Images.Media.EXTERNAL_CONTENT_URI
                else if("video".equals(type))
                    uri = MediaStore.Video.Media.EXTERNAL_CONTENT_URI
                else if("audio".equals(type))
                    uri = MediaStore.Audio.Media.EXTERNAL_CONTENT_URI
                selection = "_id=?"
                selectionArgs = arrayOf(split[1])

            }
        }

        if("content".equals(uri.scheme!!, ignoreCase = true)){
            val projection = arrayOf(MediaStore.Images.Media.DATA)
            var cursor: Cursor? = null
            try{
                cursor = context.contentResolver.query(uri,projection,selection,selectionArgs, null)
                val column_index = cursor!!.getColumnIndex(MediaStore.Images.Media.DATA)
                if (cursor.moveToFirst())
                    return cursor.getString(column_index)
            }catch (e:Exception){}
        }else if("file".equals(uri.scheme!!, ignoreCase = true))
            return uri.path
        return null
    }

    private fun isMediaDocument(uri: Uri): Boolean {
        return "com.android.providers.media.documents".equals(uri.authority)
    }

    private fun isDownloadsDocument(uri: Uri): Boolean {
        return "com.android.providers.downloads.documents".equals(uri.authority)
    }

    private fun isExternalStorageDocument(uri: Uri): Boolean {
        return "com.android.externalStorage.documents".equals(uri.authority)
    }


}