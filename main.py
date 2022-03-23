import requests
import pytube
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

def link_clip(raw_html):
    urls = []
    pattern_start = '"url":"/watch?v='
    pattern_end = '"'
    index = 0
    length = len(raw_html)
    while index < length:
        start = raw_html.find(pattern_start, index)
        if start > 0:
            start = start + len(pattern_start)
            end = raw_html.find(pattern_end, start)
            link = raw_html[start:end]
            urls.append(link)
            index = end
        else:
            break
    return urls

def link_channel(raw_html):
    urls = []
    pattern_start = '"url":"/c'
    pattern_end = '"'
    index = 0
    length = len(raw_html)
    while index < length:
        start = raw_html.find(pattern_start, index)
        if start > 0:
            start = start + len(pattern_start)
            end = raw_html.find(pattern_end, start)
            link = raw_html[start:end]
            urls.append(link)
            index = end
        else:
            break
    return urls

# get the most relevance video for get channel name
def getMostRelevance(url):
    raw_html = requests.get(url).text
    initial_id = link_clip(raw_html)[0]
    initial_link = "https://www.youtube.com/watch?v="+initial_id
    return initial_link

# get channel link
def getChannel(initial_link):
    raw_html = requests.get(initial_link).text
    channel_link = link_channel(raw_html)
    channel_link = "https://www.youtube.com/c" + channel_link[0]
    return channel_link

# go to video menu in channel
def downloadList(channel_link,n_clips):
    channel_link = channel_link + "/videos"
    raw_html = requests.get(channel_link).text

    id = []
    pattern_start = '"url":"/watch?v='
    pattern_end = '"'
    index = 0
    length = len(raw_html)
    while index < length:
        start = raw_html.find(pattern_start, index)
        if start > 0:
            start = start + len(pattern_start)
            end = raw_html.find(pattern_end, start)
            link = raw_html[start:end]
            id.append(link)
            index = end
        else:
            break
 
    # total clip that this code can load
    t_clips = len(id)
    download_list = []

    if n_clips > t_clips:
        print("Cannot downloads many clip that you want, Can download only",str(len(id)) + " clips with this query.")
        main()
    else:
        for i in range (0,n_clips):
            link_clip = "https://www.youtube.com/watch?v=" + id[i]
            download_list.append(link_clip)
    return download_list

def download(download_list,n_clips):
    for i in range (0,n_clips):
        yt = pytube.YouTube(download_list[i])
        stream = yt.streams.get_highest_resolution()
        stream.download()
    print("download success")
    return ""

# main process
def main():
    n_clips = int(input('Number of clips do you want ? : '))
    initial_link = getMostRelevance(url)
    channel_link = getChannel(initial_link)
    download_list = downloadList(channel_link,n_clips)
    if download_list != []:
        download(download_list,n_clips)

# global
query = str(input('what are the clips about ? : '))
url = 'https://www.youtube.com/results?search_query='+query
main()
