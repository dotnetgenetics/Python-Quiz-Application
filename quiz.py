import random
import main

class Quiz():
    """ Represents a Quiz based on the compiled data and a specified topic """

    def __init__(self, topic_id, compiled_data, questions):
        """ Initializes the Quiz instance """

        self.topic_id = topic_id
        self.compiled_data = compiled_data
        self.questions = questions
        self.questions_to_ask = compiled_data[topic_id]['question-ids']

        # Use the random module to randomize the order of the questions to ask
        random.shuffle(self.questions_to_ask)

    def run_quiz(self):
        """ Class method to run the Quiz instance and returns the score and the range_size (number of questions asked) """

        # Define score to start at 0 and increases with each correct answer
        score = 0
        
        # Define range_size as the number of questions to be asked, maxing out at 10 to keep the quiz short
        range_size = min(10, len(self.questions_to_ask))
        for index in range(range_size):
            current_question = self.questions.get(self.questions_to_ask[index])
            main.clear()            
            # The ask_question function runs and returns True/False for a(n) correct/incorrect answer, if correct increase the score
            if ask_question(current_question, index + 1, range_size):
                score += 1
            input('enter any key to continue ')

        return score, range_size
    
def ask_question(question, question_number, total_questions):
    """ Asks the question passed in to the user and returns True/False if answered correctly/incorrectly respectively """
    
    # Create an empty list that will be populated with the question's options and then suffled
    options = []
    for option in question['options'].values():
        options.append(option)
    random.shuffle(options)

    # Create a tuple with the first 7 letters of the alphabet
    letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
    # The shuffled_options dictionary will have the options in random order
    shuffled_options = {}
    for index in range(len(options)):
        shuffled_options[letters[index]] = options[index]

    # Print the question prompt
    print(f' - ({question_number}/{total_questions}) {question["question"]}')

    # Print shuffled_options for the user to choose from
    for key, value in shuffled_options.items():
        print(f'\t{key}. {value}')

    # Define the correct_answer from the question object
    correct_answer = question['options'][question['answer']]
    # Prompt user for input by using the validated_input function
    user_input = main.validated_input('Enter your answer (\'q\' to quit): ', list(shuffled_options.keys()))
    # Define the user_anser from suffled_options
    user_answer = shuffled_options[user_input]
    
    # Compare answers to determine if correct/incorrect and return True/False respectively
    if user_answer == correct_answer:
        print('\nThat\'s correct! Good job!\n')
        return True
    else:
        print(f'\nYou almost got it! The right answer was "{correct_answer}".\n')
        return False