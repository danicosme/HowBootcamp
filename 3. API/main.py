#%%
import requests
import json
import backoff
import random
#%%
url = 'https://economia.awesomeapi.com.br/last/USD-BRL'
ret = requests.get(url)

#%%
if ret:
    print(ret.text)
else:
    print('Falhou')

#%%
dolar = json.loads(ret.text)['USDBRL']

#%%
print(f'20 dólares hoje custam {float(dolar["bid"])*20} reais.')




#%%
def cotacao(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print(f'{valor} {moeda[:3]} hoje custam {float(dolar["bid"])* valor} {moeda[-3:]}.')


#%%
cotacao(20, 'USD-BRL')

#%%
try:
    cotacao(20, 'USD-BRL')
except Exception as e:
    print(e)
else:
    print('ok')

#%%


#%%
#Decorador 
def error_check(func):
    def inner_func(*args, **kargs):
        try:
            func(*args, **kargs)
        except:
            print(f'{func.__name__} falhou')
    return inner_func

@error_check
def multi_moedas(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print(f'{valor} {moeda[:3]} hoje custam {float(dolar["bid"])* valor} {moeda[-3:]}.')


multi_moedas(20, 'USD-BRL')
multi_moedas(20, 'EUR-BRL')
multi_moedas(20, 'BTC-BRL')
multi_moedas(20, 'RPL-BRL')
multi_moedas(20, 'JPY-BRL')


#%%


#%%
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries = 10)
def test_func(*args, **kargs):
    rnd = random.random()
    print(f"""
            RND:{rnd}
            args: {args if args else 'sem args'}
            kargs: {kargs if kargs else 'sem kagrs'}
    """)
    if rnd < .2:
        raise ConnectionAbortedError('Conexão finalizada')
    elif rnd < .4:
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        raise TimeoutError('Tempo de esperada excedido')
    else:
        return 'Ok!'
# %%
test_func()
#%%
test_func(42, 51, nome = 'Daniele')

#%%
# Logs
import logging

#%%
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)


#%%
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries = 10)
def test_func(*args, **kargs):
    rnd = random.random()
    log.debug(f'RND:{rnd}')
    log.info(f'args: {args if args else "sem args"}')
    log.info(f'kargs: {kargs if kargs else "sem kagrs"}')
    if rnd < .2:
        log.error('Conexão finalizada')
        raise ConnectionAbortedError('Conexão finalizada')
    elif rnd < .4:
        log.error('Conexão foi recusada')
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        log.error('Tempo de esperada excedido')
        raise TimeoutError('Tempo de esperada excedido')
    else:
        return 'Ok!'


#%%
test_func()


#%%
