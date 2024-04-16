from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from . forms import RegisterForm, PostForm, Car_info_form, leave_review_form, ServiceRequestForm, upcoming_maintenance_form, SubscriptionForm, BusinessCreationForm, leave_review_form_front_page
from . models import Post, Car_Information, ServiceRequest, LeaveReview, MostRecentMaintenance, BussinessCreationModel, LeaveReviewFrontPage
from scheduler.models import Event




import stripe
stripe.api_key = "pk_test_51ObrIRJ9Hp1bA45SzY1bnC0qY0VrfwTxlewKudNtjlUuqUE8CqQMw53T0MjKQh87BBHWnRLV2iAsmrV8Q5Ij5S4h00YZOYyaiZ"


def home(request):
    reviews = LeaveReviewFrontPage.objects.all()

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            send_subscription_email(subscriber.email)
            return redirect('/success_newsletter')  # Redirect to a success page
    else:
        form = SubscriptionForm()

        context = {'form': form, 'data': reviews}

    return render(request, 'main/base.html', context)


def send_subscription_email(email):
    subject = 'Thank you for subscribing!'
    message = 'Thank you for subscribing to our newsletter.'
    from_email = 'serverform45@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def oil_change_service(request):
    return render(request, 'services-offered/oil-change.html', {})


def break_pads_service(request):
    return render(request, 'services-offered/breake-pads-repair.html', {})


def alterantor_repair_service(request):
    return render(request, 'services-offered/alternator-repair.html', {})


def check_engine_light_service(request):
    return render(request, 'services-offered/check-engine-light.html', {})


def diagnostics_service(request):
    return render(request, 'services-offered/diagnostics.html', {})


def electrical_repair_service(request):
    return render(request, 'services-offered/electrical-repair.html', {})


def how_it_works(request):
    return render(request, 'main/howitworks.html', {})


def about(request):
    return render(request, 'main/about.html', {})


def pricing(request):
    return render(request, 'main/pricing.html', {})




@login_required(login_url='/login')
def user_home(request):
    # Retrieve data for the logged-in user

    business_data = BussinessCreationModel.objects.all()
    upcoming_maintenance_data = MostRecentMaintenance.objects.filter(owner=request.user)
    car_data = Car_Information.objects.filter(owner=request.user)

    context = {
        'data': car_data,
        'data_2': upcoming_maintenance_data,
        'data_3': business_data
    }

    return render(request, 'main/user-home.html', context)



@login_required(login_url='/login')
def LeaveReviewIntroPage(request):
    

    if request.method == "POST":
        form = leave_review_form_front_page(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.client_username_id = request.user
            review.save()
            return redirect('/home')
        
    else:
        form = leave_review_form_front_page()

        context = {'form': form}

    return render(request, 'main/leave_review.html', context)





def sign_up(request):
    form = RegisterForm() 
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/car-info')
        else:
            # Check for common password error
            if 'password2' in form.errors:
                messages.error(request, "Passwords do not match. Please try again.")
            elif 'password1' in form.errors:
                messages.error(request, "Password is too common. Choose a stronger password.")
            elif 'username' in form.errors:
                messages.error(request, "Username is already taken. Please choose another one.")
            elif 'email' in form.errors:
                messages.error(request, "Email is already taken. Please choose another one.")
            else:
                print(form.errors)

    return render(request, 'registration/sign_up.html', {'form': form})





def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['key'] = user.id
            request.session.save()
            return redirect('/user-home')
        else:
            messages.success(request, "Invalid username or password")
            return redirect('/login')
    else:
        return render(request, 'registration/login.html', {})




def car_info(request):
    if request.method == 'POST':
        form = Car_info_form(request.POST)
        if form.is_valid():
            data_instance = form.save(commit=False)
            data_instance.owner = request.user
            data_instance.save()
            return redirect('/last_maintenance')
    else:
        form = Car_info_form()

    return render(request, 'main/create_car_data.html', {'form': form})






@login_required(login_url='/login')
def forum(request):
    posts = Post.objects.all()
    return render(request, 'main/forum.html', {"posts": posts})




@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        post.delete()
        return redirect('forum')  # Redirect to the forum or any other page after deletion

    return render(request, 'posts/delete_post.html', {'post': post})




@login_required(login_url='/login')
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/forum')
    else:
        form = PostForm()
    
    return render(request, 'main/create_post.html', {'form': form})


@login_required(login_url='/login')
def about_mechanic(request):
    reviews = LeaveReview.objects.all().order_by('created_on')

    if request.method == "POST":
        form = leave_review_form(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.client_username_id = request.user
            review.save()
            return redirect('/about-mechanic')
        
    else:
        form = leave_review_form()

        context = {'form': form, 'data': reviews}

    return render(request, 'main/about_mechanic.html', context)






from .forms import ServiceRequestForm
@login_required(login_url='/login')
def service_request_view(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)

        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.client_username_id = request.user
            form.save()
            return redirect('service_request_view')  # Redirect to a success page
    else:
        form = ServiceRequestForm()

    return render(request, 'main/request_service_form.html', {'form': form})


def service_request_list(request):
    service_data = ServiceRequest.objects.filter(client_username_id=request.user).order_by('created_on')
    return render(request, 'main/service_request_list.html', {'data': service_data})




@login_required(login_url='/login')
def available_mechanics(request):
    return render(request, 'main/available-mechanics.html', {})





@login_required(login_url='/login')
def most_recent_maintenace(request):
    
    form = upcoming_maintenance_form(request.POST)

    if request.method == 'POST':

        if form.is_valid():
            upcoming_maintenance = form.save(commit=False)
            upcoming_maintenance.owner = request.user
            form.save()
            return redirect('/user-home')

    return render(request, 'main/last_maintenance.html', {})









def user_data(request, username):
    user = get_object_or_404(User, username=username)

    # Retrieve data for the user using your models and relationships
    user_posts = Post.objects.filter(author=user)
    user_cars = Car_Information.objects.filter(owner=user)
    user_service_requests = ServiceRequest.objects.filter(client_username_id=user)
    user_reviews = LeaveReview.objects.filter(client_username_id=user)
    user_most_recent_maintenance = MostRecentMaintenance.objects.filter(owner=user)
    
    # Convert data to dictionaries or any other format as needed
    context = {
        'data': user_posts,
        'data_01': user_cars,
        'data_02': user_service_requests,
        'data_03': user_reviews,
        'data_04': user_most_recent_maintenance,
    }

    return render(request, 'main/user_data.html', context)



def update_upcoming_maintenance(request, owner):
    post = get_object_or_404(MostRecentMaintenance, id=owner)
    
    if request.method == 'POST':
        form = upcoming_maintenance_form(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('user_data', username=post.owner.username)
    else:
        form = upcoming_maintenance_form(instance=post)

    return render(request, 'update_info/edit_upcoming_maintenance.html', {'form': form})


def update_car_info(request, owner):
    post = get_object_or_404(Car_Information, id=owner)
    if request.method == 'POST':
        form = Car_info_form(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('user_data', username=post.owner.username)
    else:
        form = Car_info_form(instance=post)

    return render(request, 'update_info/edit_car_info.html', {'form': form})




def BussinessCreation(request):
    Bussiness_Data = BussinessCreationModel.objects.filter()
    if request.method == 'POST':
        form = BusinessCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/bussiness_creation_form')
        
    form = BusinessCreationForm()

    context = { 

        'data_01': Bussiness_Data, 
        'form': form,
    }

    

    return render(request, 'maintenance/bussiness_creation.html', context)




def coming_soon(request):
    return render(request, 'main/coming_soon.html', {})



def Browse_Services(request):
    return render(request, 'main/browse_services.html', {})