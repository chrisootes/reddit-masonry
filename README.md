# Reddit Masonry
* Path endpoints are the same as reddit.com: http://localhost/r/subredditname?after=t3_id
* Uses https://masonry.desandro.com/ for ordering posts into grid
* Uses https://getbootstrap.com/ for theming
* Uses https://jquery.com/ for infinite scroll
* Needs ASGI like uvicorn: pip install uvicorn
* Needs following pip packages, see requirements.txt
    * requests
    * demoji
    * aiofiles
* Create config.py from config.py.example and edit reddit login details
* Run start.sh for an uvicorn enviroment

## Screenshots
![Fullscreen](https://github.com/chrisootes/reddit-masonry/blob/29cfe1f4565bd2e24668c208e43cdd83bf4a97cc/screenshots/fullscreen.png "Fullscreen")
![Halfscreen](https://github.com/chrisootes/reddit-masonry/blob/29cfe1f4565bd2e24668c208e43cdd83bf4a97cc/screenshots/halfscreen.png "Halfscreen")
![Mobile](https://github.com/chrisootes/reddit-masonry/blob/29cfe1f4565bd2e24668c208e43cdd83bf4a97cc/screenshots/mobile.png "Mobile")

## TODO
* async reddit api