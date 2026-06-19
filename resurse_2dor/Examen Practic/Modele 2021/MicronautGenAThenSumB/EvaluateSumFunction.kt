package com.sd.laborator;

import io.micronaut.function.FunctionBean
import io.micronaut.function.executor.FunctionInitializer
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import java.util.function.Supplier
import javax.inject.Inject

@FunctionBean("eratostene")
class EvaluateSumFunction : FunctionInitializer(), Supplier<SolutionResponse> {
    @Inject
    private lateinit var evaluateSumService: EvaluateSumService

    @Inject
    private lateinit var generateADTService: GenerateADTService

    private val LOG: Logger = LoggerFactory.getLogger(EvaluateSumFunction::class.java)

    override fun get(): SolutionResponse {
        val A = generateADTService.generateADT(100)
        val B = evaluateSumService.evaluateSum(A)

        val solutionResponse = SolutionResponse()
        solutionResponse.setList(B.toList())
        return solutionResponse
    }
}

/**
 * This main method allows running the function as a CLI application using: echo '{}' | java -jar function.jar 
 * where the argument to echo is the JSON to be parsed.
 */
fun main(args : Array<String>) { 
    val function = EvaluateSumFunction()
    function.run(args) { function.get() }
}