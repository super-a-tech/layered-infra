 import time
  import redis
  from flask import Flask

  app = Flask(__name__)
  # Connect to our Redis container.
  # "redis" is the name of the service in docker-compose.yml.
  cache = redis.Redis(host='redis', port=6379)

  def get_hit_count():
      retries = 5
      while True:
          try:
              # Increment the 'hits' counter in Redis by 1.
              # The 'incr' command is atomic.
              return cache.incr('hits')
          except redis.exceptions.ConnectionError as exc:
              if retries == 0:
                  raise exc
              retries -= 1
              time.sleep(0.5)

  @app.route('/')
  def hello():
      count = get_hit_count()
      return f'Hello! This page has been visited {count} times.\n'

  if __name__ == "__main__":
      # Listen on all network interfaces, not just localhost
      app.run(host="0.0.0.0", port=5000, debug=True)
requirements.txt - These are the Python libraries needed.

  flask
  redis
