def _str_to_host(text):
    username, delim, hostname = text.rpartition('@')
    new_host = dict()

    if username:
        new_host['username'] = username

    if hostname:
        new_host['hostname'] = hostname

    return new_host

