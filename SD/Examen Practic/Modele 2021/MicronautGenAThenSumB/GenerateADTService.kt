package com.sd.laborator

import java.util.*
import javax.inject.Singleton
import kotlin.random.Random

@Singleton
class GenerateADTService {
    private val MAX_ELEM_SIZE = 100

    fun generateADT(sizeOfADT: Int): List<Int>{
        val solution = mutableListOf<Int>()

        for(i in 0..sizeOfADT){
            solution.add(Random.nextInt(MAX_ELEM_SIZE))
        }

        return solution
    }

}