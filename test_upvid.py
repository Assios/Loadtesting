import unittest
from random import random
from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.utils import extract_token
from funkload.Lipsum import Lipsum
from webunit.utility import Upload

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

    def test_video_upload(self):
        server_url = self.server_url
        self.test_user_login()
        self.get(server_url + "/videos/new", description="View the user signin page")
        auth_token = extract_token(self.getBody(), 'name="authenticity_token" type="hidden" value="', '"')
        nb_time = self.conf_getInt("test_video_upload", 'nb_time')
        for i in range(nb_time):
            self.post(server_url + "/videos",
                params=[['authenticity_token', auth_token],
                        ['video[category]', Lipsum().getWord()],
                        ['upload[file]',  Upload("./vids/1.mp4")],
                        ['video[title]', Lipsum().getWord()]],
                        description = "upload video"
                    )

    def test_comment(self):
        server_url = self.server_url
        self.test_user_login()
        self.get(server_url + "/comments/new", description="View the comments")
        auth_token = extract_token(self.getBody(), 'name="authenticity_token" type="hidden" value="', '"')
        nb_time = self.conf_getInt("test_comment", 'nb_time')
        for i in range(nb_time):
            self.post(server_url + "/comments",
                params=[['authenticity_token', auth_token],
                        ['comment[message]', Lipsum().getWord()],
                        ['comment[video_id]', 1]],
                        description = "comment"
                )

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
            self.get(server_url + "/videos/1", description="Get video")
        # end test ---
    def test_show_user(self):
        server_url = self.server_url
        nb_time = self.conf_getInt("test_show_user", 'nb_time')
        for i in range(nb_time):
            self.get(server_url + "/users/1", description="Get user")
        # end test ---
    def test_show_comments(self):
        server_url = self.server_url
        nb_time = self.conf_getInt("test_show_comments", 'nb_time')
        for i in range(nb_time):
            self.get(server_url + "/comments", description="Get comments") 

    def test_critical_path(self):
        server_url = self.server_url
        nb_time = self.conf_getInt('test_critical_path', 'nb_time')

        #Test index
        for i in range(nb_time):
            self.get(server_url, description='Get URL')

        #Test user signup
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

        #Test user login
        email = "a@a.com"
        password = "a"

        self.post(self.server_url + "/users/sign_in",
            params=[['user[email]', email],
            ['user[password]', password],
            ['authenticity_token', auth_token],
            ['commit', 'Sign in']],
            description="Login") 

        self.test_video_upload()

        #Test show user
        for i in range(nb_time):
            self.get(server_url + "/users/1", description="Get user")

        #Test show video
        for i in range(nb_time):
            self.get(server_url + "/videos/1", description="Get video")

        #Test post comments
        self.test_user_login()
        self.get(server_url + "/comments/new", description="View the comments")
        auth_token = extract_token(self.getBody(), 'name="authenticity_token" type="hidden" value="', '"')
        nb_time = self.conf_getInt("test_comment", 'nb_time')
        for i in range(nb_time):
            self.post(server_url + "/comments",
                params=[['authenticity_token', auth_token],
                        ['comment[message]', Lipsum().getWord()],
                        ['comment[video_id]', 1]],
                        description = "comment"
                )

if __name__ in ('main', '__main__'):
    unittest.main()
    #print Upload("./vids/1.mp4")
