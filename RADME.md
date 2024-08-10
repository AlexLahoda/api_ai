1.before start app :
    1.1.install all libraries from requirements.txt
    1.2.downolad and start redis-server.exe
    1.3 in terminal run celery -A api_ai worker -l info -P eventlet
2. in another terminal run python manage.py runserver
3. Functions:
    - create user: post request to 'api/user/' body: {'username': 'yourusername', 'email': 'youremail', 'password': 'yourpassword'}
    - get token: post request to 'api/token/', body: {'username': 'yourusername', 'password': 'yourpassword'}
    - create post: post request to 'api/post/', body: {'title': 'posttitle', 'content': 'postcontent'} headers:{'Authorization': 'Token yourtoken'}
    - create comment: post request to 'api/comment/', body: {'post_id': 'post_id', 'content': 'commentcontent'} headers: {'Authorization': 'Token yourtoken'}
    - get post: get request to 'api/post/{post_id}/'
    - get comment: get request to 'api/comment/{comment_id}/'
    - get all posts: get request to 'api/post/'
    - get all comments: get request to 'api/comment/'
    - get daily-brakedown: get request to 'api/comments-daily-brakedown?date_from={your_date}&date_to={your_date}'
4. To test:
    4.1. start redis-server.exe
    4.2. run python manage.py test
