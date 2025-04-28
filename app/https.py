from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta, timezone
from pathlib import Path
from app.logger import logger
from app.config import Config

cert_file: Path = None
key_file: Path = None

COUNTRY_NAME = "US"
ORGANIZATION_NAME = "DCS Retribution"
COMMON_NAME = "localhost"

def check_cert():
    """
    Check if the SSL certificate and key files exist and are not expired.
    ---
    Returns:
        bool: True if the certificate is valid, False otherwise.
    """
    if cert_file.exists() and key_file.exists():
        try:
            with open(cert_file, "rb") as f:
                cert = x509.load_pem_x509_certificate(f.read(), default_backend())
                if cert.not_valid_after_utc < datetime.now(timezone.utc):
                    logger.warning("SSL certificate expired. A new one will be generated.")
                    return False
        except Exception as e:
            logger.error(f"Error loading certificate: {e}")
            return False
        return True
    return False

def generate_cert():
    """
    Generate a new self-signed SSL certificate and key.
    """
    cert_dir.mkdir(parents=True, exist_ok=True)

    # Generate a private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Create a self-signed certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, COUNTRY_NAME),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, ORGANIZATION_NAME),
        x509.NameAttribute(NameOID.COMMON_NAME, COMMON_NAME),
    ])

    cert = x509.CertificateBuilder() \
        .subject_name(subject) \
        .issuer_name(issuer) \
        .public_key(private_key.public_key()) \
        .serial_number(x509.random_serial_number()) \
        .not_valid_before(datetime.now()) \
        .not_valid_after(datetime.now() + timedelta(days=365)) \
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName("localhost")]),
            critical=False,
        ).sign(private_key, hashes.SHA256(), default_backend())
    
    # Save the private key and certificate to files
    with open(key_file, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=NoEncryption()
        ))
    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(Encoding.PEM))

    logger.info("Self-signed SSL certificate and key generated successfully.")

if Config.get("app.https"):
    cert_dir = Path("data")
    cert_file = cert_dir / "cert.pem"
    key_file = cert_dir / "key.pem"

    # Check if the certificate and key files exist and are not expired
    if check_cert():
        logger.info("HTTPS enabled. cert.pem and key.pem are valid.")
    else:
        generate_cert()
        logger.info("HTTPS enabled.")

