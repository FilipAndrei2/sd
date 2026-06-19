import time

from RabbitMqConnection import RabbitMqProducer, RabbitMqConsumer


class MessageProcessor:
    def __init__(self):
        # Va produce mesaje pentru coada lui biddingprocessor
        self.producer = RabbitMqProducer(exchange="bidder.direct",
                                         routing_key="biddingprocessor.routingkey")
        # Va consuma mesage de la MessajgeProcessor
        self.consumer = RabbitMqConsumer(rabbit_queue="messageprocessor.queue")

        # Ofertele se pun in dictionar, sub forma de perechi <IDENTITATE_OFERTANT, MESAJ_OFERTA>
        self.bids = dict()

    def get_and_process_messages(self):
        # Se asteapta notificarea de la Auctioneer pentru incheierea licitatiei
        print("[MessageProcessor] Astept notificare de la toate entitatile Auctioneer pentru incheierea licitatiei...")
        time.sleep(2)

        # A ajuns prima notificare, se asteapta si celelalte notificari timp de maxim 15 secunde
        try:
            self.consumer.receive_message()
        except Exception as e:
            print("except:{}".format(e))

        # Cat timp coada contine elemente
        while len(self.consumer.list_msg) != 0:
            # Extrag mesajul din coada
            msg = str(self.consumer.list_msg.pop())

            # Interceptez urmatorul mesaj
            try:
                self.consumer.receive_message()
            except Exception as e:
                print("except:{}".format(e))

            # Cazul in care mesajul este de tip incheiat
            if msg == "incheiat":
                print("[MessageProcessor] Licitatie incheiata. Procesez mesajele cu oferte...")
                break

            # Procesez mesajul si il salvez in dictionar
            split_message = msg.split("_")

            # Structura mesaj: id:{}_amount:{}
            self.bids[split_message[0].split(":")[1]] = split_message[1].split(":")[1]

        # Sortez  dupa valoare
        sorted_bids = {k: v for k, v in sorted(self.bids.items(), key=lambda item: item[1])}
        self.finish_processing(sorted_bids)

    def finish_processing(self, sorted_bids):
        # Procesarea s-a incheiat
        print("[MessageProcessor] Procesarea s-a incheiat! Trimit urmatoarele oferte:")

        # Pentru fiecare bid
        for IdBid in sorted_bids:
            # Extrag informatiile necesare
            identity = IdBid
            amount = sorted_bids[identity]
            print("[MessageProcessor] {} a licitat {}.".format(identity, amount))

            # Creez mesaj pentru BidderProcessor
            rabbit_msg = "id:{}_amount:{}".format(identity, amount)
            self.producer.send_message(rabbit_msg)

        # dupa ce terminam de procesat, anuntam ca MessageProcessor a incheiat munca
        self.producer.send_message("incheiat")

    def run(self):
        self.get_and_process_messages()


if __name__ == '__main__':
    message_processor = MessageProcessor()
    message_processor.run()
