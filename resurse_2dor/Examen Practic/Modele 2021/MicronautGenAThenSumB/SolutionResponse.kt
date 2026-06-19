package com.sd.laborator

import io.micronaut.core.annotation.Introspected

@Introspected
class SolutionResponse {
	private var list: List<Int>? = null

	fun getList(): List<Int>? {
		return list
	}

	fun setList(list: List<Int>?) {
		this.list = list
	}
}


