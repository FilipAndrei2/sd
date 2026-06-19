import com.google.gson.Gson
import model.NewsItem
import service.StockSymbolService
import khttp.get
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import model.StockItem
import java.lang.Exception
import java.net.ServerSocket
import java.net.Socket
import java.net.SocketException
import java.sql.Timestamp

class Application {
    private val symbols: List<StockItem>

    // Create obiect companion pentru valorile constante
    companion object CONSTANTS {
        private const val urlCompanyNews = "https://finnhub.io/api/v1/company-news"
        private const val token = "cian1upr01qn522c4380cian1upr01qn522c438g"
        private const val fromDate = "2023-01-23"
        private const val toDate = "2023-06-23"
    }

    // Initializare lista de simboluri
    init {
        val stockSymbolService = StockSymbolService()
        symbols = stockSymbolService.getSymbols()
    }

    // Functie privata pentru trimiterea de mesaje
    private fun sendMessage(client: Socket?, message: String) {
        println(message)
        client?.getOutputStream()?.write("$message\n".toByteArray(Charsets.UTF_8))
    }

    // Functie privata pentru primirea stirilor asociate unei companii listate
    private fun getNews(symbol: String) : List<NewsItem> = try {
        get("$urlCompanyNews?symbol=${symbol}&from=$fromDate&to=$toDate&token=$token").jsonArray.map {
                it2 -> Gson().fromJson(it2.toString(), NewsItem::class.java) }
    } catch(e: Exception) {
        listOf()
    }

    // Functie ce lanseaza server-ul la care se conecteaza clientii
    fun startStreaming() = runBlocking {
        val streamingServer = ServerSocket(5678)
        while(true) {
            val clientConnection = streamingServer.accept()

            println("Log ${Timestamp(System.currentTimeMillis())}: Subscriber conectat " +
                    "${clientConnection.inetAddress.hostAddress}:${clientConnection.port}")

            val coroutineJob = launch {
                try {
                    // Get news and send to client
                    symbols.forEach {
                        println("Log ${Timestamp(System.currentTimeMillis())}: Serverul cere stiri pentru simbolul ${it.symbol} ")
                        val news = getNews(it.symbol)
                        news.forEach {
                            n -> sendMessage(clientConnection, Gson().toJson(n))
                            println("Log ${Timestamp(System.currentTimeMillis())}: Serverul trimite catre " +
                                    "${clientConnection.inetAddress.hostAddress}:${clientConnection.port}.")
                            delay(3000L)
                        }
                    }
                }
                catch(e: SocketException) {
                    println("Log ${Timestamp(System.currentTimeMillis())}: Datele nu au putut fi trimise catre "+
                            "${clientConnection.inetAddress.hostAddress}:${clientConnection.port}.")
                }
            }
            coroutineJob.join()
            println("Log ${Timestamp(System.currentTimeMillis())}: Corutina asociata clientului " +
                    "${clientConnection.inetAddress.hostAddress}:${clientConnection.port} s-a dus drq.")
        }
    }
}

fun main() {
    val application = Application()
    application.startStreaming()
}