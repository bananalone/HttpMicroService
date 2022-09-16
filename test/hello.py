def hello(name):
    '''
    hello ${name}
    
    Args:
        name: str
    Return: str
    '''
    s = f'hello {name}'
    print(s)
    return s

def hello_json(name):
    '''
    hello json ${name}

    Args:
        name: str
    Return: dict
    '''
    return {
        'function': 'hello_json',
        'file': __file__,
        'name': name
    }
