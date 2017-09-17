import random
import json
from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from django.shortcuts import render
from WebTest.settings import DEBUG
from app.models import PlayerUI

imgs = ['paper_r.png', 'scissors_r.png', 'rock_r.png']
win_text = "Вы победили!"
lose_text = "Вы проиграли!"
draw_text = "Ничья!"

User = get_user_model()


def get_data(request):
    data = {
        "labels": 10,
        "defaultData": 5,
    }
    return JsonResponse(data)


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        if not request.session.session_key:
            request.session.save()

        try:
            player_ui = PlayerUI.objects.get(id=request.session.session_key)
        except PlayerUI.DoesNotExist:
            player_ui = PlayerUI(id=request.session.session_key)

        summ = player_ui.wins + player_ui.loses + player_ui.draws + 2
        labels = [i for i in (range(0, summ))]
        default_items = str(player_ui.sequence).split()
        # default_items.append(default_items[-1]);
        context = saveContext(player_ui)
        data = {
            "labels": labels,
            "defaultData": default_items,
            "context": context,
        }
        return Response(data)


def print_debug(player_ui):
    print(player_ui.id)
    # print(player_ui.human_story_choices)
    # print(player_ui.ai_story_choices)
    print(player_ui.draws + player_ui.loses + player_ui.wins)


def post_list(request):

    if not request.session.session_key:
        request.session.save()

    try:
        player_ui = PlayerUI.objects.get(id=request.session.session_key)
    except PlayerUI.DoesNotExist:
        player_ui = PlayerUI(id=request.session.session_key)

    if DEBUG:
        print_debug(player_ui)

    if 'btnPaper.x' in request.POST or 'btnScissors.x' in request.POST or 'btnRock.x' in request.POST:
        button_click(player_ui, request)
    elif 'btnReset' in request.POST:
        player_ui = reset_click(request)

    return render(request, 'app/post_list.html', context=saveContext(player_ui))


def button_click(player_ui, request):
    imgChangeHumanChoice(player_ui, request.POST)
    imgChangeAIChoice(player_ui, random.choice(imgs))

    compareTwoChooses(player_ui)

    updateScore(player_ui)

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


def compareTwoChooses(player_ui):
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
    player_ui.sequence += ' ' + str(player_ui.wins - player_ui.loses)


def updateScore(player_ui):
    player_ui.score_text = str(player_ui.wins) + ':' + str(player_ui.loses)
    if DEBUG:
        player_ui.ai_story_choices += player_ui.ai_choice[0] + ' '
        player_ui.human_story_choices += player_ui.human_choice[0] + ' '


def reset_click(request):
    player_ui = PlayerUI(id=request.session.session_key)
    player_ui.save()
    return player_ui


def saveContext(player_ui):
    return {
        'human_choice': player_ui.human_choice,
        'AI_choice': player_ui.ai_choice,
        'result_text': player_ui.result_text,
        'score_text': player_ui.score_text,
        'wins': player_ui.wins,
        'loses': player_ui.loses,
        'draws': player_ui.draws,
    }
