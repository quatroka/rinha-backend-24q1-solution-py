wsgi_app = 'main:app'
bind = '0.0.0.0:3000'
workers = 2
# accesslog = '-'  # stdout
# errorlog = '-'  # stdout
worker_class = 'uvicorn.workers.UvicornWorker'
