from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework import generics , permissions

from .models import User , Account , Post , PostLike , Comment , MarketPlace , Public , PrivateG
from .serializer import (
       RegistrationSerializer ,  AccountSerializer ,
       PostSerializer , PostLikeSerializer ,
       CommentSerializer , MarketPlaceSerializer ,
       JoinPrivateGroupSerializer , JoinPublicGroupSerializer ,
       PublicGroupSerializer , PrivateGroupSerializer , 
       CreatePostInPrivateGroupSerializer , CreatePostInPublicGroupSerializer ,
       PrivateSerializer , PublicSerializer
)
from .throttling import CreatingPrivateGroupThrottle
from .permissions import (
       ProfilePermission , PrivateGroupPermission ,
       PermissionToUpdatePrivateGroup,PermissionModifyComment
       )
from django.shortcuts import redirect , get_object_or_404
 

class RegisterEndPoint(APIView) :
       permission_classes = [permissions.AllowAny]
       def post(self,request,*args,**kwargs) :
              
              data = request.data
              serializer = RegistrationSerializer(data=data)
              if serializer.is_valid(raise_exception = True) :
                     serializer.save()
                     return Response(f"Account Created Successfuly..." , status=status.HTTP_201_CREATED)
              
              return Response(serializer.errors , status=status.HTTP_406_NOT_ACCEPTABLE)

class AuthUsersView(APIView) :
       def get(self,request, *args,**kwargs) :
              user = self.request.user
              return Response(f"{user}")

class UserProfileEndPoint(APIView) :
       permission_classes = [ProfilePermission]
       def get(self,request,*args,**kwargs) :
              if self.request.user.is_authenticated :
                     user = self.request.user
                     account = get_object_or_404(Account,user=user)
                     serializer  = AccountSerializer(account , many=False)
                     return Response(serializer.data , status=status.HTTP_200_OK)
              else :
                     return redirect("/api/token/")
              
class UpdateProfileInformations(generics.UpdateAPIView) :
       serializer_class = AccountSerializer
       permission_classes = [ProfilePermission]
       queryset = Account.objects.all()
       lookup_field = "pk"

class PostEndPoint(GenericAPIView ,CreateModelMixin) :
       permission_classes = [permissions.IsAuthenticated]
       serializer_class = PostSerializer
       def post(self , request , *args , **kwargs) :
              serializer = self.get_serializer(data=request.data)
              
              if serializer.is_valid() :
                     author = self.request.user
                     title  = serializer.validated_data["title"]
                     descriptions = serializer.validated_data["descriptions"]
                     try :
                            account = Account.objects.get(user=author)
                     except Account.DoesNotExist :
                            return Response("error")
                     
                     post = Post.objects.create(
                            title = title,
                            descriptions = descriptions , 
                            account = account
                     )
                     post.save()
                     return Response(serializer.data , status=status.HTTP_201_CREATED)
              
              return Response(serializer.errors , status=status.HTTP_406_NOT_ACCEPTABLE)

class PostListEndPoint(generics.ListAPIView) :
       serializer_class = PostSerializer
       queryset = Post.objects.all()
       permission_classes = [permissions.IsAuthenticated]

class PostDetailEndpoint(generics.RetrieveUpdateAPIView) :
       serializer_class = PostSerializer
       queryset = Post.objects.all()
       lookup_field = "pk"              
       permission_classes = [permissions.IsAuthenticated]

class DeletePostEndpoint(generics.DestroyAPIView) :
       serializer_class = PostSerializer
       queryset = Post.objects.all()
       lookup_field = "pk"              
       permission_classes = [permissions.IsAuthenticated]


class LikePostEndPoint(GenericAPIView , CreateModelMixin) :
       serializer_class = PostLikeSerializer
       permission_classes = [permissions.IsAuthenticated]
       def post(self,request,*args,**kwargs) :
              data = request.data
              serializer = self.get_serializer(data=data)

              if serializer.is_valid(raise_exception=True) :
                     post = serializer.validated_data["post"]
                     account = serializer.validated_data["account"]

                     post_like_filter = PostLike.objects.filter(account=account)

                     if post_like_filter :
                            post_like_filter.delete()
                            return Response("u remove the like")
                     
                     like = PostLike.objects.create(
                            post = post ,
                            account = account, 
                     )
                     like.save()
                     return Response({"msg": f"congrats ...{account.user.username} you like post of"})
            
              return Response(serializer.errors , status=status.HTTP_404_NOT_FOUND)
                     
class CommentsEndPoint(GenericAPIView,CreateModelMixin):
       serializer_class = CommentSerializer
       permission_classes = [permissions.IsAuthenticated]
       def post(self,request ,*args ,**kwargs) :
              serializer = self.get_serializer(data = request.data)
              if serializer.is_valid() :
                     try :
                            post    = serializer.validated_data["post"]
                            account = serializer.validated_data["account"]
                            content = serializer.validated_data["content"]
                     except :
                            return Response("error..")
                     
                     comments = Comment.objects.create(
                            post = post ,
                            account = account,
                            content = content
                     )
                     comments.save()
                     return Response(serializer.data , status=status.HTTP_201_CREATED)
              
              return Response({"error message" : serializer.errors} , status=status.HTTP_400_BAD_REQUEST)
                     
class RUD_Comment(generics.RetrieveUpdateDestroyAPIView) :
       serializer_class = CommentSerializer
       queryset = Comment.objects.all()
       lookup_field = "pk"
       permission_classes = [PermissionModifyComment]

class MarketPlaceEndpoint(GenericAPIView,CreateModelMixin) :
       serializer_class = MarketPlaceSerializer
       permission_classes = [permissions.IsAuthenticated]

       def post(self,request,*args,**kwargs) :
              serializer = self.get_serializer(data=request.data)
              user = self.request.user
              if serializer.is_valid() :
                     try :
                            seller_account = Account.objects.get(user=user)
                     except Account.DoesNotExist :
                            return Response("error")
                     
                     seller = serializer.validated_data["seller"]
                     product_name  = serializer.validated_data["product_name"]
                     product_image = serializer.validated_data["product_image"]
                     product_price = serializer.validated_data["product_price"]
                     product_informations = serializer.validated_data["product_informations"]

                     market_place = MarketPlace.objects.create(
                            seller = seller , 
                            product_name = product_name ,
                            product_image = product_image,
                            product_price = product_price , 
                            product_informations = product_informations
                     )

                     market_place.save()
                     return Response(serializer.data , status=status.HTTP_201_CREATED)
       
              return Response(serializer.errors , status=status.HTTP_404_NOT_FOUND)
       
class MarketProductEndpoint(generics.ListAPIView) :
       permission_classes = [permissions.IsAuthenticated]
       serializer_class = MarketPlaceSerializer
       queryset = MarketPlace.objects.all()

class SingleProduct(generics.RetrieveUpdateDestroyAPIView) :
       permission_classes = [permissions.IsAuthenticated]
       serializer_class = MarketPlaceSerializer
       queryset = MarketPlace.objects.all()
       lookup_field = "pk"

class PrivateGroupEndPoint(GenericAPIView, CreateModelMixin) :
       serializer_class = JoinPrivateGroupSerializer
       permission_classes = [permissions.IsAuthenticated]
       queryset = PrivateG.objects.all()
       
       def post(self,request,*args,**kwargs) :
              serializer = self.get_serializer(data=request.data)
              if serializer.is_valid() :
                    
                     active_account = self.request.user.accounts
                     group_id = serializer.validated_data["group_id"]
                     code = serializer.validated_data["code"]

                     group = get_object_or_404(PrivateG , id=group_id)

                     if group.code == code and active_account not in group.members.all() :
                            group.members.add(active_account)
                            group.save()
                            return Response("congrats.. u join the groupe" , status=status.HTTP_202_ACCEPTED)
                     
                     return Response("invalid code.." , status=status.HTTP_404_NOT_FOUND)
       
              return Response("error" , status=status.HTTP_404_NOT_FOUND)
       

class PublicGroupEndPoint(GenericAPIView, CreateModelMixin) :
       serializer_class = JoinPublicGroupSerializer
       permission_classes = [permissions.IsAuthenticated]
       def post(self,request,*args,**kwargs) :
              serializer = self.get_serializer(data=request.data)
              if serializer.is_valid() :
                    
                     active_account = self.request.user.accounts
                     group_id = serializer.validated_data["group_id"]
                     group = get_object_or_404(Public , id=group_id)
                     group.members.add(active_account)
                     group.save()
              
                     return Response("you Join" , status=status.HTTP_202_ACCEPTED)
       
              return Response("error" , status=status.HTTP_404_NOT_FOUND)

class PrivateGroupList(generics.ListAPIView) :
       serializer_class = PrivateGroupSerializer
       queryset = PrivateG.objects.all()              
       permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PublicGroupList(generics.ListAPIView) :
       serializer_class = PublicGroupSerializer
       queryset = Public.objects.all()                
       permission_classes = [permissions.IsAuthenticatedOrReadOnly]
 

class CreatePostInPrivateGroup(GenericAPIView,CreateModelMixin) :
       serializer_class = CreatePostInPrivateGroupSerializer 
       permission_classes = [PrivateGroupPermission]
       def post(self,request,*args,**kwargs) :
              serializer = self.get_serializer(data=request.data)
              if serializer.is_valid() :
                     
                     account  = self.request.user.accounts
                     title  = serializer.validated_data["title"]
                     image  = serializer.validated_data["image"]
                     private = serializer.validated_data["private"]
                     descriptions = serializer.validated_data["descriptions"]
 
                     post = Post.objects.create(
                            title = title,
                            image = image,
                            private = private,
                            descriptions = descriptions,
                            account = account
                     )
                     post.save()
                     return Response(serializer.data , status=status.HTTP_201_CREATED)
              return Response("error")


class CreatePostInPublicGroup(GenericAPIView,CreateModelMixin) :
       serializer_class = CreatePostInPublicGroupSerializer 
       permission_classes = [PrivateGroupPermission]
       def post(self,request,*args,**kwargs) :
              serializer = self.get_serializer(data=request.data)
              if serializer.is_valid() :
                     
                     account  = self.request.user.accounts
                     title    = serializer.validated_data["title"]
                     image    = serializer.validated_data["image"]
                     private  = serializer.validated_data["private"]
                     descriptions = serializer.validated_data["descriptions"]

                     post = Post.objects.create(
                            title   = title,
                            image   = image,
                            private = private,
                            descriptions = descriptions,
                            account = account
                     )
                     post.save()
                     return Response(serializer.data , status=status.HTTP_201_CREATED)
              return Response("error")

class CreatePrivateGroup(GenericAPIView , CreateModelMixin) :
       serializer_class = PrivateSerializer
       # permission_classes = [permissions.IsAuthenticated]
       throttle_classes = [CreatingPrivateGroupThrottle]
       def post(self, request , *args , **kwargs) :
              serializer = self.get_serializer(data=request.data)

              if serializer.is_valid() :
                     owner = self.request.user.accounts
                     account=self.request.user.accounts
                     code  = serializer.validated_data["code"]

                     private = PrivateG.objects.create(owner=owner,code=code)
                     private.save()
                     return Response("created")
              
              return Response("wait")

class UpdatePrivateGroup(generics.UpdateAPIView) :
       serializer_class = PrivateSerializer
       permission_classes = [PermissionToUpdatePrivateGroup]
       queryset = PrivateG.objects.all()
       lookup_field = "pk"

       
class DeletePrivateGroup(generics.DestroyAPIView) :
       serializer_class   = PrivateSerializer
       permission_classes = [PermissionToUpdatePrivateGroup]
       queryset = PrivateG.objects.all()
       lookup_field = "pk"


class CreatePublicGroup(GenericAPIView , CreateModelMixin) :
       serializer_class = PublicSerializer
       permission_classes = [permissions.IsAuthenticated]
       throttle_classes = [CreatingPrivateGroupThrottle]
       def post(self, request , *args , **kwargs) :
              serializer = self.get_serializer(data=request.data)

              if serializer.is_valid() :
                     owner = self.request.user.accounts
                     private = PrivateG.objects.create(owner=owner)
                     private.save()
                     return Response("created")
              
              return Response("wait")
       
class UpdatePublicGroup(generics.UpdateAPIView) :
       serializer_class = PublicSerializer
       permission_classes = [PermissionToUpdatePrivateGroup]
       queryset = Public.objects.all()
       lookup_field = "pk"

       
class DeletePublicGroup(generics.DestroyAPIView) :
       serializer_class   = PublicSerializer
       permission_classes = [PermissionToUpdatePrivateGroup]
       queryset = Public.objects.all()
       lookup_field = "pk"
            