#!/usr/bin/env python3

class point(object):
    def __init__(self, name, left_url, left_img, right_url, right_img):
        self.left_url = left_url
        self.left_img = left_img
        self.right_url = right_url
        self.right_img = right_img
        self.name = name
    def get_left_url(self):
        return self.left_url
    def get_right_url(self):
        return self.right_url
    def get_left_img(self):
        return self.left_img
    def get_right_img(self):
        return self.right_img
    def get_name(self):
        return self.name
