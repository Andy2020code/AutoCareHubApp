from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .models import Event
from main.models import Car_Information
from .forms import EventForm
from main.forms import Car_info_form

@login_required(login_url='/login')
def index(request):
    return render(request, 'scheduler/calendar.html')

@login_required(login_url='/login')
def step_02(request):
    warning_message = None
    requester = request.user
    user_car_info = Car_Information.objects.filter(owner=requester).first()

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            # Process the form data if it is valid
            # For example, save it to the database
            form.save()
            return redirect('scheduler:step_03')  # Redirect to a success page
        else:
            # If the form is not valid, set a warning message
            warning_message = "No available appointments with that time."
    else:
        form = EventForm()

    context = {
        'form': form,
        'warning_message': warning_message,
        'requester': requester,
        'user_car_info': user_car_info,
    }

    return render(request, 'scheduler/step_02.html', context)


@login_required(login_url='/login')
def update_car_info(request):
    requester = request.user
    try:
        # Retrieve the user's car information
        car_info = Car_Information.objects.get(owner=request.user)
    except Car_Information.DoesNotExist:
        # If car information doesn't exist, create a new instance
        car_info = None

    if request.method == 'POST':
        if car_info:  # If car information exists, update it
            form = Car_info_form(request.POST, instance=car_info)
        else:  # If car information doesn't exist, create a new instance
            form = Car_info_form(request.POST)
        if form.is_valid():
            car_info = form.save(commit=False)
            car_info.owner = request.user
            form.save()
            return redirect('scheduler:step_02')

    else:
        form = Car_info_form(instance=car_info)

    context = {
        'form': form,
        'requester': requester,
        'car_info': car_info,
    }
    return render(request, 'scheduler/update-car-info.html', context)


    
@login_required(login_url='/login')
def step_03(request):
    latest_event = Event.objects.latest('id')
    car_info = Car_Information.objects.get(owner=request.user)


    context = {
        'latest_event': latest_event,
        'car_info': car_info,
    }

    return render(request, 'scheduler/step_03.html', context)


@login_required(login_url='/login')
def success_schedule(request):
    user_events = Event.objects.filter(user=request.user).latest('id')
    
    return render(request, 'scheduler/schedule-confirm.html', {'event': user_events})
