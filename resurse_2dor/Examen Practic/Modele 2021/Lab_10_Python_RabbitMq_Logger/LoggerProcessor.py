import time
import logging

from RabbitMqConnection import RabbitMqConsumer

class LoggerProcessor:
    def __init__(self):
        self.consumer = RabbitMqConsumer(rabbit_queue="bidding_logger.queue")

        logging.basicConfig(filename="application_log.log", format='[%(asctime)s] %(message)s', filemode='w', )

        self.logger = logging.getLogger(__name__)

        # dezactivare log automat din alte module
        logging.getLogger("pika").setLevel(logging.CRITICAL)
        logging.getLogger("retry").setLevel(logging.CRITICAL)
        
        self.logger.setLevel(logging.INFO)

    def receive_messages(self):
        print("[LoggerProcessor] Initializare logger. Se asteapta mesaje...")
        self.logger.info("[LoggerProcessor] Initializare logger. Se asteapta mesaje...")

        while True:
            
            received_message : str = self.consumer.receive_message_infinite_tries()

            try:
                received_message = received_message.split(':', 1)
            except Exception as e:
                self.logger.warning(received_message)
                continue

            messageType = received_message[0]
            message = received_message[1]

            if messageType == "except":
                self.logger.error(message)
            elif messageType == "info":
                self.logger.info(message)
            elif messageType == "stop":
                self.logger.info("[LoggerProcessor] Incheierea activitatii.")
                break


    def run(self):
        self.receive_messages()


if __name__ == "__main__":
    processor = LoggerProcessor()
    processor.run()
