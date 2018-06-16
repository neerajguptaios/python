# use of serializers - 
# 1. Converts to JSON
# 2. Validations of data passed


from rest_framework import serializers

from post.models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = BlogPost
        fields = [
            'pk',
            'url',
            'user',
            'title',
            'content',
            'timestamp',
        ]
        read_only_fields = ['user']

    def get_url(self,obj):
        #request
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    # def validate() to validate all fields
    def validate_title(self, value):
        qs = BlogPost.objects.filter(title__iexact=value)   # title__iexact is used for case insensitive search
        if self.instance:
            qs  = qs.exclude(pk = self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Title has been used before')
        return value

