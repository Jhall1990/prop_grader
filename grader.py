#!/usr/bin/env python

import csv
import argparse


class User(object):
    def __init__(self, name, user_answers):
        self.name = name
        self.user_answers = user_answers
        self.score = 0
        self.mvp_answer = ""

    def grade(self, correct_answers):
        zip_answers = zip(self.user_answers, correct_answers)
        for index, answers in enumerate(zip_answers):
            user_answer = answers[0]
            correct_answer = answers[1]

            # Special case to handle the mvp answer.
            if index == 67:
                self.mvp_answer = user_answer
            elif user_answer == correct_answer:
                self.score += 1


def read_csv(csv_file):
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        rows = [i for i in reader]
    return rows

def get_users(csv_data, answer_email):
    user_list = []
    correct_answers = None

    # Skip the first row as it it's just the column names
    for row in csv_data[1:]:
        name = row[1].lower()
        answers = row[2:]

        if name == answer_email:
            correct_answers = answers
        else:
            user_list.append(User(name, answers))

    return user_list, correct_answers

def display_results(user_list, correct_answers):
    # Score each users entry.
    for user in user_list:
        user.grade(correct_answers)

    # Sort the users by score.
    user_list.sort(key=lambda x: x.score, reverse=True)

    # Print out the users and their scores
    for user in user_list:
        print("User: {} | Score: {} | MVP: {}".format(user.name, user.score, user.mvp_answer))
    print("Actual MVP: {}".format(correct_answers[67]))


def configure_arg_parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", help="The csv file location", required=True)
    ap.add_argument("--answer", help="The email address that submitted answers", required=True)
    return ap

if __name__ == "__main__":
    parser = configure_arg_parse()
    args = parser.parse_args()

    csv_rows = read_csv(args.csv)
    users, actual_answers = get_users(csv_rows, args.answer)
    display_results(users, actual_answers)
