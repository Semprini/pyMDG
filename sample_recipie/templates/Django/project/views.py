from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {
        'foo': 'bar',
    })


def streams(request):
    return render(request, 'streams.html', {
        'foo': 'bar',
    })
