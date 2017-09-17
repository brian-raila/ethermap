from ethereum.utils import privtoaddr, encode_hex
from ethermap.database import *
from ethereum.tools import keys
from passlib.hash import pbkdf2_sha256
import random, json, os, ast 
 
def keystore_to_address(json_keystore, password):	
	address = privtoaddr(keys.decode_keystore_json(json_keystore, password))
	address = encode_hex(address)
	return address


class Wallet:
	
	def __init__(self, exists=False, wallet_id=None, pseudo_name=None):
		self.seed = str(os.urandom(64))
		if exists is True:
			if wallet_id:
				self.ready_wallet = self.load_wallet(wallet_id=wallet_id)
			elif pseudo_name:
				self.ready_wallet = self.load_wallet(wallet_id=None, pseudo_name=pseudo_name)
			else:
				self.ready_wallet = None
			if self.ready_wallet:
				self.json_keystore = ast.literal_eval(ready_wallet.json_keystore)
				self.wallet_id = ready_wallet.wallet_id
				self.password_hash = ready_wallet.password_hash
				self.wallet_pseudo = ready_wallet.wallet_pseudo
				self.public_address = ready_wallet.public_address
		else:
			pass

	def create_new(self, pseudo_name=None, password=None):
	#Both are required to create a coinbase/wallet to store Ether
		if pseudo_name and password:
			self.wallet_id = str(random.random())[2:]
			self.json_keystore = keys.make_keystore_json(keys.sha3(self.seed), password)

			self.public_address = keystore_to_address(self.json_keystore, password)
			self.password_hash = pbkdf2_sha256.encrypt(password)
			self.pseudo_name = pseudo_name
			#Save this information on SQLite
			try:
				self.__query = coinbase.insert().values(wallet_id=self.wallet_id, json_keystore=str(self.json_keystore), password_hash=self.password_hash,
				wallet_pseudo=self.pseudo_name, public_address=self.public_address)
				db.execute(self.__query)
				return json.dumps({"Success" : "Account {} successfully created".format(self.pseudo_name)})

			except Exception as e:
				return json.dumps({"Error": str(e)})
		elif not pseudo_name:
			return json.dumps({"Error":"Please provide a pseudo name for your wallet. It is required."})
		elif not password:
			return json.dumps({"Error": "Please provide a password to secure your wallet"})
		else:
			return json.dumps({"Error":"An unknown error occured. Please try again"})

	def export_wallet(self, password, wallet_id=None, pseudo_name=None):
		if wallet_id and pseudo_name is None:
			return json.dumps({"No wallet identifier was passed. A wallet or pseudo name is required"})

		elif wallet_id:
			wallet = session.query(coinbase).filter_by(wallet_id=wallet_id).one()
			if pbkdf2_sha256.verify(password, wallet.password_hash) is True:
				private_key = keys.decode_keystore_json(ast.literal_eval(wallet.json_keystore), password)
				private_key = str(encode_hex(private_key))
				return json.dumps({"Success" : "Private Key : {}".format(private_key)})	
			#If the provided password was incorrect
			else: 
				return json.dumps({"Error":"Incorrect password provided"})
		elif pseudo_name:
			wallet = session.query(coinbase).filter_by(wallet_pseudo=pseudo_name).one()
			if pbkdf2_sha256.verify(password, wallet.password_hash) is True:
				private_key = keys.decode_keystore_json(ast.literal_eval(wallet.json_keystore), password)
				private_key = encode_hex(private_key)
				return json.dumps({"Success" : "Private Key : {}".format(private_key)})	
			#If the provided password was incorrect
			else: 
				return json.dumps({"Error":"Incorrect password provided"})
		else:
			return json.dumps({"Error":"Unknown error. Please try again"})


	def load_wallet(self, wallet_id=None, pseudo_name=None):
		if wallet_id:
			wallet = session.query(coinbase).filter_by(wallet_id=wallet_id).one()
			return wallet
		elif pseudo_name:
			wallet = session.query(coinbase).filter_by(wallet_pseudo=pseudo_name).one()
			return wallet
		else:
			return -99 #Error
			
			


