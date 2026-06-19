from RabbitMqConnection import RabbitMqConsumer, RabbitMqProducer


class Auctioneer:
    def __init__(self):
        self.consumer = RabbitMqConsumer(rabbit_queue="bidder.queue")
        self.producer = RabbitMqProducer(exchange="bidder.direct", routing_key="messageprocessor.routingkey")
        self.loggerProducer = RabbitMqProducer(exchange="bidder.direct", routing_key="bidding_logger.routingkey")

    def receive_bids(self):
        # se preiau toate ofertele din topicul bids_topic
        print("[Auctioneer] Astept oferte pentru licitatie...")
        self.loggerProducer.send_message("info:[Auctioneer] Astept oferte pentru licitatie...")

        while True:
            receiver_message = None
            try:
                receiver_message = self.consumer.receive_message()
            except Exception as e:
                self.loggerProducer.send_message("except:{}".format(e))
            
            # Se iese din loop datorita neprimirii de mesaje in timp util
            if receiver_message == None:
                break

            # mesajul e de tip identity:NUME_amount:SUMA
            receiver_message = receiver_message.split("_")
            identity = receiver_message[0].split(":")[1]
            amount = int(receiver_message[1].split(":")[1])
            print("[Auctioneeer] {} a licitat {}".format(identity, amount))
            self.loggerProducer.send_message("info:[Auctioneeer] {} a licitat {}".format(identity, amount))

            rabbit_msg = "_".join(receiver_message)
            # trimit mesaje catre MessageProcessor
            self.producer.send_message(rabbit_msg)

        # bids_consumer genereaza exceptia StopIteration atunci cand se atinge timeout-ul de 10 secunde
        self.finish_auction()

    def finish_auction(self):
        print("[Auctioneer] Licitatia s-a incheiat!")
        self.loggerProducer.send_message("info:[Auctioneer] Licitatia s-a incheiat!")

        # notificam MessageProcessor ca poate incepe procesarea mesajelor
        auction_finished_message = "incheiat"
        self.producer.send_message(auction_finished_message)

    def run(self):
        try:
            self.receive_bids()
        except Exception as e:
            self.err.send_message("except:{}".format(e))


if __name__ == '__main__':
    auctioneer = Auctioneer()
    auctioneer.run()
