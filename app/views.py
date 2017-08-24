import random


from django.shortcuts import render

from WebTest.settings import DEBUG
from app.models import PlayerUI

imgs = ['paper_r.png', 'scissors_r.png', 'rock_r.png']


win_text = "Вы победили!"
lose_text = "Вы проиграли!"
draw_text = "Ничья!"


def print_debug(player_ui, request):
    print(player_ui.id)


def post_list(request):
    player_ui = PlayerUI.objects.get(id=request.session.session_key)

    if DEBUG:
        print_debug(player_ui, request)

    if 'btnPaper.x' in request.POST or 'btnScissors.x' in request.POST or 'btnRock.x' in request.POST:
        button_click(player_ui, request)
    elif 'btnSubmit' in request.POST:
        reset_click(player_ui, request)

    context = saveContext(player_ui)

    return render(request, 'app/post_list.html', context=context)


def button_click(player_ui, request):
    imgChangeHumanChoice(player_ui, request.POST)
    imgChangeAIChoice(player_ui, random.choice(imgs))

    compareTwoChooses(player_ui, request)

    updateScore(player_ui, request)

    player_ui.save()


def imgChangeHumanChoice(player_ui, post):
    if 'btnPaper.x' in post:
        player_ui.human_choice = imgs[0]
    elif 'btnScissors.x' in post:
        player_ui.human_choice = imgs[1]
    else:
        player_ui.human_choice = imgs[2]


def imgChangeAIChoice(player_ui, str):
    player_ui.ai_choice = str


def compareTwoChooses(player_ui, request):
    if player_ui.human_choice == player_ui.ai_choice:
        player_ui.result_text = draw_text
        player_ui.draws += 1
    else:
        if player_ui.human_choice == imgs[0] and player_ui.ai_choice == imgs[2] \
                or player_ui.human_choice == imgs[1] and player_ui.ai_choice == imgs[0] \
                or player_ui.human_choice == imgs[2] and player_ui.ai_choice == imgs[1]:
            player_ui.wins += 1
            player_ui.result_text = win_text
        else:
            player_ui.loses += 1
            player_ui.result_text = lose_text


def updateScore(player_ui, request):
    player_ui.score_text = 'Счет: ' + str(player_ui.wins) + ' - ' + str(player_ui.loses)
    if DEBUG:
        player_ui.ai_story_choices += player_ui.ai_choice[0] + ' '
        player_ui.human_story_choices += player_ui.human_choice[0] + ' '


def reset_click(player_ui, request):
    player_ui = PlayerUI(id=request.session.session_key)
    player_ui.save()


def saveContext(player_ui):
    return {
        'human_choice': player_ui.human_choice,
        'AI_choice': player_ui.ai_choice,
        'result_text': player_ui.result_text,
        'score_text': player_ui.score_text,
        'wins': player_ui.wins,
        'loses': player_ui.loses,
        'draws': player_ui.draws
    }