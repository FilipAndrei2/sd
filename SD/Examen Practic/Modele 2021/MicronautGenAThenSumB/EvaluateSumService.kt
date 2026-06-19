package com.sd.laborator

import java.util.*
import javax.inject.Singleton

@Singleton
class EvaluateSumService {

    fun evaluateSum(list:List<Int>): List<Int>{
        val solution = mutableListOf<Int>()
        if(list.isNotEmpty()){
            // evaluate first element
            solution.add(list[0] * list[0])

            // evaluate all elements
            for(i in 1..list.size-1){
                solution.add(solution[i-1] + list[i]*list[i])
            }
        }

        return solution
    }

    init {
    }
}