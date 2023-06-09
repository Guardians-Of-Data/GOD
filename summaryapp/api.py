from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

class CrawlingList(APIView):
    def get(self, request):
        model = Crawling.objects.all()
        serializer = CrawlingSerializer(model, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = CrawlingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CrawlingDetail(APIView):
    def get(self, request, pk):
        model = Crawling.objects.get(pk=pk)
        serializer = CrawlingSerializer(model)
        return Response(serializer.data)

    # def put(self, request, pk):
    #     serializer = CrawlingSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk):
    #     model = Crawling.objects.get(pk=pk)
    #     model.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)