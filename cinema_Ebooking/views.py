import json
import os
from datetime import date

import pytz
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import auth
from .forms import UserRegistrationForm
from .models import *
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from .settings import EMAIL_HOST, EMAIL_HOST_USER
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

# Create your views here.

# def home(request):
#     return render(request, 'home.html')

# def adminpage(request):
#     return render(request, 'admin.html')

# def userprofile(request):
#     return render(request,'userprofile.html')

# def logout(request):
#     return render(request, logout.html)

def login_user(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        print(email)
        print(password)
        remember = request.POST.get('rememberme')

        # print(email)
        # print(password)

        mydata = User.objects.filter(email=email).values()
        print(mydata.exists())
        try:
            mydata1 = User.objects.get(email=email)  # get
        except:
            mydata1 = None
        print(type(mydata1))

        user = auth.authenticate(email=email, password=password)

        # print(user)

        if user is not None:
            if user.is_active:
                print('user active')
                auth.login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                if user.is_superuser:
                    return redirect("/admin")  # success
                else:
                    return redirect(index)
            # else:
            #     print('user inactive')
            #     messages.info(request,'Account Not verified', extra_tags='verify')

        else:
            print('user not in db')
            if mydata.exists():
                if mydata[0]['is_active'] == False:

                    messages.info(request, 'Account not verified', extra_tags='verify')
                    activateEmail(request, mydata1, email)  # email confirmation #resend
                    return redirect('accountNotVerified')
                else:
                    messages.info(request, 'invalid credentials', extra_tags='invalid')
                    return redirect('login')
            else:
                messages.info(request, 'account does not exist', extra_tags='exist')
                return redirect('login')

    else:
        return render(request, 'login.html')


def logout(request):
    request.session.flush()
    auth.logout(request)
    return redirect(index)


def registration(request):
    if request.method == 'POST':
        print('success')
        #########################################receiving user detail##############################################
        first_name = request.POST['first_name']  # name in html
        last_name = request.POST['last_name']
        phone = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        is_promo = request.POST.get('promotion', None)
        print(is_promo)
        ######################optional data#########################################
        addr = request.POST.get('address', None)
        aptn = request.POST.get('aptNumber', None)
        # city = request.POST.get('city', None)
        state = request.POST.get('state', None)
        country = request.POST.get('country', None)
        zip = request.POST.get('zip', None)

        cardHolderName = request.POST.get('cardHolderName', None)
        cardNum = request.POST.get('cardNum', None)
        print(cardNum)
        expiryDate = request.POST.get('expiryDate', None)
        last_four = cardNum[-4:]
        cardNum = request.POST.get('cardNum', None)
        print('Decryption')
        print(cardNum)
        print(last_four)
        print('Got Data')
        #############################################check if email is in use#####################################################
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email address is already in use', extra_tags='taken')
            return redirect('registration')
        # else:
        #     print('going to save')

        ####################################################save to db####################################################
        user = User.objects.create_user(password=password1, email=email, first_name=first_name, last_name=last_name)

        # print(type(user))
        if is_promo == "on":
            user.is_promo = True
        # if phone == '':
        #     user.phone = 0
        # else:
        #     user.phone = phone
        user.phone = phone
        user.address = addr
        user.apartNumber = aptn
        # user.city = city
        user.state = state
        user.country = country
        user.zip = zip
        # user.cardname = cname
        # user.ccnum = ccnum
        # user.valid = valid

        # if addr == '':
        #     addr = null
        # user.set_password(password1)
        print(user.is_active)
        user.is_active = False
        print(user.is_active)
        print(user.first_name)

        print('saving...')
        user.save()
        print('User created')
        print(user.first_name)
        print(cardNum)
        if cardNum == 0 : 
            card = Card.objects.create(cardHolderName=cardHolderName, expiryDate=expiryDate, user_id=user.id)
            card.cardHolderName = cardHolderName
            card.cardNum = encryption(cardNum)
            card.expiryDate = encryption(expiryDate)
            card.last_four = last_four
            print(cardNum)

            card.save()
        activateEmail(request, user, email)  # email confirmation
        return redirect('accountSuccess')  # success #register
    else:
        return render(request, 'registration.html');


def activateEmail(request, user, to_email):
    print(user.first_name + 'in activateEmail')
    fname = user.first_name
    print(fname + ' new var')
    mail_subject = 'Activate your user account.'
    message = render_to_string('activationmail.html', {
        'fname': fname,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.email)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    print(message)
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.info(request, f'Dear {fname}, please go to you email {to_email} inbox and click on \
            received activation link to confirm and complete the registration. Note: Check your spam folder.',
                      extra_tags='verify')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def index(request):
    # new_movies = EbookingMovie.objects.filter(status="coming_soon")
    # present_movies = EbookingMovie.objects.filter(status="airing")

    movies = Movie.objects.values()
    moviesPlaying = movies.filter(status='Now Playing', archived=False)
    moviesComingSoon = movies.filter(status='Coming Soon', archived=False)

    context = {
        'moviesNow': moviesPlaying,
        'moviesSoon': moviesComingSoon
    }
    return render(request, 'index.html', context)


def movie_description(request):
    print('movie_description')
    name = request.GET.get('cinema_button')
    name = request.GET.get('cinema_button')
    movies = Movie.objects.filter(name=name).values()

    context = {
        'movies': movies
    }
    # print(context)
    return render(request, 'movie_description.html', context)


def show_time(request):
    name = request.GET.get('movie_title')
    print(name)
    movies = Movie.objects.filter(name=name).values('id')
    movieId = movies[0].get('id')
    print('MovieId : ', movieId)
    showTimes = ScheduleMovie.objects.filter(movie_id=movieId).values()
    list = []
    print(showTimes)
    showDateSet = set()
    for s in showTimes.order_by('showDate'):
        showDateSet.add(s.get('showDate'))
        print(showDateSet)
    for s in showTimes.order_by('showDate'):
        if s.get('showDate') in showDateSet:
            thisdict = {}
            thisdict['theatreid'] = ShowRoom.objects.filter(id=s.get('theatre_id')).values('theatre')[0].get('theatre')
            thisdict['showDate'] = (s.get('showDate')).strftime("%m-%d-%Y")
            i = 1
            for show in showTimes.order_by('showDate'):
                if s.get('theatre_id') == show.get('theatre_id') and s.get('showDate') == show.get('showDate'):
                    showtime = 'show' + str(i)
                    i = i + 1
                    thisdict[showtime] = show.get('MovieTime')
                    thisdict["showid"] = show.get('id')
            showDateSet.remove(s.get('showDate'))
            list.append(thisdict)

    context = {
        'movies': list
    }
    print(context)
    # return showtime information as a JSON response
    return JsonResponse(context)


def ticketcount(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please log in to book a movie.')
        return render(request, 'login.html')

    showId = request.GET.get("show_id")
    # print(showId)
    show = ScheduleMovie.objects.filter(id=showId).first()
    print(show)
    # print(show.movie_id)
    movie = Movie.objects.filter(id=show.movie_id).first()
    # print(movie)
    showroom = ShowRoom.objects.filter(id=show.theatre_id).first()
    seats = Seat.objects.filter(show_id=showId).first()
    available_seats = []
    available_seats = seats.seat_available.split(',')
    seatremaining = len(available_seats)
    context = {
        'seatsremaining': seatremaining,
        'moviename': movie.name,
        'showId': showId,
        'poster': movie.poster,
        'showDate': show.showDate,
        'showTime': show.MovieTime,
        'theater': showroom.theatre,
        'adultticket': show.adult_cost,
        'seniorticket': show.senior_cost,
        'childticket': show.child_cost
    }
    print(context)
    return render(request, 'ticketcount.html', context)


def confirmPayment(request):
    User = get_user_model()
    print(request.method)
    print(request.user)
    if request.method == 'POST':
        print('Confirm Payment')
        cardIdBtn = request.POST.get("cardId")
        confirm_payment = request.POST.get("confirm_payment")
        referenceNumber = request.POST.get("referenceNumber")
        save_changes = request.POST.get("save_changes")
        print(referenceNumber)
        print(save_changes)
        if cardIdBtn is not None:

            print('I am here')
            print('Pay button ID')

            print(cardIdBtn)
            mydata = User.objects.filter(email=request.user).first()
            print(mydata.id)
            cardDetails = Card.objects.filter(user_id=mydata.id).values()
            print(cardDetails)
            card1 = Card.objects.filter(id=int(cardIdBtn)).values()
            selectedCard = card1.first()
            # selectedCard.cardNum = decryption(selectedCard.cardNum)
            # selectedCard.expiryDate = decryption(selectedCard.expiryDate)
            # selectedCard.last_four = decryption(selectedCard.last_four)
            selectedCard['cardNum'] = decryption(selectedCard['cardNum'])
            selectedCard['expiryDate'] = decryption(selectedCard['expiryDate'])
            selectedCard['last_four'] = decryption(selectedCard['last_four'])
            print(selectedCard)
            l = selectedCard['expiryDate'].split('/')
            month = l[0]
            year = l[1]
            for data in cardDetails:
                # modify values as needed
                data['cardNum'] = decryption(data['cardNum'])
                data['expiryDate'] = decryption(data['expiryDate'])
                data['last_four'] = decryption(data['last_four'])

            context = {
                'cards': cardDetails,
                'referenceNumber': referenceNumber,
                'selectedCard': selectedCard,
                'month': month,
                'year': year

            }
            return render(request, 'confirmPayment.html', context)
        if save_changes is not None:
            print(request.user)
            user = User.objects.get(email=request.user)
            print(user.id)
            updated = False
            if user is not None:
                card_count = 0
                cards = []
                containsRecord = False
                for key, value in request.POST.items():
                    if key.startswith('cardHolderName_'):
                        containsRecord = True
                        card_count = key.split("_")[1]
                        card = {}
                        card['cardHolderName'] = value
                        card['cardNum'] = encryption(request.POST.get(f'cardNum_{card_count}'))
                        card['expiryDate'] = encryption(request.POST.get(f'expiryDate_{card_count}'))
                        card['last_four'] = request.POST.get(f'cardNum_{card_count}')[-4:]
                        cards.append(card)
                        print("Adding")
                if containsRecord == True:
                    print("Deleting record now")
                    # retrieve the record to be deleted
                    card_to_delete = Card.objects.filter(user_id=request.user.id)
                    # delete the record
                    card_to_delete.delete()
                print(cards)
                for card in cards:
                    # save each card object to the database
                    obj, created = Card.objects.get_or_create(
                        user_id=user.id,
                        cardHolderName=card['cardHolderName'],
                        cardNum=card['cardNum'],
                        last_four=card['last_four'],
                        expiryDate=card['expiryDate']
                    )
                    if created:
                        updated = True
                        print('Record created')
                    else:
                        print('Record Skipped')

                mydata = Card.objects.filter(user_id=user.id).values()
                for data in mydata:
                    # modify values as needed
                    data['cardNum'] = decryption(data['cardNum'])
                    data['expiryDate'] = decryption(data['expiryDate'])
                    data['last_four'] = decryption(data['last_four'])
                    # data['cardHolderName'] = decryption(data['cardHolderName'])

                context = {
                    'cards': mydata,
                    'referenceNumber': referenceNumber,

                }
                if updated == True:
                    messages.info(request, 'Successfully updated the payment details for the user.')
                return render(request, 'confirmPayment.html', context)

        if confirm_payment is not None:
            referenceNumber = request.POST.get("referenceNumberPay")
            print('Confirm Payment Button')
            print(referenceNumber)
            ticket = Tickets.objects.filter(referenceNumber=referenceNumber).first()
            print(ticket.time_created)
            difference = datetime.now(pytz.utc) - ticket.time_created
            print(difference.total_seconds())
            if difference.total_seconds() > 600:
                print('session Expired')
                messages.info(request, 'Session has expired', extra_tags='fail')
                seatsOccupied = Seat.objects.filter(show_id=ticket.show_id).first()
                list_seat_available = []
                list_seat_selected = []
                list_seat_booked = []
                print('seats selected before')

                print(seatsOccupied.seat_selected)
                print(seatsOccupied.seat_booked)
                print('seats available before')
                print(seatsOccupied.seat_available)
                if str(seatsOccupied.seat_available) != 'None' and len(seatsOccupied.seat_available) > 0:
                    list_seat_available = seatsOccupied.seat_available.split(',')
                if str(seatsOccupied.seat_selected) != 'None' and len(seatsOccupied.seat_selected) > 0:
                    list_seat_selected = seatsOccupied.seat_selected.split(',')
                    list_seat_selected1 = seatsOccupied.seat_selected.split(',')

                for i in list_seat_selected1:
                    list_seat_available.append(i)
                    list_seat_selected.remove(i)
                list_string_selected = ''
                list_string_available = ''

                k = 0
                for i in list_seat_selected:
                    if k == 0:
                        list_string_selected = str(i)
                        k = 1
                    else:
                        list_string_selected = list_string_selected + ',' + str(i)
                k = 0
                for i in list_seat_available:
                    if k == 0:
                        list_string_available = str(i)
                        k = 1
                    else:
                        list_string_available = list_string_available + ',' + str(i)
                ticket.isBooked = False
                print('seats selected after')
                print(list_string_selected)
                print('seats available after')
                print(list_string_available)
                seatsOccupied.seat_available = list_string_available
                seatsOccupied.seat_selected = ''
                seatsOccupied.save()
                ticket.save()
                return redirect('index')

                # session expired
            else:
                print('session not Expired')
                seatsOccupied = Seat.objects.filter(show_id=ticket.show_id).first()
                currentUser = User.objects.get(email=request.user)
                list_seat_available = []
                list_seat_selected = []
                list_seat_booked = []
                print(seatsOccupied.seat_selected)
                print(seatsOccupied.seat_booked)
                print(seatsOccupied.seat_available)
                if str(seatsOccupied.seat_booked) != 'None' and len(seatsOccupied.seat_booked) > 0:
                    list_seat_booked = seatsOccupied.seat_booked.split(',')
                if str(seatsOccupied.seat_selected) != 'None' and len(seatsOccupied.seat_selected) > 0:
                    list_seat_selected = seatsOccupied.seat_selected.split(',')
                    list_seat_selected1 = seatsOccupied.seat_selected.split(',')

                for i in list_seat_selected1:
                    list_seat_booked.append(i)
                    list_seat_selected.remove(i)
                list_string_selected = ''
                list_string_booked = ''

                k = 0
                for i in list_seat_selected:
                    if k == 0:
                        list_string_selected = str(i)
                        k = 1
                    else:
                        list_string_selected = list_string_selected + ',' + str(i)
                k = 0
                for i in list_seat_booked:
                    if k == 0:
                        list_string_booked = str(i)
                        k = 1
                    else:
                        list_string_booked = list_string_booked + ',' + str(i)
                ticket.isBooked = True
                print(list_string_selected)
                print(list_string_booked)
                seatsOccupied.seat_booked = list_string_booked
                seatsOccupied.seat_selected = ''
                seatsOccupied.save()
                ticket.save()
                show = ScheduleMovie.objects.filter(id=ticket.show_id).first()
                movie = Movie.objects.filter(id=show.movie_id).first()
                showroom = ShowRoom.objects.filter(id=show.theatre_id).first()
                confirmEmailTicketBooking(currentUser, movie, show, showroom, ticket)
                print('Email sent')
                print(referenceNumber)
                print(request.method)
                messages.info(
                request,
                mark_safe(f'Dear {currentUser.first_name},<br><br>Thank you for choosing E-Cinema Booking System. Please go to your email {request.user} inbox and find the order details confirming your order shortly.<br><br>Note: Check your spam folder.<br><br>\
                                            Order Id : {ticket.referenceNumber}<br>Movie : {movie}<br>Theater : {showroom.theatre}<br>\
                                            Date : {show.showDate}<br>Time : {show.MovieTime}<br>Seats : {ticket.seat_data}<br>Amount Paid : {ticket.price}'),
                extra_tags='confirm'
)

                return render(request, 'bookingconfirmed.html')
    else:
        print('Confirm Payment')
        showId = request.GET.get("show_Id")
        referenceNumber = request.GET.get("referenceNumber")
        print(referenceNumber)
        print(showId)
        mydata = User.objects.filter(email=request.user).first()
        print(mydata.id)
        cardDetails = Card.objects.filter(user_id=mydata.id).values()
        print(cardDetails)
        for data in cardDetails:
            # modify values as needed
            data['cardNum'] = decryption(data['cardNum'])
            data['expiryDate'] = decryption(data['expiryDate'])
            data['last_four'] = decryption(data['last_four'])

        context = {
            'cards': cardDetails,
            'referenceNumber': referenceNumber

        }
        return render(request, 'confirmPayment.html', context)


def bookingConfirmed(request):
    if request.method == 'POST':
        return render(request, 'index.html');
    return render(request, 'bookingconfirmed.html')


def checkout(request):
    print(request.method)
    if request.method == 'POST':
        apply_promo_btn = request.POST.get("proceed_checkout")
        make_payment_btn = request.POST.get("make_payment")
        showId = request.POST.get("show_id")
        print(showId)
        movie = request.POST.get("movie")
        print(movie)
        movieDateTime = request.POST.get("show_time")
        theatre = request.POST.get("show_room")
        selectedseats = request.POST.get("seats")
        totalCount = request.POST.get("no_of_tickets")
        price = request.POST.get("tickets_price")
        tax = request.POST.get("taxes")
        adultCount = request.POST.get("adult")
        childCount = request.POST.get("child")
        seniorCount = request.POST.get("senior")
        totalPrice = request.POST.get("total_price")
        totalPaymentAmount = request.POST.get("amount")
        print('Actual Payment amount : ',totalPaymentAmount)
        promotion_code = request.POST.get("promotion_code")
        print(promotion_code)
        promotion = Promotion.objects.filter(promo_code=promotion_code).first()
        discount = 0.00
        dateToday = date.today()
        if apply_promo_btn is not None:
            if promotion is None:
                messages.info(request, 'Promo code is not valid', extra_tags='promocode')
                payment_amount = totalPrice
            else:
                if promotion.valid_from <= dateToday and dateToday <= promotion.valid_upto:
                    subtotal = float(price) - (float(price) * float(promotion.discount)) / 100
                    tax = (subtotal * 5) / 100
                    payment_amount = subtotal + tax
                    discount = (float(price) * float(promotion.discount)) / 100
                    discount = str("{0:.2f}".format(discount))
                    tax = str("{0:.2f}".format(tax))
                    payment_amount = str("{0:.2f}".format(payment_amount))
                    messages.info(request, f'Promo code is valid, you get {promotion.discount} % discount',
                                  extra_tags='promocode')
                else:
                    messages.info(request, 'Promo code is not valid', extra_tags='promocode')
                    payment_amount = totalPrice
            context = {
                'theater': theatre,
                'movieDateTime': movieDateTime,
                'movie': movie,
                'seats': selectedseats,
                'numSeats': totalCount,
                'price': price,
                'tax': tax,
                'totalPrice': totalPrice,
                'promotion_code': promotion_code,
                'discount': "- " + str(discount),
                'payment_amount': payment_amount,
                'showId': showId,
                'adult': adultCount,
                'child': childCount,
                'senior': seniorCount
            }
            return render(request, 'checkout.html', context)
        if make_payment_btn is not None:
            print('make payment')
            print("Final price for the ticket: ", totalPaymentAmount)
            ticket = Tickets()
            ticket.user = request.user
            ticket.isBooked = False
            ticket.ticket_adult = adultCount
            ticket.ticket_child = childCount
            ticket.ticket_senior = seniorCount
            ticket.seat_data = selectedseats
            ticket.show_id = showId
            ticket.time_created = datetime.now()
            ticket.price = totalPaymentAmount
            ticket.time_created = datetime.now(pytz.utc)
            timeCreated = ticket.time_created.strftime('%Y-%m-%d %H:%M:%S.%f')
            referenceNumber = 'tkt-' + "-".join(str(timeCreated).split(' '))
            ticket.referenceNumber = referenceNumber.replace('-', '').replace(':', '').replace('.', '')
            seatsOccupied = Seat.objects.filter(show_id=showId).first()
            list_seat_available = []
            list_seat_selected = []

            print('Before Split from DB')
            print(seatsOccupied.seat_available)
            print(seatsOccupied.seat_selected)
            if str(seatsOccupied.seat_available) != 'None' and len(seatsOccupied.seat_available) > 0:
                list_seat_available = seatsOccupied.seat_available.split(',')
            if str(seatsOccupied.seat_selected) != 'None' and len(seatsOccupied.seat_selected) > 0:
                list_seat_selected = seatsOccupied.seat_selected.split(',')
            print('After Split')
            print(list_seat_selected)
            print(list_seat_available)
            list_seat_selected1 = selectedseats.split(',')
            for i in list_seat_selected1:
                list_seat_selected.append(i)
                list_seat_available.remove(i)
            print('After adding into selected and deleting from available')
            print(list_seat_selected)
            print(list_seat_available)
            list_string_selected = ''
            list_string_available = ''

            k = 0
            for i in list_seat_selected:
                if k == 0:
                    list_string_selected = str(i)
                    print(str(k) + '------' + list_string_selected)
                    k = 1
                else:
                    list_string_selected = list_string_selected + ',' + str(i)
                    print(str(k) + '-------  ' + list_string_selected)

            k = 0
            for i in list_seat_available:
                if k == 0:
                    list_string_available = str(i)
                    print(str(k) + '------' + list_string_available)
                    k = 1
                else:
                    list_string_available = list_string_available + ',' + str(i)
                    print(str(k) + '------' + list_string_available)

            seatsOccupied.seat_available = list_string_available
            seatsOccupied.seat_selected = list_string_selected
            print(list_string_selected)
            print(list_string_available)
            print('selected seats saved')
            seatsOccupied.save()
            ticket.save()

            return redirect(f'/confirmPayment?show_Id={showId}&referenceNumber={ticket.referenceNumber}')
    else:
        print('Inside Checkout GET method')
        reference = request.GET.get("referenceNumber")
        print(reference)
        showId = request.GET.get("show_id")
        totalCount = int(request.GET.get("total"))
        adultCount = int(request.GET.get("adult", None))
        childCount = int(request.GET.get("child", None))
        seniorCount = int(request.GET.get("senior", None))
        selectedseats = request.GET.get("seatselected", None)
        show = ScheduleMovie.objects.filter(id=showId).first()
        movie = Movie.objects.filter(id=show.movie_id).first()
        showroom = ShowRoom.objects.filter(id=show.theatre_id).first()
        price = adultCount * show.adult_cost + childCount * show.child_cost + seniorCount * show.senior_cost
        tax = (price * 5) / 100
        totalPrice = price + tax
        totalPrice = str("{0:.2f}".format(totalPrice))
        tax = str("{0:.2f}".format(tax))
        price = str("{0:.2f}".format(price))
        theater = showroom.theatre
        movieDateTime = show.MovieTime + ' ' + str(show.showDate)

        # data['cardHolderName'] = decryption(data['cardHolderName'])

        context = {
            'showId': showId,
            'theater': theater,
            'movieDateTime': movieDateTime,
            'movie': movie,
            'seats': selectedseats,
            'numSeats': totalCount,
            'price': price,
            'tax': tax,
            'totalPrice': totalPrice,
            'discount': "0.00",
            'payment_amount': totalPrice,
            'adult': adultCount,
            'child': childCount,
            'senior': seniorCount
        }
        return render(request, 'checkout.html', context)


def seats(request):
    if request.method == 'POST':
        seats = json.loads(request.body)['seats']
        showId = json.loads(request.body)['showid']
        totalSeats = json.loads(request.body)['totalSeat']
        childCount = json.loads(request.body)['adultCount']
        adultCount = json.loads(request.body)['childCount']
        seniorCount = json.loads(request.body)['seniorCount']
        print(seats)
        print(showId)
        context = {

        }
        print('Entering Checkout')
        return render(request, 'checkout.html', context)
        # Rest of your 
    else:
        showId = request.GET.get("show_id")
        totalCount = request.GET.get("total")
        adultCount = request.GET.get("adult", None)
        childCount = request.GET.get("child", None)
        seniorCount = request.GET.get("senior", None)
        print(adultCount)
        show = ScheduleMovie.objects.filter(id=showId).first()
        print(show)
        # print(show.movie_id)
        movie = Movie.objects.filter(id=show.movie_id).first()
        # print(movie)
        showroom = ShowRoom.objects.filter(id=show.theatre_id).first()
        seats = Seat.objects.filter(show_id=showId).first()
        available_seats = []
        available_seats = seats.seat_available.split(',')
        # print(available_seats)
        seatdict = {}
        for i in range(1, 51):
            if str(i) in available_seats:
                seatdict[i] = 'A'
            else:
                seatdict[i] = 'O'
        # print(seatdict)
        context = {
            'moviename': movie.name,
            'showId': showId,
            'poster': movie.poster,
            'showDate': show.showDate,
            'showTime': show.MovieTime,
            'theater': showroom.theatre,
            'available_seats': seatdict,
            'min_seats': totalCount,
            'adult_count': adultCount,
            'senior_count': seniorCount,
            'child_count': childCount,
        }
        print(context)
        return render(request, 'seats.html', context)


def base(request):
    results = []

    if request.method == 'GET':
        movie_category = request.GET.get('movie_category', None)
        movie_name = request.GET.get('movie_name', None)
        count = 0
        print(movie_category)
        print(movie_name)
        if movie_name == '' and movie_category == 'ALL':
            results = Movie.objects.filter(archived=False)
            count = Movie.objects.filter(archived=False).count()
        elif movie_name != '' and movie_category != '':
            results = Movie.objects.filter(Q(name__icontains=movie_name) | Q(category1__icontains=movie_category) | Q(
                category2__icontains=movie_category) | Q(category3__icontains=movie_category), archived=False)
            count = Movie.objects.filter(Q(name__icontains=movie_name) | Q(category1__icontains=movie_category) | Q(
                category2__icontains=movie_category) | Q(category3__icontains=movie_category), archived=False).count()
        elif movie_name != '':
            results = Movie.objects.filter(name=movie_name, archived=False)
            count = Movie.objects.filter(name=movie_name, archived=False).count()
        elif movie_category != '':
            results = Movie.objects.filter(
                Q(category1__icontains=movie_category) | Q(category2__icontains=movie_category) | Q(
                    category3__icontains=movie_category))
            count = Movie.objects.filter(
                Q(category1__icontains=movie_category) | Q(category2__icontains=movie_category) | Q(
                    category3__icontains=movie_category)).count()
        else:
            results = Movie.objects.filter(archived=False)
            count = Movie.objects.filter(archived=False).count()
    if len(results) == 0:
        messages.error(request, 'No movie exists for given title or category', extra_tags='exist')
        results = Movie.objects.all()
        moviesPlaying = results.filter(status='Now Playing',archived = False)
        moviesComingSoon = results.filter(status='Coming Soon',archived = False)
        context = {
             'moviesNow': moviesPlaying,
             'moviesSoon': moviesComingSoon
        }
        return render(request, 'index.html', context)
    moviesPlaying = results.filter(status='Now Playing')
    moviesComingSoon = results.filter(status='Coming Soon')

    context = {
         'moviesNow': moviesPlaying,
         'moviesSoon': moviesComingSoon
     }
    return render(request, 'index.html', context)


def regisconfirmation(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(email=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        print('verified')

        messages.info(request, 'Thank you for your email confirmation. Now you can login your account.',
                      extra_tags='activated')
        return redirect('accountVerify')  # login page
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('index')  # homepage


def forgot_password_view(request):
    return render(request, "forgot_password.html")


def account_success(request):
    return render(request, "accountSuccess.html")


def account_verify(request):
    return render(request, "accountVerify.html")


def forgot_password_validation(request):
    return render(request, "new_password.html")


def account_notverified(request):
    return render(request, "accountNotVerified.html")


def edit_profile(request):
    User = get_user_model()
    if request.method == 'GET':
        mydata = User.objects.filter(email=request.user).values()
        print(mydata)
        template = loader.get_template('edit_profile.html')
        context = {
            'profileable': mydata
        }
        return HttpResponse(template.render(context, request))
    else:
        email1 = request.POST.get("email")
        print(email1)
        try:
            user = User.objects.get(email=request.user)
            print(user.email)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.phone = request.POST['phone_number']
            user.address = request.POST['streetAddressBilling']
            print(user.address)
            # user.first_name = request.POST.get("aptNumberBilling")

            user.state = request.POST['stateBilling']
            user.zip = request.POST['zipCodeBilling']
            user.apartNumber = request.POST['aptNumberBilling']
            user.country = request.POST['country']
            if request.POST.get('promotion') == 'on':
                user.is_promo = True
            else:
                user.is_promo = False
            print(user.is_promo)
            user.save()
            print('profile updated successfully')
            confirmEmailProfileUpdation(user)
            messages.info(request, 'Your profile has  been updated!!!', extra_tags='success')
            return redirect('/edit_profile')


def edit_password(request):
    if request.method == 'POST':
        currentPassword = request.POST.get("current_password")
        newPassword = request.POST.get("new_password")
        confirmPassword = request.POST.get("confirm_password")
        user = auth.authenticate(email=request.user, password=currentPassword)
        if user is not None:
            if newPassword == confirmPassword:
                currentUser = User.objects.get(email=request.user)
                currentUser.set_password(newPassword)
                currentUser.save()
                messages.info(request, 'Successfully changed password', extra_tags='success')
                print('Updated')
                confirmEmailPasswordUpdation(currentUser)
                # conf_Email(request, currentUser, request.user)
                return redirect('/login')
            else:
                messages.info(request, 'Password not matching', extra_tags='match')
                print('Password not matching')
                return render(request, 'new_password.html')
        else:
            if currentPassword is not None:
                messages.info(request, 'Failed to Authenticate, current password is incorrect', extra_tags='fail')
                print("Failed to Authenticate, reset through email link")
            return render(request, 'new_password.html')
    else:
        return render(request, "new_password.html")


def edit_card(request):
    if request.method == 'POST':
        print(request.user)
        user = User.objects.get(email=request.user)
        print(user.id)
        updated = False
        if user is not None:
            card_count = 0
            cards = []
            containsRecord = False
            for key, value in request.POST.items():
                if key.startswith('cardHolderName_'):
                    containsRecord = True
                    card_count = key.split("_")[1]
                    card = {}
                    card['cardHolderName'] = value
                    card['cardNum'] = encryption(request.POST.get(f'cardNum_{card_count}'))
                    card['expiryDate'] = encryption(request.POST.get(f'expiryDate_{card_count}'))
                    card['last_four'] = request.POST.get(f'cardNum_{card_count}')[-4:]
                    cards.append(card)
                    print("Adding")
            if containsRecord == True:
                print("Deleting record now")
                # retrieve the record to be deleted
                card_to_delete = Card.objects.filter(user_id=request.user.id)
                # delete the record
                card_to_delete.delete()
            print(cards)
            for card in cards:
                # save each card object to the database
                obj, created = Card.objects.get_or_create(
                    user_id=user.id,
                    cardHolderName=card['cardHolderName'],
                    cardNum=card['cardNum'],
                    last_four=card['last_four'],
                    expiryDate=card['expiryDate']
                )
                if created:
                    updated = True
                    print('Record created')
                else:
                    print('Record Skipped')

            mydata = Card.objects.filter(user_id=user.id).values()
            for data in mydata:
                # modify values as needed
                data['cardNum'] = decryption(data['cardNum'])
                data['expiryDate'] = decryption(data['expiryDate'])
                data['last_four'] = decryption(data['last_four'])
                # data['cardHolderName'] = decryption(data['cardHolderName'])

            template = loader.get_template('edit_card.html')
            context = {
                'cards': mydata
            }
            if updated == True:
                messages.info(request, 'Successfully updated the payment details for the user.')
            return HttpResponse(template.render(context, request))

    print(request.user)
    user = User.objects.get(email=request.user)
    print(user.id)
    mydata = Card.objects.filter(user_id=user.id).values()
    template = loader.get_template('edit_card.html')
    context = {
        'cards': mydata
    }

    return HttpResponse(template.render(context, request))


def orderconfirmation(request, order):
    return render(request, "orderConfirmation.html")


def book_movie(request):
    return render(request, 'bookmovie.html')


def summary(request):
    return render(request, 'summary.html')


def password_reset_confirmation(request):
    return render(request, 'passwordresetconfirm.html')


def pwd_reset(request):
    if request.method == 'POST':
        email = request.POST['email']
        mydata = User.objects.filter(email=email).values()

        # print(mydata)
        if mydata.exists():
            mydata1 = User.objects.get(email=email)
            resetPwdEmail(request, mydata1, email)  # reset function call
            # messages.info(request,'Password Reset link has been sent to your Email Id. Please click on \
            # received reset link to reset your password. Note: Check your spam folder.',extra_tags='exist')
            return render(request, "forgot_password.html")
        else:
            messages.info(request,
                          'No account exists for provided Email Id. Please check it once and try sending the link again',
                          extra_tags='exist')
            return render(request, "forgot_password.html")


    else:
        return render(request, "forgot_password.html")


def resetPwdEmail(request, user, to_email):
    # print(user.first_name + 'in resetEmail')
    firstname = user.first_name
    # print(fname + ' new var')
    mail_subject = 'Cinema EBooking Password Reset Link'
    message = render_to_string('pwdresetmail.html', {
        'firstname': firstname,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    print(message)
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.info(request, f'Dear {firstname}, a password reset link is sent to your {to_email} inbox. Please click on \
            received reset link to reset your password. Note: Check your spam folder.')
    else:
        messages.error(request, f'Some issue with sending mail to {to_email}, check if you typed it correctly.')


def forgot_password_validation(request, uidb64, token):
    if request.method == 'POST':

        #currentpassword = request.POST['current_password']
        newpassword1 = request.POST['new_password']
        newpassword2 = request.POST['new_password2']
        if newpassword1 == newpassword2:
            User = get_user_model()
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and account_activation_token.check_token(user, token):
                user.set_password(newpassword1)
                print(user.password)
                user.save()
                messages.info(request, "Password is reset successfully. Please login with the new password.")
                return render(request, 'passwordresetconfirm.html')  # success page

            else:
                messages.info(request,
                              'Reset link is invalid! Please check the link or resend a new link to you email.')
                return render(request, 'passwordresetconfirm.html')  # success page

        else:
            messages.info(request, 'Passwords do not match, please try again with the link sent to email',
                          extra_tags='match')
            return render(request, 'passwordresetconfirm.html')

    else:
        return render(request, "passwordreset.html")


def reset_password(request):
    return render(request, 'passwordreset.html')


def confirmEmailProfileUpdation(user):
    try:
        send_mail(
            subject='Profile Updated!!!',
            message='Dear {name},\nYour Profile has been updated successfully'.format(name=user.first_name),
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email])
    except:
        pass


def confirmEmailPasswordUpdation(user):
    try:
        send_mail(
            subject='Password Changed!!!',
            message='Dear {name},\nYour password has been changed successfully'.format(name=user.first_name),
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email])
    except:
        pass


def confirmEmailTicketBooking(user, movie, show, showroom, ticket):
    try:
        send_mail(
            subject='Ticket Booked!!!',
            message='Dear {name},\nYour ticket has been booked successfully.\n' \
                    'Ticket Details\n' \
                    '___________________________________\n' \
                    'Movie      :   {movie}\n' \
                    'Theater      :   {theater}\n' \
                    'Show Date  :   {showDate}\n' \
                    'Show Time  :   {showTime}\n' \
                    'Adult          :   {adult}\n' \
                    'Child     :   {child}\n' \
                    'Senior     :   {senior}\n' \
                    'Seats      :   {seats}\n' \
                    '___________________________________\n' \
                    'Your Booking reference number is {reference}.'.format(name=user.first_name,
                                                                           movie=movie,
                                                                           theater=showroom.theatre,
                                                                           showDate=show.showDate,
                                                                           showTime=show.MovieTime,
                                                                           adult=ticket.ticket_adult,
                                                                           child=ticket.ticket_child,
                                                                           senior=ticket.ticket_senior,
                                                                           seats=ticket.seat_data,
                                                                           reference=ticket.referenceNumber),
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email])
    except Exception as error:
        print('Exception')
        print(error)
        pass


def notifyPromo(request, promo_id):
    allUsers = User.objects.filter(is_promo=True)
    promo = get_object_or_404(Promotion, pk=promo_id)
    promooff = promo.discount
    code = promo.promo_code
    validuntil = promo.valid_upto
    validfrom = promo.valid_from
    mail_subject = 'New promotion, Avail Now'
    for user in allUsers:
        first_name = user.first_name
        to_email = user.email
        message = render_to_string('promomail.html', {
            'firstname': first_name,
            'promooff': promooff,
            'code': code,
            'validfrom': validfrom,
            'validuntil': validuntil
        })
        email = EmailMessage(mail_subject, message, to=[to_email])
        if email.send():
            print(f' User : {to_email} notified successfully')


@login_required
def order_history(request):
    user = request.user
    user = User.objects.get(email=request.user)
    print(user.id)
    tickets = Tickets.objects.filter(user_id=user.id, isBooked=True)
    records = []
    for ticket in tickets:
        print(ticket.show_id)
        show = ScheduleMovie.objects.get(id=ticket.show_id)
        movie = Movie.objects.get(id=show.movie_id)
        theatre = ShowRoom.objects.get(id=show.theatre_id)
        print(show)
        print(theatre)
        timestamp_str = str(ticket.time_created)
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f%z")
        formatted_timestamp = timestamp.strftime("%m-%d-%y %H:%M")
        record = {
            "movie_name": movie.name,
            "theatre_name": theatre.theatre,
            "total_amount": ticket.price,
            "status": "Booked",
            "seats": ticket.seat_data,
            "BookingId": ticket.referenceNumber,
            "show_date": show.showDate,
            "show_time": show.MovieTime,
            "booking_date": formatted_timestamp
        }
        records.append(record)

    # print(tickets.show_id)
    context = {'records': records}
    print(context)
    return render(request, 'booking_history.html', context)


def encryption(message):
    encrypted = ""
    for char in message:
        if char.isalpha():
            encrypted += chr(ord('a') + (ord(char) - ord('a') + 13) % 26)  # replace characters with ROT13 shift
        elif char.isdigit():
            encrypted += str((int(char) + 5) % 10)  # replace integers with +5 modulus 10
        else:
            encrypted += char
    return encrypted


def decryption(encrypted):
    decrypted = ""
    for char in encrypted:
        if char.isalpha():
            decrypted += chr(ord('a') + (ord(char) - ord('a') - 13) % 26)  # reverse ROT13 shift for characters
        elif char.isdigit():
            decrypted += str((int(char) - 5) % 10)  # reverse +5 modulus 10 for integers
        else:
            decrypted += char
    return decrypted
