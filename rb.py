import hashlib, base58, binascii, ecdsa, codecs
import pandas as pd
import sys
import time
from os import system
import numpy as np

data = pd.read_csv('Bitcoin_addresses_LATEST.txt', sep=" ", header=None)
data.columns = ["address"]

datanp = data['address'].to_numpy()

alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def sha256(arg) :
    ''' Return a sha256 hash of a hex string '''
    byte_array = bytearray.fromhex(arg)
    m = hashlib.sha256()
    m.update(byte_array)
    return m.hexdigest()

def b58encode(hex_string) :
    ''' Return a base58 encoded string from hex string '''
    num = int(hex_string, 16)
    encode = ""
    base_count = len(alphabet)
    while (num > 0) :
            num, res = divmod(num,base_count)
            encode = alphabet[res] + encode
    return encode

def privToWif(priv, verbose=False) :
    ''' Produce a WIF from a private key in the form of an hex string '''
    # 1 - Take a private key
    _priv = priv.lower() # just for aesthetics
    if verbose : print("Private key: "+_priv)
    # 2 - Add a 0x80 byte in front of it
    priv_add_x80 = "80" + _priv
    if verbose : print("Private with x80 at beginning: "+priv_add_x80)
    # 3 - Perform SHA-256 hash on the extended key 
    first_sha256 = sha256(priv_add_x80)
    if verbose : print("sha256: " + first_sha256.upper())
    # 4 - Perform SHA-256 hash on result of SHA-256 hash 
    seconf_sha256 = sha256(first_sha256)
    if verbose : print("sha256: " + seconf_sha256.upper())
    # 5 - Take the first 4 bytes of the second SHA-256 hash, this is the checksum 
    first_4_bytes = seconf_sha256[0:8]
    if verbose : print("First 4 bytes: " + first_4_bytes)
    # 6 - Add the 4 checksum bytes from point 5 at the end of the extended key from point 2 
    resulting_hex = priv_add_x80 + first_4_bytes
    if verbose : print("Resulting WIF in HEX: " + resulting_hex)
    # 7 - Convert the result from a byte string into a base58 string using Base58Check encoding. This is the Wallet Import Format 
    result_wif = b58encode(resulting_hex)
    if verbose : print("Resulting WIF: " + result_wif)
    return result_wif

def f(datanp=datanp):
    c = 0
    while True:
        #start_time = time.time()
        # Step1: Generate ECDSA Private Key")
        ecdsaPrivateKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        #print("ECDSA Private Key: ", ecdsaPrivateKey.to_string().hex())
        #print("------------------------------------------------------")
        # Step2: Generate ECDSA Public Key from value at Step#1
        ecdsaPublicKey = '04' +  ecdsaPrivateKey.get_verifying_key().to_string().hex()
        #print("ECDSA Public Key: ", ecdsaPublicKey)
        #print("------------------------------------------------------")
        # Step3: SHA256(value at Step#2)
        hash256FromECDSAPublicKey = hashlib.sha256(binascii.unhexlify(ecdsaPublicKey)).hexdigest()
        #print("SHA256(ECDSA Public Key): ", hash256FromECDSAPublicKey)
        #print("------------------------------------------------------")
        # Step4: RIDEMP160(value at Step#3)
        ridemp160FromHash256 = hashlib.new('ripemd160', binascii.unhexlify(hash256FromECDSAPublicKey))
        #print("RIDEMP160(SHA256(ECDSA Public Key)): ", ridemp160FromHash256.hexdigest())
        #print("------------------------------------------------------")
        # Step5: Prepend 00 as network byte to value at Step#4
        prependNetworkByte = '00' + ridemp160FromHash256.hexdigest()
        #print("Prepend Network Byte to RIDEMP160(SHA256(ECDSA Public Key)): ", prependNetworkByte)
        #print("------------------------------------------------------")
        # Step6: Apply SHA256 to value at Step#5 at 2 times to generate Checksum
        hash = prependNetworkByte
        for x in range(1,3):
            hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()
            #print("\t|___>SHA256 #", x, " : ", hash)
        #print("------------------------------------------------------")
        # Step7: Get first 4 bytes of value at Step#6 as Checksum
        cheksum = hash[:8]
        #print("Checksum(first 4 bytes): ", cheksum)
        #print("------------------------------------------------------")
        # Step8: Append Checksum to value at Step#5
        appendChecksum = prependNetworkByte + cheksum
        #print("Append Checksum to RIDEMP160(SHA256(ECDSA Public Key)): ", appendChecksum)
        #print("------------------------------------------------------")
        # Step9: Generate Bitcoin Address with apply Base58 Encoding to value at Step#8
        bitcoinAddress = base58.b58encode(binascii.unhexlify(appendChecksum))
        
        #print("Bitcoin Address: ", bitcoinAddress.decode('utf8'))

        #print(datanp[datanp == bitcoinAddress.decode('utf8')])

        '''
        start_time = time.time()
        if datanp[datanp == '1111111111111111111114oLvT2']:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("Tempo decorrido: {:.2f} segundos".format(elapsed_time))

        start_time = time.time()
        if np.any(datanp == '1111111111111111111114oLvT2'):
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("Tempo decorrido: {:.2f} segundos".format(elapsed_time))

        input('press any')
        break
        '''
        #if True:
        if np.any(datanp == bitcoinAddress.decode('utf8')):
        #if datanp[datanp == bitcoinAddress.decode('utf8')]:
        #if datanp[datanp == '1111111111111111111114oLvT2']:
            with open(bitcoinAddress.decode('utf8'), 'a') as file:
                wi = "ECDSA Private Key: " + ecdsaPrivateKey.to_string().hex() + '\n' \
                + "ECDSA Public Key: " + ecdsaPublicKey + '\n' \
                + "Wif Priv Key: " + privToWif(ecdsaPrivateKey.to_string().hex()) + '\n' \
                + "Bitcoin Address: " + bitcoinAddress.decode('utf8')
                            
                file.write(wi)
            #break
        else:
            #system('cls')
            #print(bitcoinAddress.decode('utf8'))

            c += 1
            if c == 1:
                print(bitcoinAddress.decode('utf8'))
                #print('.')
            #elif c == 2:
            #    print('..')
            elif c == 100:
                #print('...')
                c = 0
                system('cls')

        #end_time = time.time()
        #elapsed_time = end_time - start_time
        #print("Tempo decorrido: {:.2f} segundos".format(elapsed_time))
        #print('Media de {:.1f} por minuto'.format(60/elapsed_time))


if __name__ == '__main__':  # name guard to avoid recursive fork on Windows
    #import multiprocessing as mp
    #n = 2 #mp.cpu_count()#mp.cpu_count() * 32  # multiply guard against counting only active cores
    #print(n)
    #with mp.Pool(n) as p:
    #    p.map(f, range(n))
    f()
