from kafka import KafkaConsumer, KafkaProducer

from RabbitMqConnection import RabbitMqProducer, RabbitMqConsumer


class Auctioneer:
    def __init__(self):
        super().__init__()

        # Va produce spre MessageProcessor
        self.producer = RabbitMqProducer(exchange="bidder.direct",
                                         routing_key="messageprocessor.routingkey")
        # Va consuma cererile de la Bidderi din Bidder queue
        self.consumer = RabbitMqConsumer(rabbit_queue="bidder.queue")

    def receive_bids(self):
        # Se preiau toate bid-urile din coada de bid-uri
        print("[Auctioneer] Astept oferte pentru licitatie...")

        # Execut receive_message pentru a popula lista de mesaje din consumer
        try:
            self.consumer.receive_message()
        except Exception as e:
            print("except:{}".format(e))

        # Cat timp exista elemente de procesat in lista respectiva
        while len(self.consumer.list_msg) != 0:
            # Mesajul este de tip id:{}_amount:{}
            bidder_message = self.consumer.list_msg.pop()
            bidder_message_splitted = bidder_message.split("_")

            # Extragem informatiile necesare din mesaj
            identity = bidder_message_splitted[0].split(":")[1]
            amount = bidder_message_splitted[1].split(":")[1]
            print("[Auctioneeer] {} a licitat {}".format(identity, amount))

            # Trimit mai departe mesajul spre MessageBidderMicroservice
            self.producer.send_message(bidder_message)

            # Interceptez urmatorul mesaj
            try:
                self.consumer.receive_message()
            except Exception as e:
                print("except:{}".format(e))

        # In aceasta varianta, licitatia se va termina atunci cand nu mai sunt bid-uri in coada
        self.finish_auction()

    def finish_auction(self):
        print("[Auctioneer] Licitatia s-a incheiat!")

        # Trimitem spre MessageProcessor ca poate incepe procesarea, de vreme
        auction_finished_message = "incheiat"
        self.producer.send_message(auction_finished_message)

    def run(self):
        try:
            self.receive_bids()
        except Exception as e:
            print("except:{}".format(e))


if __name__ == '__main__':
    auctioneer = Auctioneer()
    auctioneer.run()
