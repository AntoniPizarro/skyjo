def check_logging(logging):
    fields = {'name', 'password'}

    if len(logging) < 2:
        return False
    
    for field in fields:
        if field not in logging:
            return False
    
    return True