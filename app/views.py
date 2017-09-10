from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()


def get_data(request):
    data = {
        "doge": 10,
        "shiba": 5,
    }
    return JsonResponse(data)


class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        labels = ["Users", "0", "1", "2", "3"]
        default_items = [qs_count, 0, -1, 0, 1]
        data = {
            "labels": labels,
            "defaultData": default_items,
        }
        return Response(data)