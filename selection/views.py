from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse, Http404
from selection.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime,calendar
from guest.models  import Room as Guest_Room,Reservation,Guest
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    return render(request, 'home.html')


def start(request):
    return render(request, 'start.html')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        # error1, error2 = False, False
        print(form.is_valid())
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            Student.objects.create(user=new_user)
            cd = form.cleaned_data
            print(str(cd))
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password1'])
            if user is not None:
                if user.is_active:

                    login(request, user)
                    return redirect('login/edit/')
                else:

                    return HttpResponse('Disabled account')
            else:

                return HttpResponse('Invalid Login')
        else:
            form = UserForm()
            args = {'form': form}
            return render(request, 'reg_form.html', args)
        # elif len(form.data['password1']) <= 8 or len(form.data['password2']) <= 8:
        #     if len(form.data['password1']) <= 8:
        #         error1 = True
        #     if len(form.data['password2']) <= 8:
        #         error2 = True
        #     return render(request, 'reg_form.html', {'form': form, 'error1': error1, 'error2': error2})

    else:

        form = UserForm()
        args = {'form': form}
        return render(request, 'reg_form.html', args)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'])
            if user is not None:
                if user.is_warden:
                    return HttpResponse('Invalid Login')
                if user.is_active:
                    login(request, user)
                    # student = request.user.student
                    # leaves = Leave.objects.filter(student=request.user.student)
                    # return render(request, 'profile.html', {'student': student, 'leaves': leaves})
                    return redirect('../student_profile/')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def warden_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'])
            print(cd['username'],cd['password'])
            print(user)
            if user is not None:
                if not user.is_warden:
                    return HttpResponse('Invalid Login')
                elif user.is_active:
                    login(request, user)
                    # print('True')
                    # room_list = request.user.warden.hostel.room_set.all()
                    # context = {'rooms': room_list}
                    # return render(request, 'warden.html', context)
                    return redirect('../warden_profile/')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def warden_profile(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        elif user.is_active:
            login(request, user)
            print('True')
            room_list = request.user.warden.hostel.room_set.all().order_by('no')
            context = {'rooms': room_list}
            return render(request, 'warden.html', context)
        else:
            return HttpResponse('Disabled account')
    else:
        return HttpResponse('Invalid Login')


def student_profile(request):
    user = request.user
    if user is not None:
        if user.is_warden:
            return HttpResponse('Invalid Login')
        if user.is_active:
            login(request, user)
            student = request.user.student
            leaves = Leave.objects.filter(student=request.user.student)
            return render(request, 'profile.html', {'student': student, 'leaves': leaves})
        else:
            return HttpResponse('Disabled account')
    else:
        return HttpResponse('Invalid Login')



@login_required
def edit(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=request.user.student)
        if form.is_valid():
            form.save()
            student = request.user.student
            leaves = Leave.objects.filter(student=request.user.student)
            return render(request, 'profile.html', {'student': student, 'leaves': leaves})
        else:
            form = RegistrationForm()
            return render(request, 'edit.html', {'form': form})
    else:
        form = RegistrationForm(instance=request.user.student)
        return render(request, 'edit.html', {'form': form})


@login_required
def select(request):

    if request.method == 'POST':
        if request.user.student.room:
            room_id_old = request.user.student.room_id

        if not request.user.student.no_dues:
            return HttpResponse('You have dues. Please contact your Hostel Caretaker or Warden')
        form = SelectionForm(request.POST, instance=request.user.student)
        if form.is_valid():
            if request.user.student.room_id:
                # stud = form.save(commit=False)
                # print(request.user.student.room_id, stud.room_id)
                request.user.student.room_allotted = True
                r_id_after = request.user.student.room_id
                room = Room.objects.get(id=r_id_after)
                room.vacant = False
                room.save()
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            else:
                request.user.student.room_allotted = False
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            student  = form.save()
            print(student.room_id)
            student = request.user.student
            leaves = Leave.objects.filter(student=request.user.student)
            return render(request, 'profile.html', {'student': student, 'leaves': leaves})
    else:
        if not request.user.student.no_dues:
            return HttpResponse('You have dues. Please contact your Hostel Caretaker or Warden')
        form = SelectionForm(instance=request.user.student)
        student_gender = request.user.student.gender
        student_course = request.user.student.course
        if student_course is None:
            return HttpResponse('No Course Selected <br> '
                                '<h3><a href = \'..\edit\' style = "text-align: center; color: Red ;"> Update Profile </a> </h3> ')
        student_room_type = request.user.student.course.room_type
        hostel = Hostel.objects.filter(
            gender=student_gender, course=student_course).order_by('name')
        print(student_gender, student_course, student_room_type)
        print(hostel)
        x = Room.objects.none()
        if student_room_type == 'B':
            # print(student_room_type)
            # for i in range(len(hostel)):
            #     h_id = hostel[i].id
            x = Room.objects.filter(
                hostel__id=hostel, room_type=['S','D'], vacant=True).order_by('no')

            # x = x | a
        else:
            # for i in range(len(hostel)):
            #     h_id = hostel[i].id
            x = Room.objects.filter(
                hostel_id__in=hostel, room_type=student_room_type, vacant=True).order_by('hostel_id','no')
            print(x)
            # x = x | a
        form.fields["room"].queryset = x
        print('x',x)
        return render(request, 'select_room.html', {'form': form})


def repair(request):

    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid() & request.user.student.room_allotted:

            rep = form.cleaned_data['repair']
            room = request.user.student.room
            room.repair = rep
            room.save()
            return HttpResponse('<h3>Complaint Registered</h3> <br> <a href = \'../../student_profile\''
                                ' style = "text-align: center; color: Red ;"> Go Back to Profile </a>')
        elif not request.user.student.room_allotted:
            return HttpResponse('<h3>First Select a Room </h3> <br> <a href = \'../select\''
                                ' style = "text-align: center; color: Red ;"> SELECT ROOM </a> ')

        else:
            form = RepairForm()
            room = request.user.student.room
            return render(request, 'repair_form.html', {'form': form, 'room': room})
    else:
        if not request.user.student.room_allotted:
            return HttpResponse('<h3>First Select a Room </h3> <br> <a href = \'../select\''
                                ' style = "text-align: center; color: Red ;"> SELECT ROOM </a> ')
        else:
            form = RepairForm()
            room = request.user.student.room
            return render(request, 'repair_form.html', {'form': form,'room': room})





# @login_required
def warden_dues(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            students = Student.objects.all()
            return render(request, 'dues.html', {'students': students})
    else:
        return HttpResponse('Invalid Login')


# @login_required
def warden_add_due(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            if request.method == "POST":
                form = DuesForm(request.POST)
                if form.is_valid():
                    student = form.cleaned_data.get('choice')
                    student.no_dues = False
                    student.save()
                    return HttpResponse('Done')
            else:
                form = DuesForm()
                return render(request, 'add_due.html', {'form': form})
    else:
        return HttpResponse('Invalid Login')


# @login_required
def warden_remove_due(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            if request.method == "POST":
                form = NoDuesForm(request.POST)
                if form.is_valid():
                    student = form.cleaned_data.get('choice')
                    student.no_dues = True
                    student.save()
                    return HttpResponse('Done')
            else:
                form = NoDuesForm()
                return render(request, 'remove_due.html', {'form': form})
    else:
        return HttpResponse('Invalid Login')


def empty_rooms(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        elif user.is_active:
            room_list = request.user.warden.hostel.room_set.filter(vacant=True).order_by('no')
            context = {'rooms': room_list}
            return render(request, 'empty_rooms.html', context)
        else:
            return HttpResponse('Disabled account')
    else:
        return HttpResponse('Invalid Login')


def guest_requests(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        elif user.is_active:
            guest_request = Reservation.objects.filter(room_alloted = True,accept=False,reject=False)
            accepted_requests = Reservation.objects.filter(room_alloted = True,accept=True).order_by('-booking_id')[:10]
            print('true')
            return render(request, 'guest_requests.html', {'requests': guest_request,'accepted':accepted_requests})
        else:
            return HttpResponse('Disabled account')
    else:
        return HttpResponse('Invalid Login')


def bookings(request,b_id):
    try:
        guest = Reservation.objects.get(booking_id = b_id).guest
        print(guest.first_name)
    except ObjectDoesNotExist:
        guest = Guest.objects.none()

    if guest:
        all_bookings = Reservation.objects.none()
        all_bookings = all_bookings | Reservation.objects.filter(guest=guest,room_alloted = True,accept=True)
        all_bookings = all_bookings | Reservation.objects.filter(guest=guest, room_alloted=True, reject=True)
        all_bookings = all_bookings | Reservation.objects.filter(guest=guest, room_alloted=True, accept=False,reject=False)
        print(all_bookings.count)
        return render(request,'bookings.html',{"bookings":all_bookings,"guest":guest})
    else:

        return render(request, 'bookings.html',{"bookings":Reservation.objects.none(),"guest":guest})


@login_required
def guest_accept(request,res_id):
    res = Reservation.objects.get(booking_id=res_id)

    if res.room_alloted is True:
        res.accept = True
    else:
        res.reject = True

    res.save()
    return redirect('../../guest_requests')


@login_required
def guest_reject(request, res_id):
    res = Reservation.objects.get(booking_id=res_id)

    if res.room_alloted is True:
        res.reject = True
        res.save()
    else:
        res.delete()

    return redirect('../../guest_requests')


def present_leaves(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        elif user.is_active:
            warden_hostel = user.warden.hostel
            stud = Student.objects.filter(room__hostel=warden_hostel)
            leaves = Leave.objects.filter(student__in=stud,accept=True,start_date__lte=datetime.date.today(), end_date__gte=datetime.date.today()).values_list('student', flat=True).distinct()
            stud = Student.objects.filter(id__in= leaves)
            # print(leaves.query)
            print(stud.query)
            # print(stud)
            return render(request, 'present_leaves.html', {'student': stud})
        else:
            return HttpResponse('Disabled account')
    else:
        return HttpResponse('Invalid Login')


def mess_rebate(request):
    if request.method == 'POST':
        user = request.user
        form = RebateForm(request.POST)
        if user is not None:
            if not user.is_warden:
                return HttpResponse('Invalid Login')
            elif user.is_active and form.is_valid():

                reb = form.cleaned_data['rebate']
                print(reb)
                warden_hostel = user.warden.hostel
                stud = Student.objects.filter(room__hostel=warden_hostel).order_by('enrollment_no')
                leaves = Leave.objects.filter(student__in=stud, accept=True).order_by('student__enrollment_no')
                stud_rebate_list = {}
                this_month = reb.month
                first_day = datetime.date(reb.year, this_month, 1)

                for stud_id in stud:
                    cnt = 0
                    for leave in leaves:
                        if leave.student.id == stud_id.id and (leave.start_date.month == this_month or leave.end_date.month == this_month)  :
                            if (reb-leave.end_date).days > 0:

                                dayz = abs(leave.end_date-first_day).days - abs(leave.start_date-first_day).days + 1
                            else:
                                dayz = abs(reb - first_day).days - abs(leave.start_date - first_day).days
                            #print(leave.start_date, first_day, abs(leave.start_date - first_day).days)
                            print(leave.end_date,first_day,stud_id.student_name,dayz)
                            cnt = cnt+dayz
                    stud_rebate_list[stud_id.enrollment_no] = cnt
                print(stud_rebate_list)
                month_name = calendar.month_name[this_month]
                #stud = Student.objects.filter(id__in=leaves)
                # this_month = datetime.datetime.now().month
                # HourEntries.objects.filter(date__month=this_month).aggregate(Sum("quantity"))
                return render(request, 'mess_rebate.html',
                              {'form': form, 'count_rebate': stud_rebate_list, 'student': stud})
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid Login')
    else:
        form = RebateForm()
        stud_rebate_list={}
        stud=Student.objects.none()

        return render(request, 'mess_rebate.html', {'form': form,'count_rebate': stud_rebate_list,'student': stud})


def user_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid() & request.user.student.room_allotted:

            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            delta = end- start
            if delta.days > 0 and (start - datetime.date.today()).days >= 0:
                user_contr = Leave.objects.filter(student = request.user.student,start_date__lte=end,end_date__gte=start)
                count = user_contr.count()
                count = int(count)
                if count == 0:
                    leave_form = form.save(commit=False)
                    student = request.user.student
                    leave_form.student = student
                    leave_form.save()
                    leaves = Leave.objects.filter(student = request.user.student)

                    return render(request, 'profile.html', {'student': student,'leaves': leaves})
                else:
                    return HttpResponse('<h3>Already have a Leave in this period Try another</h3>  <br> '
                                        '<a href = \'\' style = "text-align: center; color: Red ;"> Apply Leave </a> ')
            else:
                return HttpResponse('<h2> Invalid Date </h2> <br>  <a href = \'\' '
                                    'style = "text-align: center; color: Red ;"> Apply Leave </a> ')
        elif not request.user.student.room_allotted:
            return HttpResponse('<h3>First Select a Room </h3> <br> <a href = \'select\''
                                ' style = "text-align: center; color: Red ;"> SELECT ROOM </a> ')

        else:
            form = LeaveForm()
            return render(request, 'leave_form.html', {'form': form})
    else:
        form = LeaveForm()
        return render(request, 'leave_form.html', {'form': form})


def leave_admin(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            warden_hostel = user.warden.hostel
            stud = Student.objects.filter(room__hostel = warden_hostel)
            # print(stud.values_list('id', flat=True))
            leaves = Leave.objects.filter(student__in=stud).filter(accept=False,reject=False)
            today = datetime.datetime.now().date()
            yesterday = today - datetime.timedelta(15)
            print(today,yesterday)
            accepted_leaves = Leave.objects.filter(student__in=stud,accept=True,
                                                   start_date__lte =today,end_date__gte=yesterday).\
                order_by('-confirm_time')
            print(accepted_leaves)
            return render(request, 'pending.html', {'leaves': leaves,'accepted':accepted_leaves})
    else:
        return HttpResponse('Invalid Login')


def student_leaves(request,std_id):
    today = datetime.datetime.now().date()
    yesterday = today - datetime.timedelta(60)
    print(today, yesterday)
    stud = Student.objects.get(id = std_id)
    leaves = Leave.objects.filter(student__id=std_id,accept=True,
                                  start_date__lte=today, end_date__gte=yesterday).order_by('-start_date')
    return render(request, 'student_leave.html', {'leaves': leaves,'student':stud})


def leave_confirm(request,lv_id):
    lv = Leave.objects.get(id = lv_id)
    lv.confirm_time = datetime.datetime.now()
    lv.accept = True
    lv.save()
    return redirect('../../leave')


def leave_reject(request, lv_id):
    lv = Leave.objects.get(id=lv_id)
    lv.reject = True
    lv.save()
    return redirect('../../leave')


def logout_view(request):
    logout(request)
    return redirect('/')


def BH5_Floor1(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms': room_list}
    return render(request, 'BH5_Floor1.html', context=room_dict)


def BH5_Floor2(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms': room_list}
    return render(request, 'BH5_Floor2.html', context=room_dict)


def BH5_Floor3(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms': room_list}
    return render(request, 'BH5_Floor3.html', context=room_dict)


def BH5_Floor4(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms': room_list}
    return render(request, 'BH5_Floor4.html', context=room_dict)


def BH5_Floor5(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms': room_list}
    return render(request, 'BH5_Floor5.html', context=room_dict)


def BH5_Floor6(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms': room_list}
    return render(request, 'BH5_Floor6.html', context=room_dict)


def BH5_GroundFloor(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms': room_list}
    return render(request, 'BH5_GroundFloor.html', context=room_dict)


def hostels(request):
    hostels_all = Hostel.objects.order_by('name')
    return render(request, 'hostels_all.html', {'hostels':hostels_all})


def hostel_detail_view(request, hostel_name):
    try:
        this_hostel = Hostel.objects.get(name=hostel_name)
    except Hostel.DoesNotExist:
        raise Http404("Invalid Hostel Name")
    context = {
        'hostel': this_hostel,
        'rooms': Room.objects.filter(
            hostel=this_hostel).order_by('name')}
    return render(request, 'hostels.html', context)