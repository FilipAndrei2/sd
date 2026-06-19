package com.sd.laborator.interfaces

import com.sd.laborator.pojo.Person

interface ICacheInterface {
    fun checkResource(url:String):Boolean
    fun getResource(url:String) : List<Person?>
    fun addResource(url:String, persons: List<Person>)
}