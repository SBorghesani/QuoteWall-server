"""View module for handling requests about quotes"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth import get_user, get_user_model
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from quotewallapi.models import Quote, Group
from datetime import datetime


class QuoteView(ViewSet):
    """QuoteWall"""
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized quote instance
        """
        user=request.auth.user
        group=Group.objects.get(pk=request.data["groupId"])

        try:
            quote = Quote.objects.create(
                user=user,
                group=group,
                quote_text=request.data["quoteText"],
                quoter=request.data["quoter"],
                context=request.data["context"],
                date_added=datetime.now().strftime("%Y-%m-%d")
            )

            serializer = QuoteSerializer(quote, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single quote
        Returns:
            Response -- JSON serialized quote instance
        """
        try:
            quote = Quote.objects.get(pk=pk)

            serializer = QuoteSerializer(quote, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as ex:
            return Response({'message': 'quote not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to quotes resource
        Returns:
            Response -- JSON serialized list of quotes
        """
        user = self.request.auth.user
        quotes = Quote.objects.all().order_by("-date_added")
        groups = user.member_of.all()
        group_query = self.request.query_params.get("group", None)
        myfeed = self.request.query_params.get("myfeed", None)
        search = self.request.query_params.get("q", None)
        

        if group_query is not None:
            quotes = quotes.filter(group__id=group_query).order_by("-date_added")
            if search is not None:
                quotes = quotes.filter(
                    Q(quote_text__icontains=search) |
                    Q(context__icontains=search)
                )
            

        elif myfeed is not None:
            quotes = quotes.filter(group__in = groups)[:20]

        else:
            quotes = quotes.filter(group__private = False)[:20]

        serializer = QuoteSerializer(quotes, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Handle PUT requests for a quote
        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            user=request.auth.user
            group=Group.objects.get(pk=request.data["groupId"])
            quote = Quote.objects.get(pk=pk)
            quote.quote_text = request.data['quoteText']
            quote.quoter = request.data['quoter']
            quote.context = request.data['context']
            quote.date_added = datetime.now().strftime("%Y-%m-%d")
            quote.user = user
            quote.group = group

            quote.save()

            return Response({"message": "quote updated"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single quote
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            quote = Quote.objects.get(pk=pk)
            quote.delete()

            return Response({"message": "quote deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Quote.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QuoteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')

class QuoteSerializer(serializers.ModelSerializer):
    """JSON serializer for quotes
    
    Arguments:
        serializer type
    """
    user = QuoteUserSerializer(many=False)
    class Meta:
        model = Quote
        fields = ('id', 'user', 'group', 'quote_text', 'quoter', 'context', 'date_added')
        depth = 1

