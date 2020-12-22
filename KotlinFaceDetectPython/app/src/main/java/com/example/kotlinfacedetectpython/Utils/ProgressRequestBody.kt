package com.example.kotlinfacedetectpython.Utils

import android.os.Handler
import android.os.Looper
import okhttp3.MediaType
import okhttp3.RequestBody
import okio.BufferedSink
import java.io.File
import java.io.FileInputStream
import java.io.IOException

class ProgressRequestBody(private val file: File,
                          private val listener:IUploadCallback):RequestBody() {

    companion object{
        private val DEFAULT_BUFFER_SIZE = 4096
    }

    override fun contentType(): MediaType? {
        return MediaType.parse("image/*")
    }

    @Throws(IOException::class)
    override fun writeTo(sink: BufferedSink) {
        val fileLength = file.length()
        val buffer = ByteArray(DEFAULT_BUFFER_SIZE)
        val `in` = FileInputStream(file)
        var uploaded : Long = 0
        try{
            var read:Int
            val handler = Handler(Looper.getMainLooper())
            while(`in`.read(buffer).let {
                    read = it; it !=-1
                }){
                handler.post(ProgressUpdater(uploaded,fileLength))
                uploaded+=read.toLong()
                sink.write(buffer, 0, read)
            }
        }finally {
            `in`.close()
        }
    }

    inner class ProgressUpdater(private val uploaded: Long, private val fileLength: Long) : Runnable{
        override fun run() {
            listener.onProgressUpdate((100*uploaded / fileLength).toInt())
        }

    }

}