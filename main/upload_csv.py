import csv


def save_new_students_from_csv(file_path):
    # do try catch accordingly
    # open csv file, read lines
    with open(file_path, 'r') as fp:
        students = csv.reader(fp, delimiter=',')
        row = 0
        for student in students:
            if row == 0:
                headers = student
                row = row + 1
            else:
                # create a dictionary of student details
                new_student_details = {}
                for i in range(len(headers)):
                    new_student_details[headers[i]] = student[i]

                # for the foreign key field current_class in Student you should get the object first and reassign the value to the key
                # get the record according to value which is stored in db and csv file
                new_student_details['current_class'] = StudentClass.objects.get(
                )

                # create an instance of Student model
                new_student = Student()
                new_student.__dict__.update(new_student_details)
                new_student.save()
                row = row + 1
        fp.close()
