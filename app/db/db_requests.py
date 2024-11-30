import sqlite3

class DataBase:
    def __init__(self):
        self.__connection = sqlite3.connect('data/data.db')
        self.__cursor = self.__connection.cursor()

    def get_questions_answers(self) -> list[list]:
        self.__cursor.execute(
        """
            SELECT questions.question_id, questions.question, group_concat(answers.answer, ';') 
            FROM questions
            INNER JOIN answers ON questions.question_id=answers.question_id
            GROUP BY questions.question_id
            ORDER BY questions.question_id
        """)
        source_data = self.__cursor.fetchall()
        self.__connection.commit()
        self.__connection.close()
        return source_data

    def get_animals_data(self, answers_max_to_min) -> list[list]:
        self.__cursor.execute(
        f"""
            SELECT * FROM animals
            WHERE answers = {answers_max_to_min}
            ORDER BY animal_id
        """)
        animals_data = self.__cursor.fetchall()
        self.__connection.commit()
        self.__connection.close()
        return animals_data

    def insert_application(self, person: dict) -> None:
        self.__cursor.execute(
            "INSERT INTO applications (name_user, phone_user, email_user, content) VALUES (?,?,?,?)",
            tuple(person.values())
        )

        self.__connection.commit()
        self.__connection.close()

    def insert_feedback_data(self, feedback: dict) -> None:
        self.__cursor.execute(
            "INSERT INTO feedback (name_user, content) VALUES (?,?)",
            tuple(feedback.values())
        )
        self.__connection.commit()
        self.__connection.close()

    def insert_questions_answers(self, questions_answers: dict) -> bool:

        self.__cursor.execute(
            'SELECT question FROM questions WHERE question = (?)',
            (questions_answers['question'],)
        )
        status = self.__cursor.fetchone()

        if status is not None:
            return False

        self.__cursor.execute(
            "INSERT INTO questions (question) VALUES (?)",
            (questions_answers['question'],)
        )
        self.__cursor.execute(
            "SELECT question_id FROM questions where question = (?)",
            (questions_answers['question'],)
        )
        question_id = self.__cursor.fetchone()
        answers = [(line, *question_id) for line in questions_answers['answers']]
        self.__cursor.executemany(
            "INSERT INTO answers (answer, question_id) VALUES (?, ?)",
            answers
        )
        self.__connection.commit()
        self.__connection.close()
        return True

    def get_all_questions(self) -> list[list]:
        self.__cursor.execute('SELECT * FROM questions')
        all_questions = self.__cursor.fetchall()
        self.__connection.commit()
        self.__connection.close()
        return all_questions

    def update_question(self, new_question: str, question_id: int) -> None:
        self.__cursor.execute(
            "UPDATE questions SET question = (?) WHERE question_id = (?)",
            (new_question, question_id)
        )
        self.__connection.commit()
        self.__connection.close()

    def delete_question_answers(self, question_id: int) -> None:
        self.__cursor.execute(
            "DELETE FROM questions WHERE question_id = (?)",
            (question_id,)
        )
        self.__cursor.execute(
            "DELETE FROM answers WHERE question_id = (?)",
            (question_id,)
        )
        self.__connection.commit()
        self.__connection.close()

    def get_answers_by_id(self, question_id) -> list[list]:
        self.__cursor.execute(
            "SELECT answer_id, answer FROM answers where question_id = (?)",
            (question_id,)
        )
        answers = self.__cursor.fetchall()
        self.__connection.commit()
        self.__connection.close()
        return answers

    def update_answer(self, new_answer: str, answer_id: int) -> None:
        self.__cursor.execute(
            "UPDATE answers SET answer = (?) WHERE answer_id = (?)",
            (new_answer, answer_id)
        )
        self.__connection.commit()
        self.__connection.close()

    def get_connect_data(self) -> list[list]:
        self.__cursor.execute("SELECT * FROM applications")
        connect_data = self.__cursor.fetchall()
        self.__connection.commit()
        self.__connection.close()
        return connect_data

    def get_feedback_data(self) -> list[list]:
        self.__cursor.execute("SELECT * FROM feedback")
        feedback_data = self.__cursor.fetchall()
        self.__connection.commit()
        self.__connection.close()
        return feedback_data
