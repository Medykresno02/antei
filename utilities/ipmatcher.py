from .REGEX import re
from .REGEX import three_digit_of_ip


def matchForSetIP(ip):
    return bool(ip.count('.') ==3 and '.'.join(list(filter(bool, three_digit_of_ip.findall(ip.lower())))[:4]) == ip and filter(lambda x:x.count('x')>1,ip.split('.')))

def match(listip, ip):
    """
For Example:
    match(['192.168.43.x','192.168.x.1', 'x.x.x.x'], '192.68.43.1')
    """
    for i in listip:
        res=re.search(i.replace("x","[0-9]{,3}"), ip)
        if res and res.group(0) == ip:
            return True
    else:
        return False
