package com.sd.laborator.services

import com.sd.laborator.interfaces.ICacheInterface
import com.sd.laborator.pojo.Person
import org.springframework.stereotype.Service
import java.util.*

@Service
class CacheService : ICacheInterface {

    private var resource = mutableMapOf<String, Pair<Date,List<Person>>>()
    private val expireTime = 1000 * 60 * 30

    override fun checkResource(url: String): Boolean {
        var now = Date()
        if(url in resource.keys )
        {
            if(now.time - (resource[url]?.first?.time ?: now.time) <= expireTime)
            {
                return true
            }
        }
        return false
    }

    override fun getResource(url: String): List<Person?> {
        return resource[url]!!.second
    }

    override fun addResource(url: String, persons: List<Person>) {
        resource[url] = Pair(Date(), persons)
    }
}