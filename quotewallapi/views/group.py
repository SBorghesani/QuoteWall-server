"""View module for handling requests about groups"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth import get_user, get_user_model
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from quotewallapi.models import Quote, Group, ApprovalRequest
from django.db.models import Q
from datetime import datetime
from rest_framework.decorators import action


class GroupView(ViewSet):
    """QuoteWall"""

    @action(methods=['post', 'delete'], detail=True)
    def join(self, request, pk=None):
        """Managing users joining groups"""

        user=request.auth.user
        group_user=self.request.query_params.get('groupuser')
        user_request=self.request.query_params.get('userrequest')

        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response({'message': "Group does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == "POST":
            if user_request is not None:
                try:
                    group.requests.add(user)
                    return Response({"message": 'request submitted'}, status=status.HTTP_201_CREATED)
                
                except Exception as ex:
                    return Response({'reason': ex.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
            elif group_user is not None:
                try:
                    group.members.add(group_user)
                    return Response({"message": 'user added to group'}, status=status.HTTP_201_CREATED)
                except Exception as ex:
                    return Response({'message': ex.args[0]})
            else:
                try:
                    group.members.add(user)
                    return Response({"message": "user joined group"}, status=status.HTTP_201_CREATED)
                except Exception as ex:
                    return Response({'message': ex.args[0]})

        elif request.method == "DELETE":
            if user_request is not None:
                try:
                    group.requests.remove(user_request)
                    return Response({'message': "user removed from requests"}, status=status.HTTP_204_NO_CONTENT)
                except Exception as ex:
                    return Response({'message': ex.args[0]})
            if (group_user is not None and int(group_user) != group.admin.id):
                try:
                    group.members.remove(group_user)
                    return Response({"message": 'user removed from group'}, status=status.HTTP_204_NO_CONTENT)
                except Exception as ex:
                    return Response({'message': ex.args[0]})
            elif (user.id == group.admin.id):
                return Response({"message": "cannot remove admin"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    group.members.remove(user)
                    return Response({"message": "user left group"}, status=status.HTTP_204_NO_CONTENT)
                except Exception as ex:
                    return Response({'message': ex.args[0]})

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized group instance
        """
        user=request.auth.user

        try:
            group = Group.objects.create(
                admin=user,
                name=request.data["name"],
                description=request.data["description"],
                private=request.data['private'],
                created_on=datetime.now().strftime("%Y-%m-%d")
            )
            group.members.add(user)
            serializer = GroupSerializer(group, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single group
        Returns:
            Response -- JSON serialized group instance
        """
        try:
            group = Group.objects.get(pk=pk)

            serializer = GroupSerializer(group, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as ex:
            return Response({'message': 'group not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to groups resource
        Returns:
            Response -- JSON serialized list of groups
        """
        user_groups = self.request.query_params.get("mygroups", None)
        user = self.request.auth.user
        groups = Group.objects.all()
        search = self.request.query_params.get("q", None)

        if search is not None:
            groups = Group.objects.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        if user_groups is not None:
            groups = user.member_of.all()[:10]

        serializer = GroupSerializer(groups, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Handle PUT requests for a group
        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            admin = request.auth.user
            group = Group.objects.get(pk=pk)
            group.name = request.data['name']
            group.description = request.data['description']
            group.admin = admin
            group.private = request.data['private']
            group.created_on = datetime.now().strftime("%Y-%m-%d")

            group.save()

            return Response({"message": "group updated"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single group
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            group = Group.objects.get(pk=pk)
            group.delete()

            return Response({"message": "group deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Quote.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdminGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')

class MemberGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')
        depth = 1

class GroupSerializer(serializers.ModelSerializer):
    """JSON serializer for groups
    
    Arguments:
        serializer type
    """
    requests = RequestSerializer(many=True)
    admin = AdminGroupSerializer(many=False)
    members = MemberGroupSerializer(many=True)
    class Meta:
        model = Group
        fields = ('id', 'name', 'description', 'admin', 'private', 'created_on', 'members', 'requests')
        depth = 1