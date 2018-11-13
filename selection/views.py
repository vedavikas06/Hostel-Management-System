from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse, Http404
from selection.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


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
                    student = request.user.student
                    leaves = Leave.objects.filter(student=request.user.student)
                    return render(request, 'profile.html', {'student': student, 'leaves': leaves})
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
            if user is not None:
                if not user.is_warden:
                    return HttpResponse('Invalid Login')
                elif user.is_active:
                    login(request, user)
                    room_list = request.user.warden.hostel.room_set.all()
                    context = {'rooms': room_list}
                    return render(request, 'warden.html', context)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


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
        student_room_type = request.user.student.course.room_type
        hostel = Hostel.objects.filter(
            gender=student_gender, course=student_course)
        print(student_gender, student_course, student_room_type)
        print(hostel)
        x = Room.objects.none()
        if student_room_type == 'B':
            print(student_room_type)
            for i in range(len(hostel)):
                h_id = hostel[i].id
                a = Room.objects.filter(
                    hostel_id=h_id, room_type=['S','D'], vacant=True)

                x = x | a
        else:
            for i in range(len(hostel)):
                h_id = hostel[i].id
                a = Room.objects.filter(
                    hostel_id=h_id, room_type=student_room_type, vacant=True)
                print(a)
                x = x | a
        form.fields["room"].queryset = x
        print('x',x)
        return render(request, 'select_room.html', {'form': form})


@login_required
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


@login_required
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


@login_required
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


def logout_view(request):
    logout(request)
    return redirect('/')


def BH5_Floor1(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms': room_list}
    return render(request, 'BH5_Floor1.html', context=room_dict)


def BH5_Floor2(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'BH5_Floor2.html', context=room_dict)


def BH5_Floor3(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'BH5_Floor3.html', context=room_dict)


def BH5_Floor4(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'BH5_Floor4.html', context=room_dict)


def BH5_Floor5(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'BH5_Floor5.html',context=room_dict)


def BH5_Floor6(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'BH5_Floor6.html', context=room_dict)


def BH5_GroundFloor(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'BH5_GroundFloor.html', context=room_dict)


def hostel_detail_view(request, hostel_name):
    try:
        this_hostel = Hostel.objects.get(name=hostel_name)
    except Hostel.DoesNotExist:
        raise Http404("Invalid Hostel Name")
    context = {
        'hostel': this_hostel,
        'rooms': Room.objects.filter(
            hostel=this_hostel)}
    return render(request, 'hostels.html', context)


def user_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid() & request.user.student.room_allotted:
            leave_form = form.save(commit=False)
            student = request.user.student
            leave_form.student = student
            leave_form.save()
            leaves = Leave.objects.filter(student = request.user.student)
            return render(request, 'profile.html', {'student': student,'leaves': leaves})

        elif not request.user.student.room_allotted:
            return HttpResponse('<h3>First Select a Room </h3> <br> <br> <a href = \'select\'> SELECT A ROOM </a> ')

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
            leaves = Leave.objects.filter(student__in=stud).filter(accept=False,reject=False)
            return render(request, 'pending.html', {'leaves': leaves})
    else:
        return HttpResponse('Invalid Login')


def leave_confirm(request,lv_id):
    lv = Leave.objects.get(id = lv_id)
    lv.accept = True
    lv.save()
    return redirect('../../leave')


def leave_reject(request, lv_id):
    lv = Leave.objects.get(id=lv_id)
    lv.reject = True
    lv.save()
    return redirect('../../leave')