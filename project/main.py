from pprint import pprint
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import sys
from . import db
from .ig_api.defines import getCreds
from .ig_api.business_discovery import getAccountPosts
from .chat import generateComment

main = Blueprint('main', __name__)
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, email = current_user.email)

@main.route('/signup')
def signup():
    return render_template('signup.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/logout')
def logout():
    return render_template('logout.html')

@main.route('/webhook', methods=['POST', 'GET'])
def webhook():
    print("Debug message here : 1", file=sys.stderr)

    if request.method == 'POST':
        print("POST", file=sys.stderr)
        return 'success', 200
    elif request.method == 'GET':
        print("GET", file=sys.stderr)
        # get IG account
        ig_account = request.args.get('ig_account')

        # take last post
        post_id = 0
        # if specific post requested
        if request.args.get('post_id'):
            # take specific post
            post_id = int(request.args.get('post_id'))

        params = getCreds()
        params['ig_username'] = ig_account
        response = getAccountPosts( params ) # hit the api for some data!
        # pprint(response['json_data'])
        # get specified post and its caption
        caption = response['json_data']['business_discovery']['media']['data'][post_id]['caption']
        caption_encode = caption.encode('ascii', 'ignore')
        caption = caption_encode.decode()
        comment = generateComment(params['ig_username'], caption)
        '''
        # For IG API webhook verification
        challenge = request.args.get('hub.challenge')
        if challenge == None:
            return '',200
        else:
            return challenge
        '''

        '''
        return {'ig_username' : params['ig_username'], 
                'post' : caption,
                'reply': comment}
        '''
        messages = {'ig_username' : params['ig_username'], 
                'post' : caption,
                'reply': comment}


        print(messages, file=sys.stderr)
        return render_template('reply.html', messages=messages)
    else:
        print("Debug message here : 2", file=sys.stderr)
        return '',200

