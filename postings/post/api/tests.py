from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from rest_framework import status
from post.models import BlogPost
from rest_framework.reverse import reverse as api_reverse

from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER


# automated 
# new / blank db 

User = get_user_model()


class BlogPostAPITestCase(APITestCase):
    def setUp(self): # default method, if can be somewhere used as set_up()
        # user = User.objects.create(username = 'testcase',email='test@test.com')
        user_obj = User(username = 'testcase',email='test@test.com')
        user_obj.set_password("somerandompassword")
        user_obj.save()
        blog_post = BlogPost.objects.create(user=user_obj, title = 'testttile', content='some random content' )
        
    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count,1)
    
    def test_single_post(self):
        post_count = User.objects.count()
        self.assertEqual(post_count,1)

    def test_get_item(self):
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data= {}
        response = self.client.get(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)

    def test_get_list(self):
        data= {}
        url = api_reverse("api-postings:post-list-without-create")
        response = self.client.get(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)

    def test_update_item(self):
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data= {"title":"remanfosd" , "content":"skjsdfdf  sjk"}
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #print(response.data)


    def test_update_item_with_user(self):
        blog_post = BlogPost.objects.first()
        print(blog_post.content)
        url = blog_post.get_api_url()
        data= {"title":"remanfosd" , "content":"some more content"}
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)  # JWT <token>

        response = self.client.put(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)

    def test_post_item_with_user(self):
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)  # JWT <token>

        data= {"title":"hello title" , "content":"ssecont psot objectk"}
        url = api_reverse("api-postings:post-list-with-create")
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #print(response.data)

    def test_user_ownership(self):
        owner = User.objects.create(username='somertestuser')
        blog_post = BlogPost.objects.create(user=owner, title = 'testttile', content='some random content' )

        url = blog_post.get_api_url()
        data= {"title":"hello title" , "content":"ssecont psot objectk"}

        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.username,owner.username)

        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)  # JWT <token>

        response = self.client.put(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }

