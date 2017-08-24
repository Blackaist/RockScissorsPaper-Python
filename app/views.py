import random

from django.shortcuts import render

imgs = ['paper_r.png', 'scissors_r.png', 'rock_r.png']

context = {
    'human_choice': 'scissors_r.png',
    'AI_choice': 'scissors_r.png',
    'result_text': '',
    'score_text': 'Счет: ',
    'wins': 0,
    'loses': 0,
    'draws': 0
}
win_text = "Вы победили!"
lose_text = "Вы проиграли!"
draw_text = "Ничья!"


def post_list(request):
    if 'btnPaper.x' in request.POST or 'btnScissors.x' in request.POST or 'btnRock.x' in request.POST:
        button_click(request)
    return render(request, 'app/post_list.html', context=context)


def imgChangeHumanChoise(request, str):
    context['human_choice'] = str


def imgChangeAIChoise(request, str):
    context['AI_choice'] = str


def compareTwoChooses():
    if context['human_choice'] == context['AI_choice']:
        context['result_text'] = draw_text
        context['draws'] += 1
    else:
        if context['human_choice'] == imgs[0] and context['AI_choice'] == imgs[2]\
                or context['human_choice'] == imgs[1] and context['AI_choice'] == imgs[0]\
                or context['human_choice'] == imgs[2] and context['AI_choice'] == imgs[1]:
            context['wins'] += 1
            context['result_text'] = win_text
        else:
            context['loses'] += 1
            context['result_text'] = lose_text


def updateScore():
    context['score_text'] = 'Счет: ' + str(context['wins']) + ' - ' + str(context['loses'])


def button_click(request):
    if 'btnPaper.x' in request.POST:
        imgChangeHumanChoise(request, imgs[0])
    elif 'btnScissors.x' in request.POST:
        imgChangeHumanChoise(request, imgs[1])
    else:
        imgChangeHumanChoise(request, imgs[2])

    imgChangeAIChoise(request, random.choice(imgs))
    compareTwoChooses()
    updateScore()
