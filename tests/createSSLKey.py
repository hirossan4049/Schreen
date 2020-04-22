""" HOW TO CREATE SSL KEY
$openssl genrsa -out secret.key 2048

$openssl req -new -sha256 -key secret.key -out server.csr

Country Name (2 letter code) []:jp
State or Province Name (full name) []:fafa
Locality Name (eg, city) []:afafa
Organization Name (eg, company) []:faf
Organizational Unit Name (eg, section) []:ff
Common Name (eg, fully qualified host name) []:ff
Email Address []:ff

A challenge password []:


$echo "subjectAltName = IP:192.168.0.102" > san.txt                                              

$openssl x509 -req -sha256 -days 3650 -signkey secret.key -in server.csr -out server.crt -extfile san.txt
"""


import pexpect
#import subprocess


sslkeyspath = "/Users/unkonow/Documents/pg/python/nowProject/schreen/Schreen/tests/sslkeys"
# Forced overwrite (矯正上書き)
fo = False
ip = "192.168.0.102"


class OpenSSLNotFoundError(Exception):
    pass

def getOpenSSLVersion():
    getversion = pexpect.run("openssl version")
    if getversion.split()[0] == "LibreSSL":
        return getversion
    if getversion.split()[0] == "OpenSSL":
        return getversion
    else:
        raise OpenSSLNotFoundError("OpenSSL Not Found.")


retn = pexpect.run("openssl genrsa -out {path}/secret.key 2048".format(path=sslkeyspath)).decode("utf-8")

if retn.split("\r")[0] == "Generating RSA private key, 2048 bit long modulus":
    print("OK!!")
else:
    print("ERROR!:",str(retn))

newkeyCommand = pexpect.spawn("openssl req -new -sha256 -key {path}/secret.key -out {path}/server.csr".format(path=sslkeyspath))
#print(newkeyCommand)
newkeyCommand.sendline('jp')
newkeyCommand.sendline("name")
newkeyCommand.sendline("city")
newkeyCommand.sendline("company")
newkeyCommand.sendline("section")
newkeyCommand.sendline("host name")
newkeyCommand.sendline("email")
newkeyCommand.sendline("\n")
newkeyCommand.interact()  


with open("{path}/san.txt".format(path=sslkeyspath),"w") as h:
    h.write("subjectAltName = IP:{ip}".format(ip=ip))


retn = pexpect.run("openssl x509 -req -sha256 -days 3650 -signkey {path}/secret.key -in {path}/server.csr -out {path}/server.crt -extfile {path}/san.txt".format(path=sslkeyspath)).decode("utf-8")
if retn.split("\r")[0] == "Signature ok":
    print("OK!")
else:
    print("ERROR:",retn)
