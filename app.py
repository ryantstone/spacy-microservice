import os
from dotenv import load_dotenv
from displacy_service.server import APP, get_model

get_model('./model')

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('0.0.0.0', 8080, APP)
    httpd.serve_forever()

