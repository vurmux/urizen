#!/usr/bin/python3


class BasicGeneratorFactory(object):
    def __init__(self):
        pass
    
    def generate(self, w, h, **kwargs):
        raise NotImplementedError