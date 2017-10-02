from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import connection

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
        games = wins + loses + draws
        global_pie_percent_of_wins = [round(wins/games, 2), round(loses/games, 2), round(draws/games, 2)]

        choices = global_stat.rocks + global_stat.scissors + global_stat.papers
        global_polar_story_choices = [round(global_stat.rocks/choices, 2), round(global_stat.scissors/choices, 2), round(global_stat.papers/choices, 2)]

        global_bubble_story = []
        with connection.cursor() as cursor:
            for i in range(1, 11):
                cursor.execute("SELECT (SUM(wins) - SUM(loses)) as result FROM app_playerui WHERE wins+draws+loses < %s AND wins+draws+loses >= %s", [i * 10, (i - 1) * 10])
                summary = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) as result FROM app_playerui WHERE wins+draws+loses < %s AND wins+draws+loses >= %s", [i * 10, (i - 1) * 10])
                playersCount = cursor.fetchone()[0]
                if summary is not None and playersCount is not None:
                    summary = summary / playersCount
                    global_bubble_story += [{'x': (i-1)*10, 'y': summary, 'r': playersCount}]

        # locals
        wins = player_ui.wins
        loses = player_ui.loses
        draws = player_ui.draws
        games = wins + loses + draws
        local_pie_percent_of_wins = [round(wins/games, 2), round(loses/games, 2), round(draws/games, 2)]

        str_of_choices = player_ui.human_story_choices
        choices = str_of_choices.count('r') + str_of_choices.count('s') + str_of_choices.count('p')
        local_polar_story_choices = [round(str_of_choices.count('r')/choices, 2), round(str_of_choices.count('s')/choices, 2), round(str_of_choices.count('p')/choices, 2)]

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
