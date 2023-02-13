from flask import Flask
from flask import request
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# Generating public and private keys.
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()


@app.route('/public-key', methods=['GET'])
def get_public_key():
    return public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                   format=serialization.PublicFormat.SubjectPublicKeyInfo)


@app.route('/', methods=['POST'])
def verify():
    # Deserializing the data
    data = request.json
    signature = bytes.fromhex(data['signature'])
    sender_public_key = load_pem_public_key(str.encode(data['public_key']))
    encrypted_message = bytes.fromhex(data['encrypted_message'])

    try:
        # Verifies the signature.
        sender_public_key.verify(signature,
                                 encrypted_message,
                                 padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                                 hashes.SHA256())

    except InvalidSignature:
        print("Invalid signature!", flush=True)
        return '', 400

    else:
        # Decrypts the message, only after sucessfully verifying the signature.
        message = private_key.decrypt(encrypted_message, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )).decode('utf8')

        print(message, flush=True)

        return '', 200
