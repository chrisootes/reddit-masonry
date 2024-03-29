#!python

import urllib.parse
import logging

logger = logging.getLogger(__name__)

def default(post: dict) -> str:
    """
    This function generates a embedded card html code from a PRAW post object
    """
    parsed = urllib.parse.urlparse(post['url'])
    logger.debug(f"Sending post: {post['name']}")
    if 'i.redd.it' in post['url'] and '.gif' in post['url']:
        #logger.debug(f"Preview: {post['preview']}")
        return f"""
            <div id="{post['name']}" class="col-sm-12 col-lg-6 col-xxl-4">
                <div class="card">
                    <h3 class="card-header">{post['title']}</h3>
                    <video controls=true poster="{post['thumbnail']}" preload="auto" muted=false loop=false webkit-playsinline="" style="width: 100%; height: 100%;">
                        <source src="{post['mp4']}" type="video/mp4">
                    </video>
                    <div class="card-body">
                        <p class="card-text">{post['subreddit_name_prefixed']} - <a class="card-link" href="http://old.reddit.com/comments/{post['id']}" target="_blank">Comments</a></p>
                    </div>
                </div>
            </div>
        """
    elif 'i.redd.it' in post['url']:
        return f"""
            <div id="{post['name']}" class="col-sm-12 col-lg-6 col-xxl-4">
                <div class="card">
                    <h3 class="card-header">{post['title']}</h3>
                    <img class="card-img-top" style="width: 100%;" src="{post['url']}">
                    <div class="card-body">
                        <p class="card-text">{post['subreddit_name_prefixed']} - <a class="card-link" href="http://old.reddit.com/comments/{post['id']}" target="_blank">Comments</a></p>
                    </div>
                </div>
            </div>
        """
    elif 'v.redd.it' in post['url']:
        if post['media'] is not None:
            return f"""
                <div id="{post['name']}" class="col-sm-12 col-lg-6 col-xxl-4">
                    <div class="card">
                        <h3 class="card-header">{post['title']}</h3>
                        <video data-dashjs-player src="{post['dash_url']}" controls></video>
                        <div class="card-body">
                            <p class="card-text">{post['subreddit_name_prefixed']}</p>
                             <a class="card-link" href="http://old.reddit.com/comments/{post['id']}" target="_blank">Comments</a>
                        </div>
                    </div>
                </div>
            """
        else:
            logger.error(f"Error no media for v.redd.it link: {post['url']}")
            return ""
    elif 'imgur' in post['url'] and ('gif' in post['url'] or 'mp4' in post['url']):
        imgur_id = parsed.path.split('.')[0].split('/')[-1]
        return f"""
            <div id="{post['name']}" class="col-sm-12 col-lg-6 col-xxl-4">
                <div class="card">
                    <h3 class="card-header">{post['title']}</h3>
                    <video controls=true poster="{post['thumbnail']}" preload="auto" muted=false loop=false webkit-playsinline="" style="width: 100%; height: 100%;">
                        <source src="//i.imgur.com/{imgur_id}.mp4" type="video/mp4">
                    </video>
                    <div class="card-body">
                        <p class="card-text">{post['subreddit_name_prefixed']} - <a class="card-link" href="http://old.reddit.com/comments/{post['id']}" target="_blank">Comments</a></p>
                    </div>
                </div>
            </div>
        """
    elif 'imgur' in post['url']:
        imgur_id = parsed.path.split('.')[0].split('/')[-1]
        #<blockquote class="imgur-embed-pub" lang="en" data-id="{imgur_id}" ><a href="{post['url']}">{post['title']}</a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>
        return f"""
            <div id="{post['name']}" class="col-sm-12 col-lg-6 col-xxl-4">
                <div class="card">
                    <h3 class="card-header">{post['title']}</h3>
                    <img class="" style="width: 100%;" src="//i.imgur.com/{imgur_id}.jpg">
                    <div class="card-body">
                        <p class="card-text">{post['subreddit_name_prefixed']} - <a class="card-link" href="http://old.reddit.com/comments/{post['id']}" target="_blank">Comments</a></p>
                    </div>
                </div>
            </div>
        """
    elif 'redgif' in post['url']:
        redgifs_id = parsed.path.split('.')[0].split('/')[-1].split('-')[0]
        #<iframe src='https://www.redgifs.com/ifr/lopsidedoddballharvestmen' frameborder='0' scrolling='no' allowfullscreen width='1080' height='1920'></iframe><p><a href='https://www.redgifs.com/watch/lopsidedoddballharvestmen'>via RedGIFs</a></p>
        return f"""
            <div id="{post['name']}" class="col-sm-12 col-lg-6 col-xxl-4">
                <div class="card">
                    <h3 class="card-header">{post['title']}</h3>
                    <div style='position:relative; padding-bottom:88.67%;'>
                        <iframe src='https://redgifs.com/ifr/{redgifs_id}' frameborder='0' scrolling='no' allowfullscreen width='100%' height='100%' style='position:absolute;top:0;left:0;'></iframe>
                    </div>
                    <div class="card-body">
                        <p class="card-text">{post['subreddit_name_prefixed']} - <a class="card-link" href="http://old.reddit.com/comments/{post['id']}" target="_blank">Comments</a></p>
                    </div>
                </div>
            </div>
        """
    elif 'gfycat' in post['url']:
        gfycat_id = parsed.path.split('.')[0].split('/')[-1].split('-')[0]
        return f"""
            <div id="{post['name']}" class="col-sm-12 col-lg-6 col-xxl-4">
                <div class="card">
                    <h3 class="card-header">{post['title']}</h3>
                    <div style='position:relative; padding-bottom:88.67%;'>
                        <iframe src='https://gfycat.com/ifr/{gfycat_id}?autoplay=0&controls=1' frameborder='0' scrolling='no' allowfullscreen width='100%' height='100%' style='position:absolute;top:0;left:0;'></iframe>
                    </div>
                    <div class="card-body">
                        <p class="card-text">{post['subreddit_name_prefixed']} - <a class="card-link" href="http://old.reddit.com/comments/{post['id']}" target="_blank">Comments</a></p>
                    </div>
                </div>
            </div>
        """
    else:
        thumbnail = post.get('thumbnail', '')
        thumbnail = thumbnail if thumbnail != '' else '/favicon.ico'
        return f"""
            <div id="{post['name']}" class="col-sm-12 col-lg-6 col-xxl-4">
                <div class="card">
                    <h3 class="card-header">{post['title']}</h3>
                    <a href="{post['url']}" target="_blank"><img class="card-img-top" style="width: 100%;" src="{thumbnail}"></a>
                    <div class="card-body">
                        <p class="card-text">{post['subreddit_name_prefixed']} - <a class="card-link" href="http://old.reddit.com/comments/{post['id']}" target="_blank">Comments</a></p>
                    </div>
                </div>
            </div>
        """
    return ""

def background(post: dict) -> str:
    """
    This function generates a embedded card html code from a PRAW post object
    """
    parsed = urllib.parse.urlparse(post['url'])
    logger.debug(f"Sending post: {post['name']}")
    if 'i.redd.it' in post['url']:
        return f"""
            <div id="{post['name']}" class="col-sm-3 col-lg-3 col-xxl-3">
               <img class="" style="width: 100%;" src="{post['url']}">
            </div>
        """
    elif 'v.redd.it' in post['url']:
        if post['media'] is not None:
            return ""
            return f"""
                <div id="{post['name']}" class="col-sm-3 col-lg-3 col-xxl-3">
                    <video style="width: 100%;" data-dashjs-player autoplay src="{post['media']['reddit_video']['dash_url']}" controls></video>
                </div>
            """
        else:
            logger.error(f"Error no media for v.redd.it link: {post['url']}")
            return ""
    elif 'imgur' in post['url'] and ('gif' in post['url'] or 'mp4' in post['url']):
        return ""
        imgur_id = parsed.path.split('.')[0].split('/')[-1]
        return f"""
            <div id="{post['name']}" class="col-sm-3 col-lg-3 col-xxl-3">
                <video controls poster="//i.imgur.com/{imgur_id}.jpg" preload="auto" autoplay="autoplay" muted="muted" loop="loop" webkit-playsinline="" style="width: 100%; height: 100%;">
                    <source src="//i.imgur.com/{imgur_id}.mp4" type="video/mp4">
                </video>
            </div>
        """
    elif 'imgur' in post['url']:
        imgur_id = parsed.path.split('.')[0].split('/')[-1]
        return f"""
            <div id="{post['name']}" class="col-sm-3 col-lg-3 col-xxl-3">
                <img class="" style="width: 100%;" src="//i.imgur.com/{imgur_id}.jpg">
            </div>
        """
    elif 'redgif' in post['url']:
        return ""
        redgifs_id = parsed.path.split('.')[0].split('/')[-1]
        return f"""
            <div id="{post['name']}" class="col-sm-3 col-lg-3 col-xxl-3">
                <div style='position:relative; padding-bottom:88.67%;'>
                    <iframe src='https://redgifs.com/ifr/{redgifs_id}' frameborder='0' scrolling='no' width='100%' height='100%' style='position:absolute;top:0;left:0;' allowfullscreen></iframe>
                </div>
            </div>
        """
    elif 'gfycat' in post['url']:
        return ""
    else:
        thumbnail = post.get('thumbnail', '/favicon.ico')
        thumbnail = thumbnail if thumbnail != '' else '/favicon.ico'
        return f"""
            <div id="{post['name']}" class="col-sm-3 col-lg-3 col-xxl-3">
                <a href="{post['url']}"><img class="" style="width: 100%;" src="{thumbnail}">
            </div>
        """
    return ""