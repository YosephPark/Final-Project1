from PyQt6.QtWidgets import *
from grade_gui import *

class Logic(QMainWindow, Ui_MainWindow):
    '''
    A class representing the control logic of student grade management application work
    '''
    def __init__(self) -> None:
        '''
        Constructor to create initial actions of student grade management application
        '''
        super().__init__()
        self.setupUi(self)

        self.button_save.clicked.connect(lambda : self.save())
        self.button_clear_all_data.clicked.connect(lambda : self.clear_all_data())

        self.student_data = []

        headers = ['No.', 'Name', 'English', 'Math', 'Science', 'Total', 'Average', 'Grade']
        self.student_table.setColumnCount(len(headers))
        self.student_table.setHorizontalHeaderLabels(headers)

    def save(self) -> None:
        '''
        The data input conditions for each student and the method to present their grades
        '''
        name = self.input_name.text()
        english = self.input_English.text()
        math = self.input_Math.text()
        science = self.input_Science.text()

        try:
            name = str(name)

            if not name.strip() or name.strip().isnumeric():
                raise ValueError("Error: Student Name has to be entered with text.")

            english = english.strip()
            math = math.strip()
            science = science.strip()

            if not english.isnumeric() or not math.isnumeric() or not science.isnumeric():
                raise ValueError("Error: Subject scores must be entered as numbers.")

            english = float(english)
            math = float(math)
            science = float(science)

            if english == 0 or math == 0 or science == 0:
                raise ValueError("Error: Subject scores must exceed 0 points.")

            if not (english <= 100) or not (math <= 100) or not (science <= 100):
                raise ValueError("Error: Student scores should not exceed 100 points. Please make the necessary corrections.")

            if name and english and math and science:
                student = {'Name': name, 'English': english, 'Math': math, 'Science': science}
                self.student_data.append(student)

                self.input_name.clear()
                self.input_English.clear()
                self.input_Math.clear()
                self.input_Science.clear()

        except ValueError as e:
            self.label_error_message.setText(str(e))
            return

        self.calculate_grades()
        self.student_table.setRowCount(len(self.student_data))
        self.student_table.setColumnCount(8)
        self.student_table.verticalHeader().setVisible(False)

        for row, student in enumerate(self.student_data):
            self.student_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.student_table.setItem(row, 1, QTableWidgetItem(student['Name']))
            self.student_table.setItem(row, 2, QTableWidgetItem(str(student['English'])))
            self.student_table.setItem(row, 3, QTableWidgetItem(str(student['Math'])))
            self.student_table.setItem(row, 4, QTableWidgetItem(str(student['Science'])))
            self.student_table.setItem(row, 5, QTableWidgetItem(str(student['Total'])))
            self.student_table.setItem(row, 6, QTableWidgetItem(f'{student["Average"]:.2f}'))
            self.student_table.setItem(row, 7, QTableWidgetItem(student['Grade']))



    def calculate_grades(self) -> None:
        '''
        Method to calculate each student's final grade
        '''
        for student in self.student_data:
            scores = [student['English'], student['Math'], student['Science']]
            student_total_score = sum(scores)
            student_average_score = student_total_score / len(scores)
            student['Total'] = student_total_score
            student['Average'] = student_average_score

            if student_average_score >= 90:
                student['Grade'] = 'A'
            elif student_average_score >= 80:
                student['Grade'] = 'B'
            elif student_average_score >= 70:
                student['Grade'] = 'C'
            elif student_average_score >= 60:
                student['Grade'] = 'D'
            else:
                student['Grade'] = 'F'
        self.student_data.sort(key=lambda x: x['Total'], reverse=True)

    def clear_all_data(self) -> None:
        '''
        Method to terminate the GUI application
        '''
        self.input_name.clear()
        self.input_English.clear()
        self.input_Math.clear()
        self.input_Science.clear()
        self.label_error_message.setText('')
        self.student_data.clear()
        self.student_table.setRowCount(0)