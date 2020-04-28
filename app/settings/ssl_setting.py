import pexpect
import timeout_decorator



class OpenSSLNotFoundError(Exception):
    pass
def getOpenSSLVersion():
    getversion = pexpect.run("openssl version").decode("utf-8")
    whatSSL = getversion.split(" ")[0]
    
    if whatSSL == "LibreSSL":
        return getversion
    elif whatSSL == "OpenSSL":
        return getversion
    else:
        raise OpenSSLNotfoundError("OpenSSL Not Found")


                                   
class CreateSSLKey:
    def __init__(self,path,ip,country="JP",province="Osaka",locality="Sakai",email="unko@unko.com"):
        self.path = path
        self.ip = ip

        self.country = country
        self.province = province
        self.locality = locality
        self.organization = "Schreen"
        self.email = email



    # TODO:パスがあるか確認
    def check_path(self):
        pass

    def _createSecrtKey(self):
        retn = pexpect.run("openssl genrsa -out {path}/secret.key 2048".format(path=self.path)).decode("utf-8")
        if retn.split("\r")[0] == "Generating RSA private key, 2048 bit long modulus":
            print("OK!!")
        else:
            print("ERROR!:",str(retn))
 
    def _createcsr(self):
        newkeyCommand = pexpect.spawn("openssl req -new -sha256 -key {path}/secret.key -out {path}/server.csr".format(path=self.path))
        #print(newkeyCommand)
        # TODO:self DE
        #newKeyCommand.expect("^(?=.*Country).*$")
        # お国
        newkeyCommand.sendline(self.country)
        newkeyCommand.sendline(self.province)
        newkeyCommand.sendline(self.locality)
        newkeyCommand.sendline(self.organization)
        newkeyCommand.sendline(self.organization)
        newkeyCommand.sendline(self.organization)
        newkeyCommand.sendline(self.email)
        newkeyCommand.sendline("\n")
        newkeyCommand.interact()  
        

    def _createSan(self):
        with open("{path}/san.txt".format(path=self.path),"w") as h:
            h.write("subjectAltName = IP:{ip}".format(ip=self.ip))

    def _createCrt(self):
        retn = pexpect.run("openssl x509 -req -sha256 -days 3650 -signkey {path}/secret.key -in {path}/server.csr -out {path}/server.crt -extfile {path}/san.txt".format(path=self.path)).decode("utf-8")
        if retn.split("\r")[0] == "Signature ok":
            print("OK!")
        else:
            print("ERROR:",retn)
                
    @timeout_decorator.timeout(5,use_signals=False)
    def start(self):
        # Check Openssl
        try:
            getOpenSSLVersion()
        except OpenSSLNotFoundError:
            return "OPENSSL NOT FOUND"

        print("START CreateSertKey")
        self._createSecrtKey()
        print("DONE! CreateSertKey")
        print("START CSR")
        self._createcsr()
        print("DONE! CSR")
        self._createSan()
        print("DONE! SAN")
        self._createCrt()
        print("DONE! CRT")
        print("Done!")


#csk = CreateSSLKey()
#csk.start()

        

