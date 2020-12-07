import requests
import json
import colorama as color
import termcolor as colors
color.init()


def status():
    
    """ Checks the status of the API """
    
    url = 'https://api.whatsonchain.com/v1/bsv/main/woc'
    
    response = requests.get(url)
    status_url = response.status_code
       
    if status_url == 200:
        print(colors.colored("Connection with API - OK", "green"))
    else:
        while True:
            print(colors.colored("No connection to API", "red"))
            input()
            
def data():

    """ Retrieves the current data """

    url_2 = 'https://api.whatsonchain.com/v1/bsv/main/chain/info'
    
    response_2 = requests.get(url_2)
    data_2 = response_2.json()
    blocks = data_2['blocks']
    
    print("\n- The last block:", blocks)

    return blocks

 
def data_block(blocks):

    """ Gets information about the last block """

    url = 'https://api.whatsonchain.com/v1/bsv/main/block/height/' + str(block)
    response = requests.get(url)
    data = response.json()

    list_tx = []
    
    miner = data['miner']
    size = data['size']
    txcount = data['txcount']
    totalFees = data['totalFees']
    tx = data['tx']
    for t in tx:
        list_tx.append(t)
    how_hash = data['hash']
    starter = 2
    MB = size / 1048576
    megabajt = round(MB, 2)
    l_tx = txcount
    print("- Block size:", megabajt, "Mb")
    print("- The number of transactions in the block:", l_tx)
    print("- Miner:", miner)
    print("- Hash bloku", how_hash)
    if l_tx > 1000:
        url_2 = 'https://api.whatsonchain.com/v1/bsv/main/block/hash/' + str(how_hash) + '/page/1'
        response_2 = requests.get(url_2)
        status_url_2 = response_2.status_code
        if status_url_2 == 200:
            input("You can expand the list.. (enter)")
            data_2 = response_2.json()
            for i in data_2:
                list_tx.append(i)
            while len(list_tx) > l_tx:
                url_3 = 'https://api.whatsonchain.com/v1/bsv/main/block/hash/' + str(how_hash) + '/page/' + str(starter)
                response_3 = requests.get(url_3)
                data_3 = response_3.json()
                for index in data_3:
                    list_tx.append(index)
                    starter+=1
        
    print("Downloaded transactions:", len(list_tx), "/ Total transactions:", l_tx)
    return list_tx
  

def get_hash(list_tx):

    """ Delisting list_tx """
    n_o = 1
    for i in list_tx:
        url = 'https://api.whatsonchain.com/v1/bsv/main/tx/hash/' + str(i)
        response = requests.get(url)
        data = response.json()
        vout = data['vout']
        try:
            vout_x = vout[0]
            scriptPubKey = vout_x['scriptPubKey']
            opReturn = scriptPubKey['opReturn']
            types = opReturn['type']
            parts = opReturn['parts']
            if parts[0] != "":
                print("[", n_o, "] [", types, "]", parts)
                n_o+=1
        except:
            pass

        
status() # <-- OK
block = data() # <-- OK
list_tx = data_block(block) # <-- OK
get_hash(list_tx) # <-- OK

input("End..")





