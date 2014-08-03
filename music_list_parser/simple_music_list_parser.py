import json

class SimpleMusicListParser(object):
    """An simple music list parser for raw text and one song name a line"""
    def __init__(self, music_list_input):
        with open(music_list_input, 'r') as f:
            self.info_list = json.loads(f.read())
        f.close()   
        self.index = 0
    
    def get_next_music_info(self):
        if self.index >= len(self.info_list):
            return None
        ret_obj = self.info_list[self.index]
        self.index += 1
        return ret_obj
    


