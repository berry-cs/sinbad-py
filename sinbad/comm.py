
import platform, sys, hashlib, json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from json.decoder import JSONDecodeError

import sinbad
from sinbad import prefs


HOLD_TIME = 1    # number of seconds that we will wait to get a response back from the server


def handle_response(resp):
    '''Handle a response (string, probably JSON format) from the server'''
    if not resp: return
    
    try:
        obj = json.loads(resp)
        #print(obj)
    except JSONDecodeError:
        pass  # it's ok... probably just an "OK" string
   
   
def register_load(usage_info):  # full_url, format_type, status, sample_amt, sample_seed, data_options):
    os_info = platform.uname().system + "/" + platform.uname().release
    lang_info = 'python {}.{}.{} {}'.format(*sys.version_info[0:4])
    url = prefs.get_pref("server_base") + 'service.php'
   
    post_fields = {'type' : 'usage',
                   'version'    : sinbad.__version__,
                   'token'      : hashlib.md5(sinbad.__version__.encode()).hexdigest(),
                   'os'         : os_info,
                   'lang'       : lang_info,
                   'usage_type' : 'load',
                   'full_url'   : usage_info.get('full_url'),
                   'format'     : usage_info.get('format_type'),
                   'status'     : usage_info.get('status'),
                   'file_entry' : usage_info.get('file_entry'),
                   'sample_amt' : usage_info.get('sample_amt'),
                   'sample_seed' : usage_info.get('sample_seed'),
                   'data_options' : usage_info.get('data_options'),                   
                   }
    
    #print(post_fields)
    request = Request(url, urlencode(post_fields).encode())
    result = None
    try:
        result = urlopen(request, None, HOLD_TIME)
    except OSError:
        pass   # allow to timeout/fail silently 
    
    if result: handle_response(result.read().decode())
    
        
        
def register_install():
    os_info = platform.uname().system + "/" + platform.uname().release
    lang_info = 'python {}.{}.{} {}'.format(*sys.version_info[0:4])

    url = prefs.get_pref("server_base") + 'service.php'
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
        result = urlopen(request, None, HOLD_TIME)
    except OSError:
        pass   # allow to timeout/fail silently 
    
    if result: handle_response(result.read().decode())
        
    