########################################
### MIT Course 6 MEng GPA Calculator ###
### Author: Matt Beveridge           ###
########################################

class GPA:
    def __init__(self, semesters):
        self.semesters = semesters
        self.total_units = sum(semester.total_units for semester in semesters)
        self.technical_units = sum(semester.technical_units for semester in semesters)

    def calculate_overall_gpa(self):
        gpa = 0
        for semester in self.semesters:
            gpa += semester.calculate_gpa() * (semester.total_units / self.total_units)
        return gpa

    def calculate_technical_gpa(self):
        gpa = 0
        for semester in self.semesters:
            gpa += semester.calculate_technical_gpa() * (semester.technical_units / self.technical_units)
        return gpa

    def calculate_last_three_technical_gpa(self):
        last_three = sorted(self.semesters, key = lambda x: x.name, reverse=True)[:3]
        last_three_units = sum([s.technical_units for s in last_three])
        gpa = 0
        for semester in last_three:
            gpa += semester.calculate_technical_gpa() * (semester.technical_units / last_three_units)
        return gpa if last_three_units >= 60 else "N/A -> less than 60 technical units"

    def calculate_minus_worst_technical_gpa(self):
        best_to_worst = sorted(self.semesters, key = lambda x: x.calculate_technical_gpa(), reverse=True)
        worst = best_to_worst[-1]
        if worst.calculate_technical_gpa() < 4.0:
            best = best_to_worst[:-1]
            best_units = sum([s.technical_units for s in best])
            gpa = 0
            for semester in best:
                gpa += semester.calculate_technical_gpa() * (semester.technical_units / best_units)
            return gpa
        return "N/A -> No term GPA less than 4.0"


class Semester:
    def __init__(self, name, courses):
        """

        :param name: (int) the name of the semester starting with freshman fall = 0
        :param courses: (dictionary) specifying courses and their respective (tuple) units and grades
        """
        self.name = name
        self.courses = {}
        for course in courses:
            self.add_course(course, courses[course])
        self.total_units = sum([course.units for course in self.courses.values()])
        self.technical_units = sum([course.units for course in self.courses.values() if course.technical])

    def add_course(self, course, info):
        grade, units = info
        self.courses[course] = Course(course, grade, units)

    def calculate_gpa(self):
        gpa = 0
        for course in self.courses.values():
            gpa += course.grade * (course.units / self.total_units)
        return gpa

    def calculate_technical_gpa(self):
        gpa = 0
        for course in self.courses.values():
            if not course.technical:
                continue
            gpa += course.grade * (course.units / self.technical_units)
        return gpa


class Course:
    letter_to_number = {
        "A": 5,
        "B": 4,
        "C": 3,
        "D": 2,
        "F": 1
    }
    def __init__(self, name, grade, units):
        self.name = name
        self.grade = Course.letter_to_number[grade]
        self.units = units
        self.petitioned_classes = {"15.075"} # Any classes petitioned for technical units here
        self.technical = True if name.split(".")[0] in {"6", "8", "18"} or name in self.petitioned_classes else False


if __name__ == "__main__":
    # Example Semester Entry:
    # semester_name = {"class":("letter_grade", number_of_units)}
    # Like below:
    s_20 = {
        "18.204" : ("A", 12),
        "6.013" : ("B", 12),
        "18.335" : ("C", 12),
        "21M.606" : ("D", 12)
    }


    # Add semesters that you want considered into the semesters_input list in order from first semester
    # to most recest semester (left -> right)
    semesters_input = [s_20]
    semesters = []
    for i in range(len(semesters_input)):
        semesters.append(Semester(i, semesters_input[i]))
    gpa = GPA(semesters)
    print("overall gpa:", gpa.calculate_overall_gpa())
    print("overall technical gpa:", gpa.calculate_technical_gpa())
    print("last 3 technical gpa:", gpa.calculate_last_three_technical_gpa())
    print("minus worst technical gpa:", gpa.calculate_minus_worst_technical_gpa())


