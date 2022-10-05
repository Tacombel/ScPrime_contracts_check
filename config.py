class Config(object):
    # Thias is for scprime running inside a container. If you host it directly, check line 11 and adapt it to your command.
    # Also, for a single host, remove the for loop at line 64.
    hosts = ['scprime01'] # This is the name of the container
    base_cmd = 'docker exec'
