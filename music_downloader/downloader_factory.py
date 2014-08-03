import baidu_music_downloader
def get_downloader(output_dir):
    return baidu_music_downloader.BaiduMusicDownloader(output_dir)