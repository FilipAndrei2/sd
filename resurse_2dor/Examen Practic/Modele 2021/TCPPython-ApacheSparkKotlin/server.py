import socket
import time
import threading
import requests
import datetime

ip = "127.0.0.1"
port = 8910
addr = (ip, port)

TOKEN = "brmr2kfrh5rcss140jmg"

symbols = requests.get('https://finnhub.io/api/v1/stock/symbol?exchange=US&token=' + TOKEN).json()


def process_client(c_socket, address):
    global symbols
    try:
        print(str(address) + " connected!")
        today = datetime.datetime.now()
        todaystr = today.strftime("%Y-%m-%d")

        # print(symbols)
        for index in range(len(symbols)):
            my_symbol = symbols[index]
            news = requests.get('https://finnhub.io/api/v1/company-news?symbol=' + my_symbol.get("symbol") + '&from=' +
                                todaystr + '&to=' + todaystr +
                                '&token=' + TOKEN).text

            if len(news) > 2:
                print(news)
                if not news.__contains__('{"error":"API limit reached. Please try again later. Remaining Limit: 0"}'):
                    c_socket.sendall(bytes(news + "\n", 'utf-8'))
                    time.sleep(3)



        c_socket.close()
        print("disconnected")
    except Exception as ex:
        print(str(ex))


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(addr)
    server_socket.listen()

    while True:
        client_socket, __ = server_socket.accept()
        threading.Thread(target=process_client, args=(client_socket, __)).start()
