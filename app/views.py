from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Sum

from app.models import PlayerUI, GlobalStatistic


def get_data(request):
    data = {
        "doge": 10,
        "shiba": 4,
    }
    return render(request, 'app/stats.html', context=data)


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

        global_stat = GlobalStatistic.objects.get(id='globals')

        # globals
        wins = global_stat.wins
        loses = global_stat.loses
        draws = global_stat.draws
        global_pie_percent_of_wins = [wins, loses, draws]

        global_polar_story_choices = [global_stat.rocks, global_stat.scissors, global_stat.papers]

        global_bubble_story = []
        y, r, i = 0, 0, 0
        pair = list(map(float, global_stat.pair_y_r.split()))
        for symbols in pair:
            if i % 2 == 0:
                y = symbols
            else:
                r = int(symbols)
                global_bubble_story += [{'x': (i - 1)*5, 'y': y, 'r': r}]
            i += 1

        # locals
        wins = player_ui.wins
        loses = player_ui.loses
        draws = player_ui.draws
        local_pie_percent_of_wins = [wins, loses, draws]

        str_of_choices = player_ui.human_story_choices
        local_polar_story_choices = [str_of_choices.count('r'), str_of_choices.count('s'), str_of_choices.count('p')]

        labels = ["0", "1", "2"]
        default_items = [0, -1, 0]
        data = {
            "labels": labels,
            "defaultData": default_items,

            "globalPiePercentOfWins": global_pie_percent_of_wins,
            "localPiePercentOfWins": local_pie_percent_of_wins,

            "globalPolarChoices": global_polar_story_choices,
            "localPolarChoices": local_polar_story_choices,

            "globalBubbleStory": global_bubble_story,
        }
        return Response(data)
