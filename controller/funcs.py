from hashids import Hashids
from models import URL, db
from flask import request
from sqlalchemy.exc import InvalidRequestError
from functools import wraps

## HASH FUNCS ##
hashids = Hashids(min_length=5, salt="thisisasecretkey")


def create_hashid(id):
    hashid = hashids.encode(id)
    return hashid


def decode_hashid(hashid):
    id = hashids.decode(hashid)
    return id

###############


def startswith_http(f):
    """
    if the url doesnt start with 'http://' or 'https://' then "redirect(TARGETURL)" 
    will be useless. so we change our url with this decorator and go to the target url succesfully.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if f(*args, **kwargs) != False:
            url = f(*args, **kwargs)
            if url.startswith("http://") or url.startswith("https://"):
                return url
            else:
                return f"http://{url}"
        else:
            return f(*args, **kwargs)
    return decorated_function
  

@startswith_http
def get_original_url(hashid):
    """
    To go to the "/<id>" endpoint. We need check this hashed id in database
    we decode and convert it to real id and we get the target url 
    Returns:
        TARGET URL
    """
    try:
        original_url = URL()
        real_id = decode_hashid(hashid=hashid)
        url = original_url.get_url_with_id(real_id)
        return url
    except InvalidRequestError:
        return False
    
@startswith_http
def url_checker(form_url):
    return form_url

def short_url(form_url):
    """_summary_
    Firstly we create a new object to check if it exists in the database 
    If there is, we get the id of the row it is in.
    otherwise we add it to the database first and then get its id
    Returns:
        TARGET URL
    """
    new_url = URL()
    url = url_checker(form_url)
    url = new_url.get_row(url)
    if url:        
        short_url = request.host_url + create_hashid(url.id)
        return short_url
    else:
        checked_url = url_checker(form_url)
        new_url.add_url(checked_url)
        url = new_url.get_row(checked_url)
        short_url = request.host_url + create_hashid(url.id)
        return short_url
    
    
def click_counter(original_url):
    url = URL()
    target_url = url.get_row(original_url)
    target_url.click = target_url.click + 1
    db.session.commit()
    
    
def show_stats():
    urls = URL.query.order_by(URL.click).all()
    return urls[::-1]
    
  
    
def qr_code_url(form_url):
    return f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={form_url}"
        