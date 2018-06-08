import jwt
import datetime
import logging
import json

LOG = logging.getLogger()


class APIJwt:

    _public_dummy = '-----BEGIN PUBLIC KEY-----\n' \
                    'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzkoXUA7qFoRC/f49OB6Q\n'\
                    'm0K5jdmKkYIsM/USD8lqGsiH7ixMQSoqr7H0RxqILdOHtvHe/QHSG+nqz6Vko6Qc\n'\
                    'fgcI3LIhYiC1munfJXYZkaZ0yUgTjUHy2WIXRCtWNwav9YKpHpe5C7aeSb8+eohw\n'\
                    '8gfbcwjKTZ8XjHx7mfz7THDqRBZ1UI97V8R7LOFqPAvuDlD3uZfesJHCB6Dpo6Yy\n'\
                    'DDc8LEev8FolxYVnG4fQZNFhONHciuCIxeZ5qnzPqGOykVHPByzVs/J9QXANMgCW\n'\
                    'D9yVapYwRaYKxMg9lqmRJdPSQ6AMByKBGgN+jxNfokvx2zV7yPKfD/fQ/k/q1FId\n'\
                    'NQIDAQAB\n'\
                    '-----END PUBLIC KEY-----'
    _private_dummy = '-----BEGIN RSA PRIVATE KEY-----\n'\
                     'MIIEpAIBAAKCAQEAzkoXUA7qFoRC/f49OB6Qm0K5jdmKkYIsM/USD8lqGsiH7ixM\n'\
                     'QSoqr7H0RxqILdOHtvHe/QHSG+nqz6Vko6QcfgcI3LIhYiC1munfJXYZkaZ0yUgT\n'\
                     'jUHy2WIXRCtWNwav9YKpHpe5C7aeSb8+eohw8gfbcwjKTZ8XjHx7mfz7THDqRBZ1\n'\
                     'UI97V8R7LOFqPAvuDlD3uZfesJHCB6Dpo6YyDDc8LEev8FolxYVnG4fQZNFhONHc\n'\
                     'iuCIxeZ5qnzPqGOykVHPByzVs/J9QXANMgCWD9yVapYwRaYKxMg9lqmRJdPSQ6AM\n'\
                     'ByKBGgN+jxNfokvx2zV7yPKfD/fQ/k/q1FIdNQIDAQABAoIBAH8bPeQRXIFFO3X+\n'\
                     '+j+i7Z0M7wINIYlouM3G2jsp8pvQJZlGaDHaxnR9ZLOPEIuUA9Jgk/I29fxHFGyf\n'\
                     'TzRZQUkSEo7Rnyo0V1G9esY9T6Hj+5+uLoXiNb1l6EoTncrH7xGKUaRM/jLOchek\n'\
                     'o92iRl2LI9dseiJ7vWnNpecK7th4uwvJuvtgWuvLfRA/4OzpuaOKPfh942u7vCUc\n'\
                     'hJ529blYFZe6yyUvTa/u/PeArKMPrhOPjuqdb8JNGFCXWwVmron/uDssHvOcPyPX\n'\
                     'DgYCQELMY8bDBfthBuLZ1nkp6rCfWOqHy8CR1Rq9waQrOKXFltw4dHPi+wGTdeux\n'\
                     'znkFqX0CgYEA8QQsKd2hha1PUGc3S2uO5DOlf+zr7ofxkMeK1FfHiJjylnc3fivx\n'\
                     'cKx5pVH4NOFnvT94Z0nlZnFlaikrJKVMXhTgW0kEKevK5ys8cM5ils2DAFlbRzPS\n'\
                     'U1QPXw9CvqEW0zLiHo/xTQFsjT2UkWHTAbsEkPhetT2KlvK/laB59C8CgYEA2x07\n'\
                     'i3C6QHjsdeRSwmWV8X7l9doMkswuNPXBpCdC27vyXAeKCUhXA60FXGavK+mUc3l0\n'\
                     '1Fcy+Jd7rKDPWnTExqOlTWhoMXRP3QoFn8sImJUcBv7dkusFrWltT8k/rrcc1DKc\n'\
                     'Jfl/0RltZY/fJmQ9MH/Y+EcmtTS7bDjkzqBSF9sCgYAWKEULIEX+LR2yjZqmw1+i\n'\
                     'mSDo7tYN2s+ZeM7JkLxWUYFT1efzIIUUz7ZrPWrtKZ/I5THjhQai8V/ab6h4uP2Z\n'\
                     'VJ//pGnOlM/VisMGt+KWbJRTjuN2W0xFvt+e5J9FOTgI+I+TMbaEVtIs9fFXoD+u\n'\
                     '1AuqbDsAvISmNfDpB5TOnwKBgQCc1KOV/q2RD/xPtYj20zcrjySRf+yX9cTs6yoa\n'\
                     'kG9uT2v9KvhGBJ0jaGf55xViXOGAdWKFyZQWEnbW7JL9r65YbzEV4rERFKtFDrNP\n'\
                     '2Ebiz3csGqgFTGrX4Cn5fZYzO6VKzJ6vH5G43HZMx1l1ZTHW0Os/ac3uzTuJDn/W\n'\
                     '1TFtGQKBgQDn0bRpR4sMDQ8h7ur6TDpx7O9wQjLr/OeJBtAbFIfg6HOhe8VzsuMA\n'\
                     'b0lxZ6BD2YESDeKDjGpcjlGKuGux54VK9NFSerQNXOQ3Sp9uWziJFoKabVLZsKg2\n'\
                     'udYzRAT6QGEB4Xc9AagL6ua20pYqLpAjdmRuhtLf+ddMp0OQudd5Ng==\n'\
                     '-----END RSA PRIVATE KEY-----'

    def __init__(self, public_keys=None, private_key=None, ttl=None, **kwargs):
        self._allowed = {
            'keys': {
                'user': 'auth_user',
                'admin': 'auth_admin'
            },
            'levels': [
                0.0,  # Level 0, no authentication
                1.0,  # External auth
                2.0,  # Password/single-factor
                3.0,  # Multi-factor
                4.0  # Certificate-level
            ],
            'dnt': [
                0,  # or not set - normal user
                1,  # reservation - don't track this user
                2,  # not anonymous - don't track and don't store data anonymously
                3   # Test user - this is a test user, don't skew metrics
            ],
            'scopes': {
                'PER_KEY': {  # Use single key with 'PER_KEY' to set allowed values based on key
                    'user': ['user:all'],
                    'admin': ['admin:all']
                }
            }
        }
        # Use None as default to prune item from jwt final token
        self._jwt_extras = {
            'level': 0.0,  # Authentication level, see _levels for valid levels
            'factor': '',  # Authentication factor used, e.g. password, otp, etc
            'target': '',  # Target id for scopes
            'dnt': None,   # Do Not Track
            'scopes': [],  # Scopes allowed for this token
        }

        self._ttl = 3600
        self._public_keys = [self._public_dummy]
        self._private_key = self._private_dummy
        self.override_keys(public_keys=public_keys, private_key=private_key)
        if ttl:
            self._ttl = ttl
        self._valid = False
        self._expired = True
        self._jwt_issue = False
        self._token = None
        self._user = {
            'id': '',  # entity id
            'exp': datetime.datetime.utcnow(),  # Expiry time for the token
        }

        # Init extra jwt payload parameters
        for k, v in self._jwt_extras.items():
            if v:
                self._user[k] = v
        for k, v in kwargs.items():
            if k == 'extras':
                for a, p in v.items():
                    self.set_extras(a, p)
            if k == 'allowed':
                for a, p in v.items():
                    self.set_allowed(a, p)

    def reset_keys(self):
        """
        Reset back the keys to the dummy keys
        :return:
        """
        self._public_keys = [self._public_dummy]
        self._private_key = self._private_dummy

    def override_keys(self, public_keys=None, private_key=None):
        """
        Override the keys 'on the fly'. Preferred method is at instantiation
        :param public_keys: list or json list of keys, or single public key for decoding
        :param private_key: private key for encoding
        :return:
        """
        if public_keys:
            if isinstance(public_keys, list):
                self._public_keys = public_keys
            else:
                try:
                    self._public_keys = json.loads(public_keys)
                except (ValueError, TypeError, NameError):
                    self._public_keys = [public_keys]
        if private_key:
            self._private_key = private_key

    def add_public_keys(self, keys=None):
        """
        Add more public keys
        :param keys: Single or list of keys (no json allowed)
        """
        if keys is None:
            keys = []
        for k in keys:
            self._public_keys.append(k)

    def set_extras(self, key, default):
        """
        Set extra allowed payload parameters
        :param key: Payload name
        :param default: Default value, None if it should be pruned from jwt if not set
        """
        self._jwt_extras[key] = default

    def set_allowed(self, key, values):
        """
        Set allowed values for the extras in the payload
        :param key: Payload name
        :param values: Dict for keys and scopes, list for other extras
        """
        self._allowed[key] = values

    def _add_extras(self, key, **kwargs):
        """
        Returns a dict with validate extra payload elements
        :param key:
        :param kwargs:
        :return:
        """
        payload = {}
        for k, v in kwargs.items():
            if k not in self._jwt_extras:
                LOG.warning('%s is not an allowed extra', k)
                raise AttributeError('Payload element is not an allowed extra in payload')
            if k in self._allowed:
                if isinstance(self._allowed[k], dict) and \
                        'PER_KEY' not in self._allowed[k] and \
                        v not in self._allowed[k]:
                    LOG.warning('%s is not an allowed value for key %s', str(v), str(k))
                    raise ValueError('Value is not allowed in key')
                elif 'PER_KEY' in self._allowed[k] or isinstance(self._allowed[k], list):
                    if 'PER_KEY' in self._allowed[k]:
                        allow = self._allowed[k]['PER_KEY'][key]  # Use key to find correct allow values
                    else:
                        allow = self._allowed[k]
                    if not isinstance(v, list):
                        if isinstance(v, str):
                            v = [v]
                        else:
                            LOG.warning("Mismatch in value, list required for key %s", k)
                            raise ValueError('Invalid value, a list is expected')
                    for i in v:
                        if i not in allow:
                            LOG.warning("Found list value in key %s that is not in allowed values", k)
                            raise ValueError('Found an illegal value in the key, i.e. not in allowed')
                elif not isinstance(v, type(self._allowed[k])):
                    LOG.warning("Mismatch in type for key %s, %s is allowed value", k, str(type(self._allowed[key])))
                    raise ValueError('Mismatch between allowed value type and type for supplied value')
            # If key was not in _allowed, any value is allowed unless None
            if v is not None:
                payload[k] = v
        return payload

    def encode(self, subject=None, key='user', exp=None, **kwargs):  # noqa
        """
        Encode the token
        :param subject: id of identity that is the origin of this token
        :param key: a valid key from _allowed['keys'], typically used in iss to match key on external system
        :param exp: expiry time in seconds
        :param kwargs: extras={} or allowed={} as short-cuts to set_allowed() and set_extras
        :return: None if not successful or resulting JWT token
        """
        if key not in self._allowed['keys']:
            self._valid = False
            self._jwt_issue = True
            LOG.warning('key %s is not a valid key name', key)
            return None
        if subject is None:
            LOG.warning('subject is not set in token encode')
            raise ValueError('Subject is not set in token encode')
        if exp is None:
            exp = self._ttl
        exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=exp)
        # Initialise payload
        payload = {
            'iss': self._allowed['keys'][key],
            'sub': subject,
            'exp':  exp,
        }
        # Add default extras to payload
        for k, v in self._jwt_extras.items():
            if v is not None:
                payload[k] = v
        # Add passed in extras to payload
        if kwargs:
            payload.update(self._add_extras(key, **kwargs))
        # Serialize any list, float, int items into strings
        for k, v in payload.items():
            if isinstance(v, list):
                value = ''
                if v:
                    for s in v:
                        value += (',' if value else '')
                        value += s
                payload[k] = value
            elif isinstance(v, (float, int)):
                payload[k] = str(v)
        # Encode the payload and get token
        if self._private_key == self._private_dummy:
            LOG.warning('WARNING!!! Encoding JWT with dummy key!')
        try:
            self._token = jwt.encode(
                payload,
                self._private_key,
                algorithm='RS256'
            )
        except jwt.InvalidTokenError:
            self._token = None
            self._valid = False
            self._jwt_issue = True
            LOG.error('Not able to encode token')
            raise EnvironmentError("Not able to encode token, may be bad private key")
        self._valid = True
        self._expired = False
        self._jwt_issue = False
        for k, v in payload.items():
            self._user[k] = v
        self._user['id'] = subject
        self._user['exp'] = exp

        return self._token

    def decode(self, token=None):
        """
        Decode a token, check is_valid, is_bad, an is_expired to get details on results.
        All tokens are verified against the list of public keysl
        :param token: JWT token to decode
        :return: Either None or a dict with the payload
        """
        if token is None:
            self._valid = False
            LOG.error('Cannot decode empty token.')
            return None
        self._token = token
        payload = None
        for key in self._public_keys:
            self._valid = True
            self._expired = False
            self._jwt_issue = False
            payload = None
            if key == self._public_dummy:
                LOG.warning('WARNING!!! Decoding JWT with dummy key!')
            try:
                payload = jwt.decode(
                    token,
                    key,
                    algorithm='RS256'
                )
                break
            except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError):
                self._valid = False
                LOG.info('Invalid signature.')
                continue
            except jwt.exceptions.ExpiredSignatureError:
                self._valid = False
                self._expired = True
                LOG.info('Token has expired.')
                return None
            except jwt.InvalidTokenError:
                self._jwt_issue = True
                self._valid = False
                self._expired = False
                LOG.info('Invalid token, unspecified.')
                return None
            except jwt.PyJWTError:
                self._jwt_issue = True
                self._valid = False
                self._expired = False
                LOG.info('Invalid token, unspecified.')
                return None
        if not payload or payload.get('sub', None) is None:
            self._valid = False
            self._jwt_issue = True
            LOG.info('No payload or sub in payload.')
            return None
        for k, v in self._jwt_extras.items():
            if isinstance(v, list):
                if payload.get(k, None):
                    self._user[k] = payload[k].split(',')
            elif payload.get(k, None):
                self._user[k] = payload[k]
        self._user['exp'] = datetime.datetime.utcfromtimestamp(payload.get('exp', None))
        if self._user['exp'] is None:
            self._expired = True
            LOG.info('No exp in payload.')
            return None
        self._user['level'] = float(payload.get('level', 0.0))
        self._user['factor'] = payload.get('factor', '')
        self._user['id'] = payload.get('sub')
        return self._user

    @property
    def user(self):
        return self._user

    @property
    def jwt(self):
        return self._token

    @property
    def is_valid(self):
        return self._valid

    @property
    def is_expired(self):
        # It may have been expired when we decoded
        if self._expired:
            return self._expired
        # Update to see if it has expired by now
        if 'exp' not in self._user:
            self._expired = True
        else:
            self._expired = (self._user['exp'] < datetime.datetime.utcnow())
        return self._expired

    @property
    def is_bad(self):
        return self._jwt_issue

    @property
    def expiry(self):
        return self._user['exp']

    def __getattr__(self, key):
        try:
            return self._user[key]
        except KeyError:
            raise AttributeError(key)
