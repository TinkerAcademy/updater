import errno
import hashlib
import os
import re
import shutil
import syslog
import Tkinter as tk

BASE_LOCAL='/home/student/Documents/tinkeracademy/Setup'
BASE_REMOTE='/home/student/.Dropbox/Dropbox/'

KEY_STUDENT_ID='StudentId'
KEY_COURSE_ID='CourseId'
KEY_COURSE_NAME='CourseName'

KEY_NAME='Name'
KEY_ID='Id'

class TinkerAcademyMessage(tk.Tk):
	def __init__(self, message):
		self._message = message
		tk.Tk.__init__(self, None)
	def show(self):
		self._create_gui()
		self.mainloop()
	def _create_gui(self):
		self.title('Tinker Academy Message')
		self.grid()
		self._tf_message = tk.Label(self, text = self._message)
		self._tf_message.grid(column = 0, row = 0,sticky = 'EW')
		self._btn_ok = tk.Button(self, text = 'OK', command = self._ok_command)
		self._btn_ok.grid(column = 0, row = 1, columnspan = 2)
		self._btn_ok.focus_set()
		self.grid_columnconfigure(0, weight = 1)
		self.bind('<Return>', self._return_event)
		self.resizable(True, True)
		self.geometry('{}x{}+{}+{}'.format(400, 64, 400, 300))
	def _return_event(self, event):
		self._ok_command()
	def _ok_command(self):
		self.destroy()

def get_relative_file_paths_in_dir(dir_path):
	log_message('get_relative_file_paths_in_dir enter')
	relative_file_paths = []
	for root, dirs, files in os.walk(dir_path):
		rel_root = root.replace(dir_path, '')
		if rel_root and len(rel_root) > 0:
			if rel_root[0] == '/':
				rel_root = rel_root[1:]
			if rel_root:
				for file_ in files:
					relative_file_path = os.path.join(rel_root, file_)
					log_message('get_relative_file_paths_in_dir adding relative_file_path=' + str(relative_file_path))
					relative_file_paths.append(relative_file_path)
	log_message('get_relative_file_paths_in_dir exit')
	return relative_file_paths

def copy_files(source_file_paths, target_file_paths, clobber=False):
	log_message('copy_files enter')
	log_message('copy_files source_file_paths=' + str(source_file_paths))
	log_message('copy_files target_file_paths=' + str(target_file_paths))
	ret = 0
	n = len(source_file_paths)
	m = len(target_file_paths)
	if n == m:
		for i in range(0, n):
			source_file_path = source_file_paths[i]
			target_file_path = target_file_paths[i]
			source_files = []
			target_files = []
			if os.path.isdir(source_file_path):
				relative_file_paths = get_relative_file_paths_in_dir(source_file_path)
				for relative_file_path in relative_file_paths:
					source_file = os.path.join(source_file_path, relative_file_path)
					target_file = os.path.join(target_file_path, relative_file_path)
					source_files.append(source_file)
					target_files.append(target_file)
			elif os.path.isfile(source_file_path) and os.path.isfile(target_file_path):
				source_files.append(source_file_path)
				target_files.append(target_file_path)
			else:
				ret = -1
				break
			k = len(source_files)
			l = len(target_files)
			if k == l:
				for j in range(0, k):
					source_file = source_files[j]
					target_file = target_files[j]
					make_sure_path_exists(source_file)
					make_sure_path_exists(target_file)
					source_digest = calc_digest(source_file)
					target_digest = calc_digest(target_file)
					if target_digest is None or clobber:
						shutil.copyfile(source_file, target_file)
			else:
				ret = -1
				break
	else:
		ret = -1
	log_message('copy_files exit')
	return ret

def calc_digest(file_path):
	log_message('calc_digest enter')
	log_message('calc_digest file_path='+file_path)
	digest = None
	readable_file = os.path.exists(file_path) and os.path.isfile(file_path)
	if readable_file:
		content = read_content(file_path)
		if content:
			digest = hashlib.md5(content).hexdigest
			log_message('calc_digest digest='+str(digest))
	log_message('calc_digest exit')
	return digest

def get_course_paths(base_course_path, student_id):
	log_message('get_course_paths enter')
	log_message('get_course_paths student_id='+str(student_id))
	log_message('get_course_paths base_course_path='+str(base_course_path))
	course_paths = None
	if student_id:
		student_courses = list_student_courses(student_id)
		if student_courses:
			course_paths = []
			for student_course in student_courses:
				course_name = student_course[KEY_NAME]
				course_path = os.path.join(base_course_path, course_name)
				course_paths.append(course_path)
	log_message('get_course_paths exit')
	return course_paths

def make_sure_path_exists(path):
	try:
		dirname = os.path.dirname(path)
		os.makedirs(dirname)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise

def list_student_courses(student_id):
	log_message('list_student_courses enter')
	log_message('list_student_courses student_id='+str(student_id))
	student_courses = None
	courses = get_courses()
	if courses:
		student_profile = get_student_profile(student_id)
		if student_profile:
			student_courses = []
			for i in range(1, 5):
				course_id = student_profile[KEY_COURSE_ID + str(i)]
				if course_id and course_id != '0':
					course = courses[course_id]
					log_message('list_student_courses adding course='+str(course))
					course_name = course[KEY_COURSE_NAME]
					student_course = {}
					student_course[KEY_NAME] = course_name
					student_course[KEY_ID] = course_id
					student_courses.append(student_course)
	log_message('list_student_courses exit')
	return student_courses

def read_student_id():
	log_message('read_student_id enter')
	student_id = None
	config_file_path = os.path.join(BASE_LOCAL, 'tinkeracademy.config')
	log_message('read_student_id config_file_path=' + config_file_path)
	lines = read_lines(config_file_path)
	log_message('read_student_id lines=' + str(lines))
	count = len(lines)
	log_message('read_student_id line count=' + str(count))
	if lines and count > 0:
		prog = re.compile("\s*=\s*")
		for line in lines:
			if line:
				key, value = prog.split(line)
				if key and value:
					key = key.strip()
					value = value.strip()
					if key == KEY_STUDENT_ID:
						student_id = value
						break
	log_message('read_student_id exit')
	return student_id

def get_courses():
	log_message('get_courses enter')
	courses_file_path = os.path.join(BASE_REMOTE, 'classes/config/courses.csv')
	log_message('get_courses courses_file_path='+courses_file_path)
	courses = read_config(courses_file_path, KEY_COURSE_ID)
	log_message('get_courses exit')
	return courses

def get_student_profiles():
	log_message('get_student_profiles enter')
	csv_file_path = os.path.join(BASE_REMOTE, 'classes/config/students.csv')
	log_message('get_student_profiles csv_file_path='+csv_file_path)
	profiles = read_config(csv_file_path, KEY_STUDENT_ID)
	log_message('get_student_profiles exit')
	return profiles

def get_student_profile(student_id):
	log_message('get_student_profile enter')
	log_message('get_student_profile student_id=' + str(student_id))
	student_profile = None
	student_profiles = get_student_profiles()
	if student_id in student_profiles:
		student_profile = student_profiles[student_id]
	log_message('get_student_profile exit')
	return student_profile

def read_config(file_path, id_key):
	log_message('read_config enter')
	log_message('read_config file_path=' + file_path)
	log_message('read_config id_key=' + id_key)
	config = None
	lines = read_lines(file_path)
	if lines and len(lines) > 0:
		prog = re.compile("\s*,\s*")
		header = lines[0]
		keys = prog.split(header)
		if id_key in keys:
			entries = lines[1:]
			if entries:
				config = {}
				for entry in entries:
					values = prog.split(entry)
					id_value = None
					for i in range(0, len(keys)):
						key = keys[i]
						value = values[i]
						if key == id_key:
							id_value = values[i]
							break
					if id_value:
						config_entry = config[id_value] = {}
						for i in range(0, len(keys)):
							key = keys[i]
							value = values[i]
							config_entry[key] = value
	log_message('read_config exit')
	return config

def read_lines(file_path):
	log_message('read_lines enter')
	lines = None
	content = read_content(file_path)
	if content:
		lines = content.splitlines()
	log_message('read_lines exit')
	return lines

def read_content(file_path):
	log_message('read_content enter')
	log_message('read_content file_path='+str(file_path))
	content = None
	if os.path.isfile(file_path):
		file_handle = None
		try:
			file_handle = open(file_path, 'r')
			content = file_handle.read()
		except:
			log_error()
		finally:
			if file_handle:
				try:
					file_handle.close()
				except:
					log_error()
	log_message('read_content exit')
	return content

def log_message(message):
	syslog.syslog("tinkeracademy message=" + str(message))

def log_error():
	type_,value_,traceback_ = sys.exc_info()
	syslog.syslog('tinkeracademy error=' + value_.message)


