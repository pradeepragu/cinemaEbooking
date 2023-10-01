from django.db import models
from django.contrib.auth.models import User, AbstractUser
from .managers import CustomUserManager
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timezone
from django.db.models.functions import Now
import uuid


# Create your models here.
class User(AbstractUser):
    phone = models.TextField(blank=True, null=True)
    is_promo = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    apartNumber = models.TextField(blank=True, null=True)
    # city = models.TextField(blank = True, null = True)
    state = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    zip = models.TextField(blank=True, null=True)
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Card(models.Model):
    cardHolderName = models.CharField(max_length=1000, blank=True, null=True)
    cardNum = models.CharField(max_length=1000, blank=True, null=True)
    expiryDate = models.TextField(blank=True, null=True)
    last_four = models.CharField(max_length=4, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Movie(models.Model):
    name = models.CharField(max_length=100, default='')
    category1 = models.CharField(max_length=25,
                                choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Animation', 'Animation'),
                                         ('Biography', 'Biography'), ('Comedy', 'Comedy'), ('Crime', 'Crime'),
                                         ('Documentary', 'Documentary'), ('Drama', 'Drama'), ('Family', 'Family'),
                                         ('Fantasy', 'Fantasy'), ('Filmnoir', 'Film-Noir'), ('Gameshow', 'Game-show'),
                                         ('History', 'History'), ('Horror', 'Horror'), ('Music', 'Music'),
                                         ('Musical', 'Musical'), ('Mystery', 'Mystery'), ('News', 'News'),
                                         ('Realitytv', 'Reality-TV'), ('Romance', 'Romance'), ('Scifi', 'Sci-Fi'),
                                         ('Sport', 'Sport'), ('Talkshow', 'Talk-Show'), ('Thriller', 'Thriller'),
                                         ('War', 'War'), ('Western', 'Western')])
    category2 = models.CharField(max_length=25, default='',
                                 choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Animation', 'Animation'),
                                          ('Biography', 'Biography'), ('Comedy', 'Comedy'), ('Crime', 'Crime'),
                                          ('Documentary', 'Documentary'), ('Drama', 'Drama'), ('Family', 'Family'),
                                          ('Fantasy', 'Fantasy'), ('Filmnoir', 'Film-Noir'), ('Gameshow', 'Game-show'),
                                          ('History', 'History'), ('Horror', 'Horror'), ('Music', 'Music'),
                                          ('Musical', 'Musical'), ('Mystery', 'Mystery'), ('News', 'News'),
                                          ('Realitytv', 'Reality-TV'), ('Romance', 'Romance'), ('Scifi', 'Sci-Fi'),
                                          ('Sport', 'Sport'), ('Talkshow', 'Talk-Show'), ('Thriller', 'Thriller'),
                                          ('War', 'War'), ('Western', 'Western')])
    category3 = models.CharField(max_length=25, default='',
                                 choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Animation', 'Animation'),
                                          ('Biography', 'Biography'), ('Comedy', 'Comedy'), ('Crime', 'Crime'),
                                          ('Documentary', 'Documentary'), ('Drama', 'Drama'), ('Family', 'Family'),
                                          ('Fantasy', 'Fantasy'), ('Filmnoir', 'Film-Noir'), ('Gameshow', 'Game-show'),
                                          ('History', 'History'), ('Horror', 'Horror'), ('Music', 'Music'),
                                          ('Musical', 'Musical'), ('Mystery', 'Mystery'), ('News', 'News'),
                                          ('Realitytv', 'Reality-TV'), ('Romance', 'Romance'), ('Scifi', 'Sci-Fi'),
                                          ('Sport', 'Sport'), ('Talkshow', 'Talk-Show'), ('Thriller', 'Thriller'),
                                          ('War', 'War'), ('Western', 'Western')])
    sypnopsis = models.TextField(max_length=1000, default='')
    review = models.URLField(max_length=200, default='')
    rating = models.CharField(max_length=100,
                              choices=[('G', 'G General Audiences'), ('PG', 'PG Parental Guidance Suggested'),
                                       ('PG-13', 'PG-13 Parents Strongly Cautioned'), ('R', 'R Restricted'),
                                       ('NC-17', 'NC-17 Adults Only')], default='')
    status = models.CharField(max_length=50, default='',
                              choices=[('Now Playing', 'Now Playing'), ('Coming Soon', 'Coming Soon')])
    director = models.CharField(max_length=100, default='')
    cast = models.CharField(max_length=400, default='')
    producer = models.CharField(max_length=100, default='')
    poster = models.URLField(max_length=300, default='')
    trailer = models.URLField(max_length=200, default='')
    releasedate = models.DateField(default=False, null=True, blank=True)
    archived = models.BooleanField(default=False, null=True, blank=True)
    year = models.CharField(max_length=5, default='')
    imdb = models.CharField(max_length=6, default='')

    def __str__(self):
        return self.name

class MovieTime(models.Model):
    showDateTime = models.DateField()
    def __str__(self):
        return str(self.showDateTime)
    
class ShowRoom(models.Model):
    theatre = models.CharField(max_length=50,unique=True)
    seatNum = models.IntegerField(default=50)
    def __str__(self):
        return self.theatre

class MovieShowTime(models.Model):
    showTimes = models.TimeField()
    def __str__(self):
        return str(self.showTimes)
        
class Scheduler(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(showDate__gte=Now())

class ScheduleMovie(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    showDate = models.DateField(db_index=True)
    MovieTime = models.TextField(max_length=10,choices=[('10:00AM','10:00AM'),('13:00PM','13:00PM'),('16:00PM','16:00PM'),('19:00PM','19:00PM'),('22:00PM','22:00PM')])
    theatre = models.ForeignKey(ShowRoom,on_delete=models.CASCADE)
    child_cost=models.FloatField(default=5.99)
    adult_cost=models.FloatField(default=9.99)
    senior_cost=models.FloatField(default=6.99)
    booked_seats=models.IntegerField(default=0, validators=[MaxValueValidator(50), MinValueValidator(0)])
    def remaining_seats(self):
        return self.showroom.seatNum - self.booked_seats #numSeats
    objects = Scheduler()
    class Meta:
        unique_together = ('theatre','showDate', 'MovieTime')
    def __str__(self):
        return self.movie.name


class Promotion(models.Model):
    discount = models.IntegerField()
    user_notified = models.BooleanField(default=False, editable=False)
    promo_code = models.CharField(max_length=10, unique=True)
    valid_from = models.DateField(default=datetime.now)
    valid_upto = models.DateField()
    def __str__(self):
        return self.promo_code
    def get_discount(self):
        return (1-(self.discount/100))

class Seat(models.Model):
    seat_available = models.CharField(default="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50",max_length=200)
    seat_selected = models.CharField(max_length=200,blank=True,null=True)
    seat_booked = models.CharField(max_length=200,blank=True,null=True)
    show = models.ForeignKey(ScheduleMovie, on_delete=models.CASCADE)

    def __str__(self):
        return f'%s on %s at %s' % (self.show.movie.name, self.show.showDate, self.show.MovieTime)



class Tickets(models.Model):
    isBooked=models.BooleanField(default=False) #changed from isBookingDone to isBooked
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(ScheduleMovie,on_delete=models.CASCADE)
    ticket_child=models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    ticket_adult=models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    ticket_senior=models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    time_created = models.DateTimeField(auto_now_add=True,auto_now=False)
    seat_data = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    status = models.TextField(default="Active", blank=True, null=True)
    referenceNumber = models.TextField(max_length=50,blank=True, null=True)
    def __str__(self):
        return str(self.id)
    
class Booking(models.Model):
    tickets = models.OneToOneField(Tickets,on_delete=models.CASCADE)
    total = models.FloatField()
    bookingID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    def __str__(self):
        return f'%s on %s at %s for %s' % (self.tickets.show.movie.name,self.tickets.show.showDate,self.tickets.show.MovieTime, self.tickets.user.email)

