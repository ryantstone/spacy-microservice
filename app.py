from displacy_service.server import APP, get_model

# Pre-load English model only, to save memory
# get_model('/Users/sharkmaul/Dropbox (Personal)/prodigy/models/0.4/')
get_model('./model')
# get_model('de')


if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('0.0.0.0', 8080, APP)
    httpd.serve_forever()

