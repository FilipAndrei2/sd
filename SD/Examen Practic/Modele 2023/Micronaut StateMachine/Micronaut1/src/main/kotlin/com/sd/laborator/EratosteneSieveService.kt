package com.sd.laborator

import jakarta.inject.Singleton
import java.util.*

@Singleton
class EratosteneSieveService {
    // implementare preluata de la https://www.geeksforgeeks.org/sieve-eratosthenes-0n-time-complexity/

     /*
     isPrime[] : isPrime[i] este adevarat daca numarul i este prim
     prime[] : stocheaza toate numerele prime mai mici ca N
     SPF[] (Smallest Prime Factor) - stocheaza cel mai mic factor prim al numarului
     [de exemplu : cel mai mic factor prim al numerelor '8' si '16'
     este '2', si deci SPF[8] = 2 , SPF[16] = 2 ]
     */


    fun lengthList(a:List<Int>):Int{
        return a.size
    }
}