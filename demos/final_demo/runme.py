#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
import sys
import zmq.green as zmq
import time
import math
import json
# Debugger
from werkzeug.serving import run_with_reloader
from multiprocessing import Process
from myhandkinect import Kinect

gevent.monkey.patch_all()


from flask import Flask, request, Response, render_template


app = Flask(__name__)
app.context = zmq.Context()

DIRECCION_PUBLICADOR = 'tcp://127.0.0.1:5555'

def kinect_simulator():
    myKinect = Kinect(DIRECCION_PUBLICADOR)
    return myKinect.kinect_loop()    

def generador_de_eventos():
    '''Una función que envía acutalizaciones usando el protocolo de
    eventos emitidos por el servidor (SSE). La directiva yield retorna
    un valor, pero la función conserva su estado ante cada llamada, por
    eso está rodeada de un while True'''
    sock = app.context.socket(zmq.SUB)
    sock.connect(DIRECCION_PUBLICADOR)
    sock.setsockopt(zmq.SUBSCRIBE, "")
    while True:
        data = sock.recv()
        print "Sending %s to client" % data
        # Yield retorna un valor pero guarda estado de una función
        yield 'data: %s\n\n' % data


@app.route('/events')
def sse_request():
    '''URL donde se publican los eventos'''
    return Response(generador_de_eventos(), mimetype='text/event-stream')

@app.route('/')
def index():
    return render_template('index.html')

@run_with_reloader
def main():
    '''Función mainl del programa'''
    p = Process(target=kinect_simulator)
    p.start()
    host, port = '0.0.0.0', 12345
    print "Running server at {host}:{port}".format(host=host, port=port)

    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()
    p.kill()

if __name__ == '__main__':
    sys.exit(main())
