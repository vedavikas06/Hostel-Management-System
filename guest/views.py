from django.db.transaction import commit
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
import datetime
from .models import Room,Reservation,Guest

from django.template.loader import get_template
from .utils import render_to_pdf
# Create your views here.


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
                    RoomsBooked = Reservation.objects.filter(room=room).filter(checkIn__lte=end_date,
                                                                               checkOut__gte=start_date)
                    print(RoomsBooked)
                    count = RoomsBooked.count()
                    count = int(count)
                    if count == 0:
                        cnt += 1
                        x = x | Room.objects.filter(pk = room.pk)
                print(cnt)
                print(x)
                if cnt > 0:
                    res = form.save(commit = False)
                    res.save()

                    # form.save(form.save(commit=False))
                    # form = SelectionForm(instance=request.reservation)
                    # form.fields["room"].queryset = x
                    args = {'rooms': x, 'count': cnt, 'res': res}
                    return render(request, 'guest/details.html', args)
                else:
                    return HttpResponse('<h1> No Rooms </h1>')
            else:
                return HttpResponse('<h1> Invalid request </h1>')
        else:
            form = DateForm()
            print(request.method)
            return render(request, 'guest/home.html', {'form': form})

    else:
        form = DateForm()
        print(request.method)
        return render(request, 'guest/home.html', {'form': form})


def edit(request, res_id):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        res = Reservation.objects.get(pk=res_id)
        if form.is_valid():
            if res.room_alloted == False:
                new_guest = form.save(commit=True)

                room = Room.objects.get(no=request.session['room'])
                res.room = room

                res.room_alloted = True
                room = res.room
                res.guest = new_guest
                res.save()

                return render(request, 'guest/profile.html', {'res': res})

            else:
                return HttpResponse("<h1> Invalid Request </h1>")
        else:
            res.delete()
            return HttpResponse("<h1> Wrong Credentials </h1> <br> <br> <a href = {% url 'guest:home' %} >"
                                " Book Again! </a> ")

    else:
        form = RegistrationForm(instance=Reservation.objects.get(pk=res_id))
        return render(request, 'guest/edit.html', {'form': form})


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
        print(id)
        res = Reservation.objects.get(pk=res_id)
        form = SelectionForm(instance=res)
        start_date = res.checkIn
        end_date = res.checkOut
        x = Room.objects.none()
        print(Room.objects.all())
        cnt = 0
        for room in Room.objects.all():
            RoomsBooked = Reservation.objects.filter(room=room).filter(checkIn__lte=end_date,
                                                                       checkOut__gte=start_date)
            print(RoomsBooked.values())
            count = RoomsBooked.count()
            count = int(count)
            if count == 0:
                cnt += 1
                x = x | Room.objects.filter(pk=room.pk)
        print(cnt)
        print(x)
        form.fields["room"].queryset = x
        return render(request, 'guest/select.html', {'form': form})


def confirm(request,res_id):

    booking = Reservation.objects.get(pk = res_id)
    data = {
        'res': booking
    }
    pdf = render_to_pdf('guest/invoice.html', data)
    if pdf is None:
        booking.delete()
        return HttpResponse("<h1>Error While Loading!! <br> Try Again</h1>")
    return HttpResponse(pdf, content_type='application/pdf')


def cancel(request,res_id):
    booking = Reservation.objects.get(pk=res_id)
    booking.delete()

    return HttpResponse("<h1> Booking Cancelled </h1>")
