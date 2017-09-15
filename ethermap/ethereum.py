from ethereum.utils import privtoaddr, encode_hex
from ethermap.database import *
from ethereum.tools import keys
from passlib.hash import pbkdf2_sha256
import random, json 

 
def keystore_to_address(json_keystore, password):	
	address = privtoaddr(keys.decode_keystore_json(json_keystore, password))
	address = encode_hex(address)
	return address


class Wallet:

	def __init__(self, exists=None, wallet_id=None, pseudo=None):

		self.hot_wallet = 

	def create_new(self, pseudo_name=None, password=None):
	#Both are required to create a coinbase/wallet to store Ether
		if wallet_pseudo and password:
			self.wallet_id = str(random.random()[2:])
			self.json_keystore = keys.make_keystore_json(keys.sha3(__seed), password)
			self.public_address = keystore_to_address(self.json_keystore, password)
			self.password_hash = pbkdf2_sha256.encrypt(password)
			self.pseudo_name = pseudo_name

		elif not pseudo_name:
			return json.dumps({"Error":"Please provide a pseudo name for your wallet. It is required."})
		elif not password:
			return json.dumps({"Error": "Please provide a password to secure your wallet"})
		else:
			return json.dumps({"Error":"An unknown error occured. Please try again"})

	def export_wallet(self, password, wallet_id=None, pseudo_name=None):
		if wallet_id is None:
			return json.dumps

	def load_wallet(self, wallet_id=None, pseudo_name=None):
		if wallet_id is not None:
			wallet = ses


