from django.test import TestCase

# Create your tests here.


from projects.models import Post


class PostListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create posts for pagination tests
        number_of_posts = 10
        for post_id in range(number_of_posts):
            Post.objects.create(title='Simulation'.format(post_id),
                                author='User'.format(post_id))

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/posts/')
        self.assertEqual(response.status_code, 200)



