import hashlib

#return md5, sha1 of tuple
class hash_get:
	def get_hash(self,file_name):
		f = open(file_name,'rb').read()
		md5_ = hashlib.md5(f).hexdigest()
		sha_ = hashlib.sha1(f).hexdigest()
		#print '[+]md5 : ',md5_,'\r\n[+]SHA1 : ',sha_
		return (md5_, sha_)

#file_name = raw_input('input : ')
#hash_ = set()