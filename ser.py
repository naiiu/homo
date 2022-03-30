#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import tenseal as ts


zcontext = zmq.Context()
socket = zcontext.socket(zmq.REP)
socket.bind("tcp://*:5555")


def gencontext():
    context = ts.context(ts.SCHEME_TYPE.CKKS, 8192, coeff_mod_bit_sizes=[22 ,21, 21, 21, 21, 21, 21, 21, 21, 21])
    context.global_scale = pow(2, 21)
    context.generate_galois_keys()
    return context

def encrypt(context, np_tensor):
    return ts.ckks_tensor(context, np_tensor)

def decrypt(enc_tensor):
    return np.array(enc_tensor.decrypt().tolist())

def bootstrap(context, tensor):
    # To refresh a tensor with exhausted depth. 
    # Here, bootstrap = enc(dec())
    tmp = decrypt(tensor)
    return encrypt(context, tmp)

while True:
    #  Wait for next request from client
    [context, a,b, c_context] = socket.recv_multipart()
    # print(type(message))
    context = ts.context_from(context)
    c_context = ts.context_from(c_context)
    a = ts.ckks_vector_from(context, a)
    b = ts.ckks_vector_from(context, b)
    # print(type(received))
    print(a)
    print(b)
    #  Do some 'work'
    # tmp = a+b;
    # print(tmp)
    # result = ts.ckks_vector_from(context, tmp.serialize()).decrypt()
    # print(result)

    
    #  Send reply back to client
    socket.send(a.serialize())