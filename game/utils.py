from hashlib import md5
# get md5 digest to send to the payment request
def get_checksum(message):
    return md5(message.encode("ascii")).hexdigest()
