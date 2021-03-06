#!python

import datetime
import urllib.parse
import logging
import mimetypes

import aiofiles

import config
import reddit
import helpers

logger = logging.getLogger(__name__)
session: reddit.Reddit = None

async def app(scope, receive, send):
    """
    Async app
    """
    try:
        #logger.debug(f"Scope: {scope}")

        if scope['type'] == 'lifespan':
            while True:
                message = await receive()
                # Handle startup event
                if message['type'] == 'lifespan.startup':
                    logger.info("Starting app")
                    global session
                    session = reddit.Reddit()
                    await send({'type': 'lifespan.startup.complete'})
                    return

                # Handle shudown event
                elif message['type'] == 'lifespan.shutdown':
                    logger.info("Stopping app")
                    await send({'type': 'lifespan.shutdown.complete'})
                    return

        if scope['type'] != 'http':
            raise Exception("Unkown scope type")

        # Parse path
        path_splitted = scope['path'].split('/')
        
        # Check for static files in path
        if len(path_splitted) >= 2:
            if path_splitted[1] == 'static' or path_splitted[1] == 'favicon.ico':
                static_file_path = '/'.join(path_splitted[1:])
                static_file_type = mimetypes.guess_type(static_file_path)
                logger.debug(f"Requested static file: {static_file_path} with type: {static_file_type}")
                try:
                    static_file = await aiofiles.open(static_file_path, mode='rb')
                except IOError as e:
                    logger.error(f"Requested static file: {static_file_path} with type: {static_file_type} not found")
                    # Send 404 header
                    await send({
                        'type': 'http.response.start',
                        'status': 404,
                    })
                else:
                    # Send header
                    await send({
                        'type': 'http.response.start',
                        'status': 200,
                        'headers': [
                            [b'content-type', static_file_type[0].encode('latin1')],
                        ],
                    })
                    # Send contents
                    contents = await static_file.read()
                    await send({
                        'type': 'http.response.body',
                        'body': contents,
                    })
                
                return

        # Check for subredit in path
        if len(path_splitted) <= 2:
            if path_splitted[1] == '':
                subreddit = 'front'
                generator_type = session.generator_front
            else:
                raise Exception(f"Invalid endpoint: {path_splitted}")
        elif len(path_splitted) == 3:
            if path_splitted[1] == 'r':
                if path_splitted[2] != '':
                    subreddit = path_splitted[2]
                    generator_type = session.generator_subredit
                else:
                    raise Exception("Empty subreddit given")
            elif path_splitted[1] == 'm':
                if path_splitted[2] != '':
                    subreddit = path_splitted[2]
                    generator_type = session.generator_multi
                else:
                    raise Exception("Empty multi given")
        else:
            raise Exception(f"To long endpoint: {path_splitted}")

        if subreddit == 'undefined':
            raise Exception("Page was previously not completly loaded")
        
        # TODO if subredit does not exist 404
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'text/html'],
            ],
        })
            
        # Parse query
        query_string = scope['query_string'].decode('utf-8')
        logger.debug(f"POST query: query_string={query_string}")
        query = urllib.parse.parse_qs(query_string)

        # Check for raw in query
        raw = query.get('raw', [False])[0]
        logger.debug(f"POST query: raw={raw}")

        # Check for after in query
        after = query.get('after', [''])[0]
        logger.debug(f"POST query: after={after}")

        # Check for order in query
        order = query.get('order', ['hot'])[0]
        logger.debug(f"POST query: order={order}")

        # Check for background in query
        background = query.get('background', [False])[0]
        logger.debug(f"POST query: background={background}")

        # Check for check in query
        check = query.get('check', [False])[0]
        logger.debug(f"POST query: check={check}")

        # With background dont put the images and video in a card
        format_post = helpers.format_post
        if background:
            format_post = helpers.format_post_background
        
        # Raw only gives post html no thing more
        if raw:
            logger.debug(f"Items only for subreddit: {subreddit}")
            posts = generator_type(subreddit=subreddit, order=order, start_after=after)
            for post in posts:
                after = post['name']
                if session.check(post) or not check:
                    await send({
                        'type': 'http.response.body',
                        'body': format_post(post).encode('utf-8'),
                        'more_body': True
                    })

            # End more body
            await send({
                'type': 'http.response.body',
                'body': b'',
                'more_body': False
            })
            return
        
        # Load different templete for background
        template_filename = 'template_page.html'
        if background:
            template_filename = 'template_background.html'
        template = await aiofiles.open(template_filename, mode='r')
        # Loop template
        while True:
            line = await template.readline()
            # Chek for end file
            if line == '':
                break
            # Check for template item
            elif '$' in line:
                splitted = line.split('$')
                #logger.debug(f"Splitted template: {splitted}")
                # Send everythin before first $
                await send({
                    'type': 'http.response.body',
                    'body': splitted[0].encode('utf-8'),
                    'more_body': True
                })
                # Send between
        
                # Template key: date
                if splitted[1] == 'date':
                    await send({
                        'type': 'http.response.body',
                        'body': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode('utf-8'),
                        'more_body': True
                    })

                # Template key: page
                elif splitted[1] == 'page':
                    # Build next url with all options in query string so next page has also the options like order and check
                    next_url = f"{scope['path']}?after={after}&{query_string}"
                    logger.debug(f"next_url: {next_url}")
                    await send({
                        'type': 'http.response.body',
                        'body': next_url.encode('utf-8'),
                        'more_body': True
                    })

                # Template key: items
                elif splitted[1] == 'items':
                    logger.debug(f"Getting {subreddit} on page {after}")
                    posts = generator_type(subreddit=subreddit, order=order, start_after=after)
                    for post in posts:
                        # Used in template key: page
                        after = post['name']
                        if session.check(post) or not check:
                            await send({
                                'type': 'http.response.body',
                                'body': format_post(post).encode('utf-8'),
                                'more_body': True
                            })

                # Send everythin after second $
                await send({
                    'type': 'http.response.body',
                    'body': splitted[2].encode('utf-8'),
                    'more_body': True
                })

            # Everything else is static content
            else:
                await send({
                    'type': 'http.response.body',
                    'body': line.encode('utf-8'),
                    'more_body': True
                })

        # End more body
        await send({
            'type': 'http.response.body',
            'body': b'',
            'more_body': False
        })
    except:
        logger.exception("Catched exception")
        # TODO send something else


