# generic views
# django-rest-framework.org 

from rest_framework import generics, mixins
from post.models import BlogPost
from .permissions import IsOwnerOrReadOnly
from .serializers import BlogPostSerializer
from django.db.models import Q



class BlogPostAPIView(generics.CreateAPIView):  # Create View # CreateAPIView
    pass
    lookup_field = 'pk'
    # queryset = BlogPost.object.all()
    serializer_class = BlogPostSerializer
    
    def get_queryset(self):
        return BlogPost.objects.all()
    def perform_create(self,serializer):
        serializer.save(user = self.request.user)





class BlogPostListAPIView(generics.ListAPIView):  # ListView # ListAPIView
    pass
    lookup_field = 'pk'
    # queryset = BlogPost.object.all()
    serializer_class = BlogPostSerializer
    
    def get_queryset(self):
        return BlogPost.objects.all()
    def perform_create(self,serializer):
        serializer.save(user = self.request.user)




class BlogPostListCreateAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # ListView # ListAPIView with Create API
    pass
    lookup_field = 'pk'
    # queryset = BlogPost.object.all()
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        qs = BlogPost.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(title__icontains=query)|Q(content__icontains=query)).distinct()
        return qs

    def perform_create(self,serializer):
        serializer.save(user = self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
    # def patch(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)


        # One Way TO include POST method in LIST api view.
    # def post(self, request, *args, **kwargs):
    #     return #

    def get_serializer_context(self, *args, **kwargs):
        return {"request":  self.request}







class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):  # detailview # RetrieveAPIView
    pass
    lookup_field = 'pk'
    # queryset = BlogPost.object.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return BlogPost.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return BlogPost.objects.get(pk = pk)

    def get_serializer_context(self, *args, **kwargs):
        return {"request":  self.request}           # to pass request to serializer class