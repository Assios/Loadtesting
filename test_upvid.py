import unittest
from random import random
from funkload.FunkLoadTestCase import FunkLoadTestCase

class test_upvid(FunkLoadTestCase):
    def setUp(self):
        """Setting up test."""
        self.server_url = self.conf_get('main', 'url')

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
