from django.db.transaction import commit
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
import datetime
from .models import Room,Reservation,Guest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from .utils import render_to_pdf
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def start(request):
    return render(request, 'guest/start.html')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        # error1, error2 = False, False
        print(form.is_valid())
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            Guest.objects.create(user=new_user)
            cd = form.cleaned_data
            print(str(cd))
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password1'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('guest:home')
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
        return render(request, 'guest/reg_form.html', args)


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
                if user.is_active:
                    login(request, user)
                    return redirect('guest:home')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
        return render(request, 'guest/login.html', {'form': form})

@login_required
def home(request):
    print(request.method)
    if request.method == "POST":
        form = DateForm(request.POST)
        # response = HttpResponse()  # Created a HttpResponse
        # response['Cache-Control'] = 'no-cache'  # Set Cache-Control Header
        if form.is_valid():
            start_date = form.cleaned_data['checkIn']

            end_date = form.cleaned_data['checkOut']
            print(start_date, end_date)
            delta = end_date - start_date
            if delta.days > 0 and (start_date-datetime.date.today()).days >= 0:
                cnt = 0
                x = Room.objects.none()
                print(Room.objects.all())
                for room in Room.objects.all():
                    RoomsBooked = Reservation.objects.filter(room=room,room_alloted=True,accept=True).\
                        filter(checkIn__lte=end_date,checkOut__gte=start_date)
                    print(RoomsBooked)
                    count = RoomsBooked.count()
                    count = int(count)
                    if count == 0:
                        cnt += 1
                        x = x | Room.objects.filter(pk = room.pk)
                print(cnt)
                print(x)
                res = form.save(commit=False)
                if cnt > 0:

                    res.save()
                    request.session['booking_id'] = res.booking_id
                    # form.save(form.save(commit=False))
                    # form = SelectionForm(instance=request.reservation)
                    # form.fields["room"].queryset = x
                    args = {'rooms': x, 'count': cnt, 'res': res}
                    return render(request, 'guest/details.html', args)
                else:
                    return HttpResponse("<h1> No Rooms </h1> <br> <br> <a href =  '' >"
                                        " Book Again! </a> ")
            else:

                return HttpResponse("<h1> Invalid request </h1> <br> <br> <a href = '' >"
                                        " Book Again! </a> ")
        else:
            form = DateForm()
            print(request.method)
            return render(request, 'guest/home.html', {'form': form})

    else:
        form = DateForm()
        print(request.method)
        return render(request, 'guest/home.html', {'form': form})

@login_required
def edit(request, res_id):
    if request.method == 'POST':


        try:
            form = RegistrationForm(request.POST,instance=request.user.guest)
        except Guest.DoesNotExist:
            form = RegistrationForm(request.POST)

        # form = RegistrationForm(request.POST,instance=request.user.guest)
        res = Reservation.objects.get(pk=res_id)
        if form.is_valid():
            if (not res.room_alloted) and (request.session['room']):

                room = Room.objects.get(no=request.session['room'])
                res.room = room
                del request.session['room']


                try:
                    res.guest = request.user.guest
                    res.save()
                    form.save(commit=True)
                except Guest.DoesNotExist:
                    guest = form.save(commit=False)
                    guest.user = request.user
                    guest.save()
                    res.guest = guest

                    res.save()

                # res.guest = request.user.guest
                # res.save()

                return render(request, 'guest/profile.html', {'res': res})

            else:
                return HttpResponse("<h1> Invalid Request </h1>")
        else:
            res.delete()
            return HttpResponse("<h1> Wrong Credentials </h1> <br> <br> <a href = {% url '../../home' %} >"
                                " Book Again! </a> ")

    else:

        try:
            form = RegistrationForm(instance=request.user.guest)
        except Guest.DoesNotExist:
            form = RegistrationForm(request.POST)

        # form = RegistrationForm(instance=request.user.guest)
        return render(request, 'guest/edit.html', {'form': form,'res':res_id})


@login_required
def select(request, res_id):

    if request.method == 'POST':
        form = SelectionForm(request.POST, instance=Reservation.objects.get(pk=res_id))
        if form.is_valid():
            res_now = form.save(commit=False)
            # res_now.save()
            request.session['room'] = res_now.room.no
            # kwargs = {"room": res_now.room}
            return redirect('guest:edit', res_id =res_id)
    else:
        print('res_id',res_id)
        res = Reservation.objects.get(pk=res_id)
        form = SelectionForm(instance=res)
        start_date = res.checkIn
        end_date = res.checkOut
        x = Room.objects.none()
        print(Room.objects.all())
        cnt = 0
        for room in Room.objects.all():
            RoomsBooked = Reservation.objects.filter(room=room,room_alloted=True,accept=True).\
                filter(checkIn__lte=end_date, checkOut__gte=start_date)
            print(RoomsBooked.values())
            count = RoomsBooked.count()
            count = int(count)
            if count == 0:
                cnt += 1
                x = x | Room.objects.filter(pk=room.pk)
        if res.room:
            x = x | Room.objects.filter(pk=res.room.pk)
            cnt = cnt +1
        print(cnt)
        print(x)
        form.fields["room"].queryset = x
        return render(request, 'guest/select.html', {'form': form,'res':res})


@login_required
def bookings(request):
    try:
        guest = request.user.guest
        print(guest.first_name)
    except ObjectDoesNotExist:
        guest = Guest.objects.none()

    if guest:
        all_bookings = Reservation.objects.none()
        all_bookings = all_bookings | Reservation.objects.filter(guest=guest,room_alloted = True,accept=True)
        all_bookings = all_bookings | Reservation.objects.filter(guest=guest, room_alloted=True, reject=True)
        all_bookings = all_bookings | Reservation.objects.filter(guest=guest, room_alloted=True, accept=False,reject=False)
        print(all_bookings.count)
        return render(request,'guest/bookings.html',{"bookings":all_bookings,"guest":guest})
    elif request.user:

        return render(request, 'guest/bookings.html',{"bookings":Reservation.objects.none(),"guest":guest})


@login_required
def confirm(request,res_id):
    res = Reservation.objects.get(pk=res_id)

    res.room_alloted = True
    res.save()
    return render(request,'guest/confirm.html',{"res_id":res_id} )


@login_required
def generate_pdf(request,res_id):
    booking = Reservation.objects.get(pk = res_id)
    data = {
        'res': booking
    }
    pdf = render_to_pdf('guest/invoice.html', data)
    if pdf is None:
        booking.guest.delete()
        booking.delete()
        return HttpResponse("<h1>Error While Loading!! <br> Try Again</h1>")
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def cancel(request,res_id):
    booking = Reservation.objects.get(pk=res_id)
    booking.delete()

    return HttpResponse('<h1> Booking Cancelled </h1> <br> <a href=\"../../home\"> Book Again! </a>')


def logout_view(request):
    logout(request)
    return redirect('/guest')
