import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

nets = dict(
    craftcoin=math.Object(
        P2P_PREFIX='fcd9b7dd'.decode('hex'),
        P2P_PORT=12124,
        ADDRESS_VERSION=57,
        RPC_PORT=12123,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'craftcoin address' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 2*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s targetspacing
        SYMBOL='CRC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'craftcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/craftcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.craftcoin'), 'craftcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://crc.cryptocoinexplorer.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://crc.cryptocoinexplorer.com/address/',
        TX_EXPLORER_URL_PREFIX='http://crc.cryptocoinexplorer.com/tx/',
        SANE_TARGET_RANGE=(2**256//100000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
    ),
    casinocoin=math.Object(
        P2P_PREFIX='fac3b6da'.decode('hex'),
        P2P_PORT=47950,
        ADDRESS_VERSION=28,
        RPC_PORT=47970,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'casinocoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*10000000 >> (height + 1)//3153600,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=30, # s targetspacing
        SYMBOL='CSC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'casinocoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/casinocoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.casinocoin'), 'casinocoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://casinocoin.mooo.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://casinocoin.mooo.com/address/',
        TX_EXPLORER_URL_PREFIX='http://casinocoin.mooo.com/tx/',
        SANE_TARGET_RANGE=(2**256//100000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
    ),
    catcoin=math.Object(
        P2P_PREFIX='fcc1b7dc'.decode('hex'),
        P2P_PORT=9933,
        ADDRESS_VERSION=21,
        RPC_PORT=9902,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'catcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='CAT',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'CatCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Catcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.catcoin'), 'catcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://catchain.info/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://catchain.info/address/',
        TX_EXPLORER_URL_PREFIX='http://catchain.info/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    dogecoin=math.Object(
        P2P_PREFIX='c0c0c0c0'.decode('hex'),
        P2P_PORT=22556,
        ADDRESS_VERSION=30,
        RPC_PORT=22555,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'dogecoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 10000*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='DOGE',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'DogeCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Dogecoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.dogecoin'), 'dogecoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://dogechain.info/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://dogechain.info/address/',
        TX_EXPLORER_URL_PREFIX='http://dogechain.info/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    usde=math.Object(
        P2P_PREFIX='d9d9f9bd'.decode('hex'), #pchmessagestart
        P2P_PORT=54447,
        ADDRESS_VERSION=38, #pubkey_address
        RPC_PORT=54448,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'usdeaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 1000*100000000 if height>1000 else 100*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='USDe',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'usde') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/usde/') if platform.system() == 'Darwin' else os.path.expanduser('~/.usde'), 'usde.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://usdeexplorer.com/block/', #dummy
        ADDRESS_EXPLORER_URL_PREFIX='http://usdeexplorer.com/address/',
        TX_EXPLORER_URL_PREFIX='http://usdeexplorer.com/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    worldcoin=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=11081,
        ADDRESS_VERSION=73,
        RPC_PORT=11082,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'worldcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 64*10000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=30, # s targetspacing
        SYMBOL='WDC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'worldcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/worldcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.worldcoin'), 'worldcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://wdc.cryptocoinexplorer.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://wdc.cryptocoinexplorer.com/address/',
        TX_EXPLORER_URL_PREFIX='http://wdc.cryptocoinexplorer.com/tx/',
        SANE_TARGET_RANGE=(2**256//100000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
    ),
    litecoin=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=9335,
        ADDRESS_VERSION=48,
        RPC_PORT=9334,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'litecoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//840000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=150, # s
        SYMBOL='LTC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Litecoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Litecoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.litecoin'), 'litecoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.litecoin.net/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.litecoin.net/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.litecoin.net/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    digitalcoin=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=7999,
        ADDRESS_VERSION=30,
        RPC_PORT=7998,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'digitalcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 15*10000000 >> (height + 1)//4730400,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=40, # s targetspacing
        SYMBOL='DGC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'digitalcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/digitalcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.digitalcoin'), 'digitalcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://dgc.cryptocoinexplorer.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://dgc.cryptocoinexplorer.com/address/',
        TX_EXPLORER_URL_PREFIX='http://dgc.cryptocoinexplorer.com/tx/',
        SANE_TARGET_RANGE=(2**256//100000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
    ),
    zetacoin=math.Object(
        P2P_PREFIX='fab503df'.decode('hex'), #chainparams.cpp pchMessageStart
        P2P_PORT=17333,
        ADDRESS_VERSION=80, #PUBKEY_ADDRESS
        RPC_PORT=17335,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'zetacoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 1000*100000000 >> (height + 1)//80640,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=30, # s
        SYMBOL='ZET',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Zetacoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Zetacoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.zetacoin'), 'zetacoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://bit.usr.sh:2750/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://bit.usr.sh:2750/address/',
        TX_EXPLORER_URL_PREFIX='http://bit.usr.sh:2750/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**32 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=1e8,
    ),
    joulecoin=math.Object(
        P2P_PREFIX='a5c07955'.decode('hex'),
        P2P_PORT=26789,
        ADDRESS_VERSION=43,
        RPC_PORT=8844,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'joulecoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 16*100000000 >> (height * 1)//1401600,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=45, # s
        SYMBOL='XJO',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'joulecoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/joulecoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.joulecoin'), 'joulecoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://xjo-explorer.cryptohaus.com:2750/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://xjo-explorer.cryptohaus.com:2750/address/',
        TX_EXPLORER_URL_PREFIX='http://xjo-explorer.cryptohaus.com:2750/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**32 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=1e8,
    ),
    bitcoin=math.Object(
        P2P_PREFIX='f9beb4d9'.decode('hex'),
        P2P_PORT=18333,
        ADDRESS_VERSION=0,
        RPC_PORT=8332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'bitcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//210000,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=600, # s
        SYMBOL='BTC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Bitcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Bitcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.bitcoin'), 'bitcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://blockchain.info/block/',
        ADDRESS_EXPLORER_URL_PREFIX='https://blockchain.info/address/',
        TX_EXPLORER_URL_PREFIX='https://blockchain.info/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**32 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),
    asiccoin=math.Object(
        P2P_PREFIX='fab5e8db'.decode('hex'),
        P2P_PORT=13434,
        ADDRESS_VERSION=22,
        RPC_PORT=13435,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'asiccoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height * 1)//210000,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=45, # s
        SYMBOL='ASC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'asiccoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/asiccoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.asiccoin'), 'asiccoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://bit.usr.sh:2750/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://bit.usr.sh:2750/address/',
        TX_EXPLORER_URL_PREFIX='http://bit.usr.sh:2750/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**32 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=1e8,
    ),
    franko=math.Object(
        P2P_PREFIX='7defaced'.decode('hex'),
        P2P_PORT=7912,
        ADDRESS_VERSION=35,
        RPC_PORT=7913,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'frankoaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 1*10000000 >> (height + 1)//1080000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=30, # s targetspacing
        SYMBOL='FRK',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'franko') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/franko/') if platform.system() == 'Darwin' else os.path.expanduser('~/.franko'), 'franko.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://frk.cryptocoinexplorer.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://frk.cryptocoinexplorer.com/address/',
        TX_EXPLORER_URL_PREFIX='http://frk.cryptocoinexplorer.com/tx/',
        SANE_TARGET_RANGE=(2**256//100000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
    ),
   ekrona=math.Object(
        P2P_PREFIX='dcc1c104'.decode('hex'), #pchmessagestart
        P2P_PORT=9445,
        ADDRESS_VERSION=45, #pubkey_address
        RPC_PORT=9444,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'ekronaaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 40*100000000 >> (height + 1)//500000 ,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=200, #seconds
        SYMBOL='KRN',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Ekrona') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/ekrona/') if platform.system() == 'Darwin' else os.path.expanduser('~/.ekrona'), 'ekrona.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://altexplorer.net/block/', #dummy
        ADDRESS_EXPLORER_URL_PREFIX='http://altexplorer.net/address/',
        TX_EXPLORER_URL_PREFIX='http://altexplorer.net/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    smartcoin=math.Object(
        P2P_PREFIX='defaced0'.decode('hex'), #pchmessagestart
        P2P_PORT=58584,
        ADDRESS_VERSION=63, #pubkey_address
        RPC_PORT=58583,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'smartcoin' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 64*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=40, # s
        SYMBOL='SMC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'smartcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/smartcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.smartcoin'), 'smartcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://altexplorer.net/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://altexplorer.net/address/',
        TX_EXPLORER_URL_PREFIX='http://altexplorer.net/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0,
    ),
    luckycoin=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=9917,
        ADDRESS_VERSION=47,
        RPC_PORT=9918,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'luckycoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 88*100000000 >> (height + 1)//1036800,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60,
        SYMBOL='LKY',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Luckycoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Luckycoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.luckycoin'), 'luckycoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.luckycoinfoundation.org:49917/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.luckycoinfoundation.org:49917/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.luckycoinfoundation.org:49917/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    Extremecoin=math.Object(
        P2P_PREFIX='fcd9b7dd'.decode('hex'),
        P2P_PORT=26665,
        ADDRESS_VERSION=55,
        RPC_PORT=26666,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'Extremecoin address' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 1*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=120, # s targetspacing
        SYMBOL='EXC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'extremecoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Extremecoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.Extremecoin'), 'Extremecoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://exc-blocks.pw/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://exc-blocks.pw/address/',
        TX_EXPLORER_URL_PREFIX='http://exc-blocks.pw/tx/',
        SANE_TARGET_RANGE=(2**256//100000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
    ),
    potcoin=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=4200,
        ADDRESS_VERSION=20,
        RPC_PORT=42000,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'potcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 420*100000000 >> (height + 1)//840000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=40, # s
        SYMBOL='POT',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'potcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/potcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.potcoin'), 'potcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://potchain.potcoin.info/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://potchain.potcoin.info/address/',
        TX_EXPLORER_URL_PREFIX='http://potchain.potcoin.info/transaction/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=1e8,
    ),
    tigercoin=math.Object(
        P2P_PREFIX='fab5dfdb'.decode('hex'),
        P2P_PORT=19971,
        ADDRESS_VERSION=127,
        RPC_PORT=15661,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue('tigercoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 128*100000000 >> (height + 1)//172800,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=45, # s
        SYMBOL='TGC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'tigercoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/tigercoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.tigercoin'), 'tigercoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://bit.usr.sh:2750/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://bit.usr.sh:2750/address/',
        TX_EXPLORER_URL_PREFIX='http://bit.usr.sh:2750/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**32 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),
    platinum=math.Object(
        P2P_PREFIX='28282828'.decode('hex'),
        P2P_PORT=10125,
        ADDRESS_VERSION=55,
        RPC_PORT=10126,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue('platinumaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 78*100000000 >> (height + 1)//259200,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=120, # s
        SYMBOL='PT',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'platinum') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/platinum/') if platform.system() == 'Darwin' else os.path.expanduser('~/.platinum'), 'platinum.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://platinumcrypto.com/block/index.php?block_hash=',
        ADDRESS_EXPLORER_URL_PREFIX='http://platinumcrypto.com/address/',
        TX_EXPLORER_URL_PREFIX='http://platinumcrypto.com/block/index.php?transaction=',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**32 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),

)
for net_name, net in nets.iteritems():
    net.NAME = net_name
