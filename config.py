mcfg_url= "http://sd.testin.cn/mcfg/mcfg.action"
apikey=""
secret_key=""
email=""
password=""
try:
    from local_config import *
except ImportError, e:
    if e.args[0].startswith('No module named local_config'):
        pass
    else:
        # the ImportError is raised inside local_config
        raise