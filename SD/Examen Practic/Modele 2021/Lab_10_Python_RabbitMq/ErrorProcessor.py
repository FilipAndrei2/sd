import time

from RabbitMqConnection import RabbitMqConsumer


class ErrorProcessor:
    def __init__(self):
        self.consumer = RabbitMqConsumer(rabbit_queue="errors.queue")
        self.file = None  # fisierul in care scriem erori

    def errors(self):
        print("[ErrorProcessor] Initializare microserviciu de statistica.")
        time.sleep(5)
        self.file = open("errors.txt", "w")
        try:
            self.consumer.receive_message()
        except Exception as e:
            self.file.write(str(e) + "\n")
        while len(self.consumer.list_msg) != 0:
            msg = self.consumer.list_msg.pop()
            self.file.write(msg + "\n")
            try:
                self.consumer.receive_message()
            except Exception as e:
                self.file.write(str(e) + "\n")
        self.file.close()

    def run(self):
        self.errors()
        print("[ErrorProcessor] Incheierea activitatii.")


if __name__ == "__main__":
    processor = ErrorProcessor()
    processor.run()
