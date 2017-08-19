from django.shortcuts import render

context = {
    'human_choise': 'scissors.jpg'
}

def post_list(request):
    if 'btnPaper.x' in request.POST or 'btnScissors.x' in request.POST or 'btnRock.x' in request.POST:
        button_click(request)
    return render(request, 'app/post_list.html', context=context)


def imgChoise(request, str):
    context['human_choise'] = str


def button_click(request):
    if 'btnPaper.x' in request.POST:
        imgChoise(request, "paper.jpg")
    elif 'btnScissors.x' in request.POST:
        imgChoise(request, "scissors.jpg")
    else:
        imgChoise(request, "rock.jpg")
    print(context['human_choise'])
