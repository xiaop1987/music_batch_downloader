#coding:utf8
import sys, os
import logging
import music_list_parser.parser_factory as parser_factory
import music_downloader.downloader_factory as downloader_factory

logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), level = logging.info, filemode = 'w', format = '%(asctime)s - %(levelname)s: %(message)s')  
logger = logging.getLogger("")

if __name__ == '__main__':
    usage = 'python %s music_list output_dir'% sys.argv[0]
    if len(sys.argv) != 3:
        logger.error('Invalid parameter count')
        sys.exit(2)
           
    music_list_parser = parser_factory.get_parser(sys.argv[1])
    music_downloader = downloader_factory.get_downloader(sys.argv[2])
    while True:
        music_info = music_list_parser.get_next_music_info()
        if music_info == None:
            break       
        ret_code = music_downloader.download(music_info)
        if not ret_code:
            logger.error('Get music:[%s] failed.' % music_info['song_title'])
        logger.info('Get music:[%s] success.' % music_info['song_title'])
