
import platform, sys, hashlib, json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from json.decoder import JSONDecodeError

import sinbad


def handle_response(resp):
    '''Handle a response (string, probably JSON format) from the server'''
    if not resp: return
    
    try:
        obj = json.loads(resp)
        print(obj)
    except JSONDecodeError:
        pass  # it's ok... probably just an "OK" string
   

def register_install():
    os_info = platform.uname().system + "/" + platform.uname().release
    lang_info = 'python {}.{}.{} {}'.format(*sys.version_info[0:4])
    
    url = 'http://cs.berry.edu/sinbad/service.php' # Set destination URL here
    post_fields = {'type' : 'install',
                   'version' : sinbad.__version__,
                   'token' : hashlib.md5(sinbad.__version__.encode()).hexdigest(),
                   'os' : os_info,
                   'lang' : lang_info,
                   'first_use_ts' : sinbad.util.current_time()
                   }
    
    #print(post_fields)
    request = Request(url, urlencode(post_fields).encode())
    result = None
    try:
        result = urlopen(request, None, 3)
    except OSError:
        pass   # allow to timeout/fail silently 
    
    if result: handle_response(result.read().decode())
        
    