class Cache:
  def __init__(self, connection):
    self.conn = connection

  def set(self, key, value):
    self.conn.set(key, value.encode('utf-8'))

  def get(self, key):
    return self.conn.get(key).decode('utf-8')
