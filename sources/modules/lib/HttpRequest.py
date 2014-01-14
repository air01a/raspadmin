import json
import requests

class JsonHttpRequest:

        def __init__(self):
                self._post={}
                self._posttmp={}

        def add_post_var(self,varname,varvalue, tmp=False, jsonencode=False):
                if jsonencode:
                        varvalue=json.dumps(varvalue)

                if tmp:
                        self._posttmp[varname]=varvalue
                else:
                        self._post[varname]=varvalue

        def add_post_vars(self,vars,tmp=False,jsonencode=False):
                for key in vars.keys():
                        self.add_post_var(key,vars[key],tmp,jsonencode)


        def request(self,url):
                data=dict(self._post.items() + self._posttmp.items())
                rs = requests.post(url,data=data)
                del self._posttmp
                self._posttmp={}

                print rs.status_code
                return rs



def main():
	pass
if __name__ == '__main__':
	main()

