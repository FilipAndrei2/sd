import os
import time

from kafka import KafkaProducer, KafkaConsumer
from random import randint
from uuid import uuid4

from RabbitMqConnection import RabbitMqProducer


class Bidder:
    def __init__(self):
        super().__init__()

        # Bidder va comunica cu Auctioneer prin rabbitmq
        self.producer = RabbitMqProducer(
            exchange="bidder.direct",
            routing_key="bidder.routingkey"
        )
        # Rezultatul va fi citit din fisier
        self.consumer = open("result.txt", "r")


        # Se genereaza bid-ul si id-ul bidder-ului
        self.my_bid = randint(1000, 10_000)  # se genereaza oferta ca numar aleator intre 1000 si 10.000
        self.my_id = uuid4()  # se genereaza un identificator unic pentru ofertant

    def bid(self):
        # Mesajul care se trimite este doar un string, asa ca va trebui contruit
        bid_message = "id:{}_amount:{}".format(self.my_id, self.my_bid)
        self.producer.send_message(bid_message)
        print("[ID:{}] Sent to bid queue {}".format(self.my_id, bid_message))

        # Exista o sansa din 2 ca oferta sa fie trimisa de 2 ori pentru a simula duplicatele
        if randint(0, 1) == 1:
            self.producer.send_message(bid_message)

    def get_winner(self):
        # Se asteapta raspunsul licitatiei
        print("[ID:{}]Astept rezultatul licitatiei...".format(self.my_id))

        # Cat timp dimensiunea fisierului rezultat este nula, citeste din el
        ready = False
        while ready is False:
            # Wait optional ca sa nu faca overload
            # time.sleep(0.1)
            if os.stat("result.txt").st_size != 0:
                ready = True

        # Rezultatul este pregatit pentru a fi citit
        result = self.consumer.readline()

        # Se extrage identitatea castigatorului din mesajul de tipul
        # winner:id
        identity = result.split(":")[1]

        if identity == str(self.my_id):
            print("[ID:{}] Am castigat!!!". format(self.my_id))
        else:
            print("[ID:{}] Am pierdut ...".format(self.my_id))

    def run(self):
        self.bid()
        self.get_winner()


if __name__ == '__main__':
    bidder = Bidder()
    bidder.run()
