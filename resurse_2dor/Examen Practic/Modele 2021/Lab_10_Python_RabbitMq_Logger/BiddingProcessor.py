import time

from RabbitMqConnection import RabbitMqConsumer, RabbitMqProducer


class BiddingProcessor:
    def __init__(self):
        self.producer = RabbitMqProducer(exchange="bidder.direct", routing_key="winner.routingkey")
        self.consumer = RabbitMqConsumer(rabbit_queue="bidding_processor.queue")
        self.loggerProducer = RabbitMqProducer(exchange="bidder.direct", routing_key="bidding_logger.routingkey")

    def get_processed_bids(self):
        # se preiau toate ofertele procesate din topicul processed_bids_topic
        print("[BiddingProcessor] Astept ofertele procesate de MessageProcessor...")
        self.loggerProducer.send_message("info:[BiddingProcessor] Astept ofertele procesate de MessageProcessor...")
        # sa aibe timp restu microserviciilor sa-si incheie munca
        time.sleep(30)
        # ofertele se stocheaza sub forma de perechi <id:<ID>_amount:<SUMA>>
        bids = dict()
        
        while True:
            receiver_message = None
            try:
                receiver_message = self.consumer.receive_message()
            except Exception as e:
                self.loggerProducer.send_message("except:{}".format(e))
            
            # Se iese din loop datorita neprimirii de mesaje in timp util
            if receiver_message == None:
                break
            
            if receiver_message == "incheiat":
                break

            receiver_message = receiver_message.split("_")
            bids[receiver_message[0].split(":")[1]] = receiver_message[1].split(":")[1]
            try:
                self.consumer.receive_message()
            except Exception as e:
                self.loggerProducer.send_message("except:{}".format(e))

        self.decide_auction_winner(bids)

    def decide_auction_winner(self, bids):
        print("[BiddingProcessor] Procesez ofertele...")
        self.loggerProducer.send_message("info:[BiddingProcessor] Procesez ofertele...")

        if len(bids) == 0:
            print("[BiddingProcessor] Nu exista nicio oferta de procesat.")
            self.loggerProducer.send_message("info:[BiddingProcessor] Nu exista nicio oferta de procesat.")
            return

        # sortare dupa oferte, descrescator
        sorted_bids = sorted(bids.keys(), reverse=False)

        # castigatorul este ofertantul care a oferit pretul cel mai mare
        winner = bids[sorted_bids[0]]

        print("[BiddingProcessor] Castigatorul este:")
        self.loggerProducer.send_message("info:[BiddingProcessor] Castigatorul este:")
        print("\t{} - pret licitat: {}".format(winner, sorted_bids[0]))
        self.loggerProducer.send_message("info:\t{} - pret licitat: {}".format(winner, sorted_bids[0]))

        # se trimite rezultatul licitatiei pentru ca entitatile Bidder sa il preia din topicul corespunzator
        for i in range(0, len(sorted_bids)):
            self.producer.send_message("winner:{}".format(sorted_bids[0]))
            self.loggerProducer.send_message("info:winner:{}".format(sorted_bids[0]))


    def run(self):
        self.get_processed_bids()


if __name__ == '__main__':
    bidding_processor = BiddingProcessor()
    bidding_processor.run()
