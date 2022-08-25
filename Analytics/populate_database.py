import numpy as np
import pandas as pd
# from .models import Academics
import string
import random
from suggestions.models import Data
from profiles.models import School, Student, User
from profiles.models import Student, User, School as Student_school



def create_student_data_csv(school_id):
	columns = ['Roll_number', 'Name', 'Standard', 'Division','English', 'Hindi',
	   'Maths', 'Science', 'History', 'Geography', 'Percent',
	   'How interactive in class', 'Assignments on time', 'Attentive in class',
	   'Creativity', 'Participation in extra curricular', 'Confidence',
	   'Social relationships', 'Obedient','Year']
	data =[]
	print('RUNNN')
	for standards in range(1,11):
		for divisions in ["A","B","C","D"]:
			for roll_nos in range(1,3):
				row = []
				N = 7
				name = ''.join(random.choices(string.ascii_uppercase +
											 string.digits, k=N))
				row.extend([roll_nos,name, standards,divisions])
				mark_student = []
				for marks in range(6):
					mark_student.append(np.random.randint(0,100))
				row.extend(mark_student)
				row.append((sum(mark_student)*100)/600)
				extras =[]
				for marks in range(8):
					extras.append(np.random.randint(0,5))
				row.extend(extras)
				row.append("2022")
				data.append(row)
				username = str(name)+'@'+str(roll_nos)
				user_obj = User.objects.create(username=username, name=name)
				user_obj.set_password(f'Password_{username}')
				user_obj.save()
				student = Student()
				student.user = user_obj
				student.roll_number = roll_nos
				student.std = standards
				student.division = divisions
				student.school = Student_school.objects.get(user_id=school_id)
				student.save()
	df = pd.DataFrame(data, columns =columns)
	df.to_csv("student_data.csv",index=False)

def database_happiness_index_survey():
	columns = ['Standard','Level Of Courses (Difficulty)', 'A Clean Environment',
	   'Employing teachers with competency',
	   'Preventing Discrimination and Persuasion',
	   'Providing laboratory & workshop facilities', 'The school timetable',
	   'Performing group work', 'Mental health assessment of all students',
	   'Presenting more sporting & artistic classes',
	   'Being able to solve problems of the learner',
	   'Courses should have creative and colorful instructional materials and fun activities.',
	   'Focus on the individual',
	   'Involve with fundamental and critical aspects of learner , about manner of living',
	   'Course relevance',
	   'Issues of concern should be made a point of conversation within age appropriate classrooms and children made aware of existing realities.',
	   'Are these problems being solved by the School?',
	   'Any other factors , according to you , which contribute to happiness index']
	schools = School.objects.all()
	for sc in schools:
		students = Student.objects.filter(school = sc)
		for student in students:
			info = []
			for _ in range(len(columns)-1):
				info.append(np.random.randint(0, 5))
			data = Data(school=sc, student=student, levelc=info[0], env=info[1], teachersc=info[2], prevdisc=info[3],
						fecilities=info[4], timetable=info[5], grpwork=info[6], mentalhlth=info[7],
						sportart=info[8], solveprob=info[9], creativecourse=info[10], foconindv=info[11],
						mannlearn=info[12], courserele=info[13], issuesofconc=info[14],
						aresolved=info[15],
						others="Cleanliness is very important")
			data.save()





# create_student_data_csv()