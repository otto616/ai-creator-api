from slowapi import Limiter
from slowapi.util import get_remote_address

# Init the limiter using the IP of the user as id
limiter = Limiter(key_func=get_remote_address)