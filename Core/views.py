from django.shortcuts import render

def dashboard(request):
    role = 'Admin'
    title = 'Good Morning'
    desc = 'Your performance summary this week'

    context = {
        'role': role,
        'title': title,
        'desc': desc
    }
    return render(request, 'core/dashboard.html', context)