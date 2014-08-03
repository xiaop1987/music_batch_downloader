#coding:utf-8
import os
import urllib, urllib2
from urllib import quote
from bs4 import BeautifulSoup
import logging
import threading
import time

logger = logging.getLogger('')
class DownloadThread(threading.Thread):
    def __init__(self, output_dir, download_url, song_title, type):
        threading.Thread.__init__(self)
        self.output_dir = output_dir
        self.download_url = download_url
        self.song_title = song_title
        self.type = type

    def run(self):
        print 'start to download: ', self.song_title
        output_file_path = self.output_dir + '/' + self.song_title
        if type == '1' or type == '8':
            output_file_path += '.mp3'        
        else:
            logger.error('Unrecognized type:[%s] with download  url:[%s] song title:[%s]' % (type, self.download_url,
                self.song_title))
            return False
        url_obj = urllib2.urlopen(self.download_url)
        f = open(output_file_path, 'wb')
        file_size_dl = 0  
        block_sz = 8192  
        while True:  
            buffer = url_obj.read(block_sz)  
            if not buffer:  
                break  
            file_size_dl += len(buffer)  
            f.write(buffer)  
            time.sleep(0.1)
        f.close()  
        logger.info('Save file:[%s] to [%s]' % (self.song_title, self.output_file_path))
        #print urllib.urlretrieve(download_url, output_file_path)
        return True

class BaiduMusicDownloader(object):
    """description of class"""
    def __init__(self, output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
            logger.info('Make dir:[%s] success' % output_dir)
        elif not os.path.isdir(output_dir):
            return None
        self.output_dir = output_dir
        self.download_url_template = 'http://box.zhangmen.baidu.com/x?op=12&count=1&title=%(song_title)s$$%(performer)s$$$$'

    def __parse_return_xml(self, xml):
        soup = BeautifulSoup(xml)
        count = int(soup.count.contents[0])
        if count == 0:
            return False, None, None
        download_url = soup.result.url.find('encode').contents[0]
        download_file_name = soup.result.url.find('decode').contents[0]
        type = soup.result.url.find('type').contents[0]
        temp = download_url.split('/')
        temp[-1] = download_file_name
        download_url = ('/').join(temp)
        return True, type, download_url

    def download(self, music_info):
        song_title = music_info['song_title']
        performer = music_info['performer']
        
        param_map = {}
        param_map['song_title'] = quote(song_title.encode('utf-8')).encode('utf-8')
        param_map['performer'] = quote(performer.encode('utf-8')).encode('utf-8')
        search_url = self.download_url_template % param_map
        req = urllib.urlopen(search_url)
        try:
            xml = req.read().decode('utf-8')
        except:
            logger.error('Search song:[%s] failed.' % song_title)
            return False
        ret_code, type, download_url = self.__parse_return_xml(xml)
        if not ret_code:
            logger.error('Search song:[%s] failed.' % song_title)
            return False
        download_thread = DownloadThread(self.output_dir, download_url, song_title, type)
        download_thread.start()
        download_thread.join(10)
        return True

if __name__ == '__main__':
    downloader = BaiduMusicDownloader("./output/")
    music_info = {
                  'song_title':'¥Û‘º‘⁄∂¨ºæ',
                  'performer':'∆Î«ÿ'
                  }
    downloader.download(music_info)
