from hashids import Hashids
from models import URL
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
        if f(*args, **kwargs).startswith("http://") or f(*args, **kwargs).startswith("https://"):
            return f(*args, **kwargs)
        else:
            return f"http://{f(*args, **kwargs)}"
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
    
    
def short_url(form_url):
    """_summary_
    Firstly we create a new object to check if it exists in the database 
    If there is, we get the id of the row it is in.
    otherwise we add it to the database first and then get its id
    Returns:
        TARGET URL
    """
    new_url = URL()
    url = new_url.get_row(form_url)
    if url:        
        short_url = request.host_url + create_hashid(url.id)
        return short_url
    else:
        new_url.add_url(form_url)
        url = new_url.get_row(form_url)
        short_url = request.host_url + create_hashid(url.id)
        return short_url
    
  
    
def qr_code_url(form_url):
    return f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={form_url}"
        