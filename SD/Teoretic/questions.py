import random

if __name__ == "__main__":

    f = open("all_questions.txt", "r")
    content = f.readlines()
    questions = []

    for line in content:
        questions.append(line)

    while True:
        print("Intrebare: ")
        index = random.randint(0, len(questions))
        print(questions[index])
        print("")
        next = input("Next question ... ")