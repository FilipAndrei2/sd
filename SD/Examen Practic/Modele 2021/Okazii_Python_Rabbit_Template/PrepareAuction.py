from kafka import KafkaAdminClient
from kafka.admin import NewTopic
import time

from RabbitMqConnection import RabbitMqConsumer

if __name__ == '__main__':
    # Tot ce trebuie facut este sa se goleasca fisierul de result.txt
    f = open("result.txt", "w")
    f.write("")
    f.close()

    # Aici ar trebui sa goleasca toate cozile ...
    bidder_queue = RabbitMqConsumer(
        rabbit_queue="bidder.queue"
    )
    messageprocessor_queue = RabbitMqConsumer(
        rabbit_queue="messageprocessor.queue"
    )
    biddingprocessor_queue = RabbitMqConsumer(
        rabbit_queue="biddingprocessor.queue"
    )

    try:
        bidder_queue.receive_message()
    except Exception as e:
        print("except:{}".format(e))
    bidder_queue.list_msg.clear()
    print("Bidder queue empty.")

    try:
        messageprocessor_queue.receive_message()
    except Exception as e:
        print("except:{}".format(e))
    messageprocessor_queue.list_msg.clear()
    print("Messageprocessor queue empty.")

    try:
        biddingprocessor_queue.receive_message()
    except Exception as e:
        print("except:{}".format(e))
    biddingprocessor_queue.list_msg.clear()
    print("Biddingprocessor queue empty.")


    print("Gata! Microserviciile participante la licitatie pot fi pornite.")
