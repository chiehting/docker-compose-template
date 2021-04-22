DATABASES = {
    'default': {
        'ATOMIC_REQUESTS': True,
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "awx",
        'USER': "awx",
        'PASSWORD': "awxpass",
        'HOST': "postgres",
        'PORT': "5432",
    }
}

BROADCAST_WEBSOCKET_SECRET = "YTl5eFdmZTBDTnliYUY5TklxaUluWC44LjppLDFza2EwUGt2V1JqRFBhLlhPNSwxZS5iWDI2NWhOOC0zWEplbEExWE54Wjo2c19HQUQtWExnOXZzVmprUmJYbUFFLlZzenU4b01Sb1A2eVlyTUt0OUdjNS4xYnVhc3czUl85ckg="
