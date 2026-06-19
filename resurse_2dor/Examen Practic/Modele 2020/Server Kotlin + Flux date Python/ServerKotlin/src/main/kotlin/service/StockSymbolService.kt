package service

import com.google.gson.Gson
import khttp.get
import model.StockItem

class StockSymbolService {
    companion object {
        private const val urlSymbols = "https://finnhub.io/api/v1/stock/symbol"
        private const val token = "cian1upr01qn522c4380cian1upr01qn522c438g"
    }

    fun getSymbols() : List<StockItem> = get("$urlSymbols?exchange=US&token=$token").jsonArray.map {
        Gson().fromJson(it.toString(), StockItem::class.java)
    }
}