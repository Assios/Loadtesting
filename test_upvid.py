import unittest
from random import random
from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.utils import extract_token
from funkload.Lipsum import Lipsum

class test_upvid(FunkLoadTestCase):
    def setUp(self):
        """Setting up test."""
        self.server_url = self.conf_get('main', 'url')

    def test_user_signup(self):
        server_url = self.server_url
        self.get(server_url, description='Get root URL')
        self.get(server_url + "/users/sign_up", description="View the user signup page")

        auth_token = extract_token(self.getBody(), 'name="authenticity_token" type="hidden" value="', '"')
        email = Lipsum().getUniqWord() + "@" + Lipsum().getWord() + ".com"

        self.post(self.server_url + "/users",
            params=[['user[email]', email],
            ['user[password]', 'a'],
            ['user[password_confirmation]', 'a'],
            ['authenticity_token', auth_token],
            ['commit', 'Sign up']],
            description="Create New User")

    def test_user_login(self):
        server_url = self.server_url
        self.get(server_url, description='Get root URL')
        self.get(server_url + "/users/sign_in", description="View the user signin page")

        auth_token = extract_token(self.getBody(), 'name="authenticity_token" type="hidden" value="', '"')
        email = "a@a.com"
        password = "a"

        self.post(self.server_url + "/users/sign_in",
            params=[['user[email]', email],
            ['user[password]', password],
            ['authenticity_token', auth_token],
            ['commit', 'Sign in']],
            description="Login")       

    def test_index(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin test ---------------------------------------------
        nb_time = self.conf_getInt('test_index', 'nb_time')
        for i in range(nb_time):
            self.get(server_url, description='Get URL')
        # end test -----------------------------------------------
    def test_show_video(self):
        server_url = self.server_url
        nb_time = self.conf_getInt("test_show_video", 'nb_time')
        for i in range(nb_time):
            self.get(server_url + "/videos/2", description="Get video")
        # end test ---
    def test_show_user(self):
        server_url = self.server_url
        nb_time = self.conf_getInt("test_show_user", 'nb_time')
        for i in range(nb_time):
            self.get(server_url + "/users/2", description="Get user")
        # end test ---
    def test_show_comments(self):
        server_url = self.server_url
        nb_time = self.conf_getInt("test_show_comments", 'nb_time')
        for i in range(nb_time):
            self.get(server_url + "/comments", description="Get comments") 

if __name__ in ('main', '__main__'):
    unittest.main()
