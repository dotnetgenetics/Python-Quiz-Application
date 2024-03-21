""" This is greg's version of the quiz application """
import json
import os
import quiz

def load_json_files(*file_names):
    """ Receives one or more file names and returns a list of dictionaries, each dictionary representing the contents of each file. """
    
    resulting_loads = []
    for file in file_names:
        with open(file) as file_object:
            current_load = json.load(file_object)
            resulting_loads.append(current_load)
    
    return resulting_loads

def create_compiled_data(questions, topics, past_scores):
    """ Create compiled data from the contents loaded from the questions, topics, and past_scores files """    
    
    # Creating an empty dictionary that will eventually be used to create the welcome table
    compiled_data = {}

    # Start filling in the welcome_page_info list with the topics
    for number, topic in topics.items():
        compiled_data[number] = { 'topic': topic }

    # Append one last item for "all" topics, we use int(max(topics)) and add 1 since the number of topics in topics.json might vary
    compiled_data[str(len(compiled_data) + 1)] = { 'topic': 'all' }
    
    # Fill in the compiled_data dictionary with the remaining data from the questions and past_scores objects (previously loaded from files)
    for data_key, data_value in compiled_data.items():

        data_value["question-ids"] = []
        if data_value["topic"] != 'all':
            for key, value in questions.items():
                if data_value["topic"] in value["topics"]:
                    data_value["question-ids"].append(key)
        else:
            for key, value in questions.items():
                data_value["question-ids"].append(key)

        data_value['questions-count'] = len(data_value['question-ids'])
        data_value['past-score'] = past_scores.get(data_key)

    return compiled_data

def print_welcome_page(compiled_data):    
    """ Takes in the compiled_data and does some formatting to print the welcome page to the app """
    
    table_titles = ['topic', 'questions', 'previous score']

    # Define the length of the longest title (for table sizing later on)
    max_length = len(max(table_titles, key=len))

    # Compare max title length to topics lengths to determine which one to use (+4 because of the numeration of each title)
    for value in compiled_data.values():
        if len(value['topic']) + 4 > max_length:
            max_length = len(value['topic']) + 4

    print('Welcome to your Python Learning App!\n')
    print('Select a topic to review and you will be asked a max of 10 questions per run. Good luck!\n')

    # Print table titles
    print('| {0:^{max_length}} | {1:^{max_length}} | {2:^{max_length}} |'
        .format(
            table_titles[0].title(),
            table_titles[1].title(),
            table_titles[2].title(),
            max_length=max_length))

    # Print table rows
    for key, value in compiled_data.items():
        print('| {0:{max_length}} | {1:^{max_length}} | {2:^{max_length}} |'
            .format(
                f'{key}. {value["topic"].title()}',
                value['questions-count'],
                value.get('past-score', '') or '',
                max_length=max_length))

def validated_input(prompt, valid_options, value_to_quit='q'):
    """ Validate user input, q to quit """

    # Prompt the user for input
    user_input = input(prompt)

    # Iterate through the while loop until the user_input is valid (and return valid input), or if the value_to_quit is entered raise a SystemExit exception
    flag = True
    while flag:
        if user_input == value_to_quit:
            raise SystemExit
        elif user_input not in valid_options:
            user_input = input(f'Please enter a valid option or \'{value_to_quit}\' to quit: ')
        else:
            return user_input
           
def clear():   
    """ Clears the terminal """

    # This is a shorthand if statement. If the OS is Windows os.name would == 'nt' and 'cls' would be used, for everything else 'clear' is used
    arg = 'cls' if os.name == 'nt' else 'clear'
    # Use the system() function from the os library to clear the terminal screen
    os.system(arg)

def main():    
    """ Runs main code """

    while True:
        # These are the files to be loaded
        questions_file = 'questions.json'
        topics_file = 'topics.json'
        past_scores_file = 'past_scores.json'

        # Load files as dictionaries and assign to each variable respectively
        questions, topics, past_scores = load_json_files(questions_file, topics_file, past_scores_file)

        # Create a list of dictionaries, each dictionary has one topic and it's corresponding data
        compiled_data = create_compiled_data(questions, topics, past_scores)
        
        # Call the clear function to clear the screen, defined earlier in the script
        clear()

        # Print welcome page - a table with all topics, their question count, and their previous scores
        print_welcome_page(compiled_data)

        # Get the topic_id as user input using the validated_input function. All wrapped in a try block in case the user quits along the way
        topic_id = validated_input('\nEnter the number of the topic you want to review (\'q\' to quit): ', list(compiled_data.keys()))

        # Create an instance of the the Quiz class based on the topic selected by the user and passing in compiled_data and questions
        chosen_quiz = quiz.Quiz(topic_id, compiled_data, questions)

        # Execute the run_quiz method from the Quiz instance named chosen_quiz. All wrapped in a try block in case the user quits along the way
        score, range_size = chosen_quiz.run_quiz()

        # Call the clear function to clear the screen, defined earlier in the script
        clear()

        # Compute the final score based on what was returned from the chosen_quiz method
        final_score = int(100 * score / range_size)

        # Update the value of the past_scores dictionary for the corresponding topic
        past_scores[topic_id] = str(final_score) + '%'

        # Write into the past_scores.json file the updated past_scores dictionary
        with open('past_scores.json', 'w') as file_object:
            json.dump(past_scores, file_object)

        # Return score, selecting prompt based on how high is was
        if final_score == 100:
            print(f'\nUnbelieveable! You scored {final_score}%!\n')
        elif final_score >= 90:
            print(f'\nExcellent job! You scored {final_score}%!\n')
        elif final_score >= 80:
            print(f'\nAwesome! You scored {final_score}%!\n')
        else:
            print(f'\nYou scored {final_score}%\n')

        # Finally, ask the user if they want to re-run the app or quit
        another_try = input('Enter \'y\' to run the app again, any other key to quit: ')
        if another_try != 'y':
            break
    
if __name__ == '__main__':
    main()