import OpenSSL
import os
import settings
import time

cert_dir = os.path.join(settings.app_dir, 'certs')
hope_ca_file_path = os.path.join(cert_dir, 'hopeca.crt')


def setup_certs():
    if not os.path.exists(cert_dir):
        os.mkdir(cert_dir)

    if not os.path.isfile(hope_ca_file_path):
        create_hope_ca_file()


def setup_domain_cert(domain):
    if not os.path.isfile(get_domain_cert_file_path(domain)):
        create_domain_cert_file(domain)


def get_domain_cert_file_path(domain):
    return os.path.join(cert_dir, domain+'.crt')


def create_hope_ca_file():
        key = OpenSSL.crypto.PKey()
        key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
        req = OpenSSL.crypto.X509Req()
        subj = req.get_subject()
        subj.countryName = 'CN'
        subj.stateOrProvinceName = 'SH'
        subj.localityName = 'SH'
        subj.organizationName = 'Hope'
        subj.organizationalUnitName = 'Hope'
        subj.commonName = 'Hope root Certificate'
        req.set_pubkey(key)
        req.sign(key, 'sha256')
        ca = OpenSSL.crypto.X509()
        ca.set_serial_number(0)
        ca.gmtime_adj_notBefore(0)
        ca.gmtime_adj_notAfter(3600 * 24 * 365 * 10)
        ca.set_issuer(req.get_subject())
        ca.set_subject(req.get_subject())
        ca.set_pubkey(req.get_pubkey())
        ca.sign(key, 'sha256')
        with open(hope_ca_file_path, 'wb') as fp:
            fp.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, ca))
            fp.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key))


def create_domain_cert_file(domain=None):
    if not domain:
        return

    with open(hope_ca_file_path, 'rb') as fp:
        content = fp.read()
        key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, content)
        ca = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, content)

    pkey = OpenSSL.crypto.PKey()
    pkey.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

    req = OpenSSL.crypto.X509Req()
    subj = req.get_subject()
    subj.countryName = 'CN'
    subj.stateOrProvinceName = 'SH'
    subj.localityName = 'SH'
    subj.organizationalUnitName = 'Hope'
    subj.organizationName = 'Hope'
    subj.organizationalUnitName = 'Hope'
    subj.commonName = domain
    req.set_pubkey(pkey)
    req.sign(pkey, 'sha256')

    cert = OpenSSL.crypto.X509()
    cert.set_version(2)
    cert.set_serial_number(int(time.time()*1000))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(3600 * 24 * 365 * 10)
    cert.set_issuer(ca.get_subject())
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(key, 'sha256')

    with open(get_domain_cert_file_path(domain), 'wb') as fp:
        fp.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
        fp.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, pkey))


if __name__ == '__main__':
    setup_certs()
    setup_domain_cert("www.google.com.hk")
