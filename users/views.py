from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate  # , login
import os
from .models import StudentsData, LecturerData, LecturerAttendance, Faculty
import face_recognition
import cv2
import dlib
from tkinter import *
import pickle
import datetime
from imutils import paths
import time
import random
import string
from django.core.mail import send_mail
from django.conf import settings
import csv
from django.http import HttpResponse
import xlwt

video_capture = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()


def facedect(loc):
    s, img = video_capture.read()
    if s:

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media_root = os.path.join(base_dir, 'pages')

        loc = (str(media_root) + loc)
        face_1_image = face_recognition.load_image_file(loc)
        face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]

        #

        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        check = face_recognition.compare_faces(face_1_face_encoding, face_encodings)

        print(check)
        # if check[0]:
        # return redirect('home')
    elif not s:
        return redirect('addstudent')


def index(request):
    msg = 'Wrong Username & Password'
    try1 = ' Try Again: Login'
    msg1 = 'Face Does Not Match'
    check1 = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            # f_log = facedect(user.adminprofile.head_shot.url)
            if user is not None:
                return redirect('home')
            else:
                return render(request, "index.html", {"msg": msg, "try1": try1})
    else:

        MyLoginForm = LoginForm()
        return render(request, "index.html", {"MyLoginForm": MyLoginForm})
    return render(request, "index.html", {})


def create(reqeust):
    print(reqeust.POST)
    adminid = reqeust.GET['admin_id']
    name = reqeust.GET['name']
    surname = reqeust.GET['surname']
    country = reqeust.GET['country']
    address = reqeust.GET['address']
    email = reqeust.GET['email']
    phone = reqeust.GET['phone']
    picture = reqeust.GET['a_picture']
    student_details = StudentsData(reg_no=adminid, name=name, surname=surname, country=country,
                                   address=address, email=email, phone=phone,  picture=picture)
    student_details.save()

    return redirect('addadmin')


def lec_create(reqeust):
    print(reqeust.POST)

    l_id = reqeust.GET['l_id']
    name = reqeust.GET['l_name']
    surname = reqeust.GET['l_surname']
    email = reqeust.GET['l_email']
    phone = reqeust.GET['l_phone']
    country = reqeust.GET['l_country']
    address = reqeust.GET['l_address']
    faculty = reqeust.GET['l_faculty']
    picture = reqeust.GET['l_picture']
    lec_details = LecturerData(l_id=l_id, name=name, surname=surname, email=email, phone=phone, country=country,
                               address=address, faculty=faculty, picture=picture)
    lec_details.save()

    folderName = l_id  # creating the person or user folder
    folderPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dataset/" + folderName)
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    sampleNum = 0
    while (True):
        ret, img = video_capture.read()  # reading the camera input
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converting to GrayScale
        dets = detector(img, 1)
        for i, d in enumerate(dets):  # loop will run for each face detected
            sampleNum += 1
            cv2.imwrite(folderPath + "/User." + l_id + "." + str(sampleNum) + ".jpg",
                        img[d.top():d.bottom(), d.left():d.right()])  # Saving the faces
            cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (0, 255, 0), 2)  # Forming the rectangle
            cv2.waitKey(200)  # waiting time of 200 milisecond
        cv2.imshow('frame', img)  # showing the video input from camera on window
        cv2.waitKey(1)
        if sampleNum >= 10:  # will take 20 faces
            break

    video_capture.release()  # turning the webcam off
    cv2.destroyAllWindows()

    return redirect('teacher')


def caption(request):
    if request.method == "POST":

        # creating instance of TK
        root = Tk()

        root.configure(background="white")

        def function1():
            os.system("python ./users/recog.py --encodings encodings.pickle")

        # setting title for the window
        root.title("S.S.S")

        # creating first button
        Button(root, text="Initialise Camera ", font=("times new roman", 20), bg="#0D47A1", fg='white',
               command=function1()).grid(
            row=3, columnspan=2, sticky=W + E + N + S, padx=5, pady=5)

        root.mainloop()
        return redirect('dattendance')
    else:
        return redirect('home')


def recog(request):
    if request.method == "POST":

        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = base_dir + '/encodings.pickle'

        # list of names in dataset
        dataset_image = os.path.dirname(os.path.abspath(__file__))
        dir = dataset_image + '/dataset'
        files = os.listdir(dir)

        # load the known faces and embeddings
        print("[INFO] loading encodings...")
        da = open(image_dir, 'rb')
        data = pickle.load(da)
        # Get a reference to webcam #0 (the default one)
        print("[INFO] starting video stream...")

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        ts = [0, 0, False]

        # Load present date and time time variables
        now = datetime.datetime.now()
        today = datetime.date.today()
        duration = 120
        start_time = time.time()

        # eperiment code  inserting users into the database for a day to be
        # marked***********************************************
        for na in files:
            li = na + str(now)
            status_n = "Absent"
            day = "--:--:--"
            lec_a = LecturerAttendance(a_id=li, l_id=na, day=today, time_in=day, time_out=day,
                                       status=status_n)
            lec_a.save()

        # end of eperiment ********************************************

        sampleNum = 0

        while True:

            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            det = detector(frame, 1)

            pass
            tin = datetime.datetime.now()
            pass
            timein = tin.time()

            # Only process every other frame of video to save time
            if process_this_frame:

                # Find all the faces and face encodings in the current frame of video

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []

                for face_encoding in face_encodings:

                    # initial_recogtime = datetime.datetime.now()
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(data["encodings"], face_encoding)
                    name = "Unknown"

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:

                        first_match_index = matches.index(True)
                        name = data["names"][first_match_index]
                        matchedidxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}

                        # loop over the matched indexes and maintain a count for
                        # each recognized face face
                        for i in matchedidxs:
                            name = data["names"][i]
                            counts[name] = counts.get(name, 0) + 1

                            # determine the recognized face with the largest number
                            # of votes (note: in the event of an unlikely tie Python
                            # will select first entry in the dictionary)
                        name = max(counts, key=counts.get)

                        # eperiment code  marking attendance inserting record into the
                        # database *******************************************

                        a_id = name + str(now)
                        out1 = datetime.datetime.now()
                        to = out1.time()
                        sta = "Present"
                        lec_a = LecturerAttendance(a_id=a_id, l_id=name, day=today, time_in=timein,
                                                   time_out=to, status=sta)
                        lec_a.save()

                        # eperiment code end*****************************************

                    face_names.append(name)
                    print(" Stuff Name Identified", face_names, timein)

            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image

            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return redirect('dattendance')

            de = (time.time() - start_time)

            if de >= duration:  # will take 2min  to recog the faces
                cv2.destroyAllWindows()
                return redirect('dattendance')

        # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


def train(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dataset = BASE_DIR + '/dataset'

    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")
    info1 = "[INFO] quantifying faces..."
    imagePaths = list(paths.list_images(image_dataset))

    # initialize the list of known encodings and known names
    knownEncodings = []
    knownNames = []

    now = datetime.datetime.now()

    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i + 1,
                                                     len(imagePaths)), imagePath)
        name = imagePath.split(os.path.sep)[-2]

        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image

        # face detection model to use: either `hog` or `cnn`
        boxes = face_recognition.face_locations(rgb,
                                                model="hog")

        # compute the facial embedding for the facec
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # enco3dings
            knownEncodings.append(encoding)
            knownNames.append(name)

        # generating id for time for training
        def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))
        # saving time for training
        # train_time = Faculty(faculty_id=id_generator(), faculty_name=now)
        # train_time.save()

    # dump the facial encodings + names to disk
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    im = BASE_DIR + '/encodings.pickle'
    f = open(im, "wb")
    f.write(pickle.dumps(data))
    f.close()

    return render(request, 'training.html', {})


def email(request):
    reg_no = request.GET['email_data']
    rows = LecturerAttendance.objects.all().values_list('a_id', 'l_id', 'day', 'time_in', 'time_out', 'status')
    subject = 'Testings email'
    message = "Attendance Data"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [reg_no]
    send_mail(subject, message, email_from, recipient_list)

    return render(request, 'attendance_report.html')


def export_users_csv(request):
    now = datetime.datetime.now()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv+now.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'name', 'day', 'time_in', 'time_out', 'status'])

    users = LecturerAttendance.objects.all().values_list('a_id', 'l_id', 'day', 'time_in', 'time_out', 'status')
    for user in users:
        writer.writerow(user)

    return response


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sss_attendance_excel.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Today Attendance')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'name', 'day', 'time_in', 'time_out', 'status']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = LecturerAttendance.objects.all().values_list('a_id', 'l_id', 'day', 'time_in', 'time_out', 'status')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def graphs(request):
    now = datetime.datetime.now()
    today = datetime.date.today()
    dataset_image = os.path.dirname(os.path.abspath(__file__))
    dir = dataset_image + '/dataset'
    files = os.listdir(dir)
    for na in files:
        li = na + str(now)
    total_nu = LecturerAttendance.objects.all().count()
    return render(request, 'graphs.html', {'att_re': total_nu})


def timeframe(reqeust):
    print(reqeust.POST)
    adminid = reqeust.GET['time_f']

    time_f = Faculty.objects.get(faculty_name=120)
    time_f.value = adminid
    time_f.save()

    return redirect('dattendance')

