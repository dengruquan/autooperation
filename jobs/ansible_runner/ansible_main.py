
from django.http import HttpResponseRedirect  

def test():
    return HttpResponseRedirect("/cmdb/asset.html")

if __name__ == "__main__":
    test()