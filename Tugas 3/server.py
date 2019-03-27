import threading
import socket
import os
import sys
import shutil

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 8080)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(1)

#download file
def response_download(param):
    url, filename = param.split('=')
    print filename
    file = open(filename, 'rb').read()
    panjang = len(file)
    hasil = "HTTP/1.1 200 OK\r\n" \
            "Content-Type:  multipart/form-data\r\n" \
            "Content-Length: {}\r\n" \
            "\r\n" \
            "{}".format(panjang, file)
    return hasil

#tambah folder
def response_tambahfolder(param):
    url, dirname = param.split('=')
    try:
        os.system('mkdir ' + dirname)
        hasil = "HTTP/1.1 200 OK\r\n" \
            "Content-Type: text/plain\r\n" \
            "Content-Length: 17\r\n" \
            "\r\n" \
            "folder ditambahkan "
    except:
        hasil = "HTTP/1.1 200 OK\r\n" \
                "Content-Type: text/plain\r\n" \
                "Content-Length: 23\r\n" \
                "\r\n" \
                "tidak bisa menambahkan folder "
    return hasil

#upload file
def uploader():
    file = open('page.html', 'r').read()
    panjang = len(file)
    hasil = "HTTP/1.1 200 OK\r\n" \
            "Content-Type: text/html\r\n" \
            "Content-Length: {}\r\n" \
            "\r\n" \
            "{}".format(panjang, file)
    return hasil

def post_receiver():
    request_message = ''
    while True:
        data = koneksi_client.recv(64)
        request_message = request_message+data

        if (len(data) < 64):
            #m.write(request_message)
            filename = request_message.split('filename="')
            filename = filename[1]
            index = filename.find('"')
            filename = filename[:index:]
            f = open(filename, "wb")
            request_message = request_message.split("Content-Type: ")
            request_message = request_message[2]
            print request_message[-60::]
            index = request_message.find("\r\n\r\n")
            request_message = request_message[index+4::]
            request_message = request_message.split("\n\r\n------WebKitForm")
            break
    f.write(request_message[0])
    f.close()

def layani_client(koneksi_client, alamat_client):
    try:
        print >> sys.stderr, 'ada koneksi dari', alamat_client
        request_message = ''
        while True:
            data = koneksi_client.recv(64)
            request_message = request_message + data
            if request_message.startswith("POST") :
                post_receiver()
                break
            if (request_message[-4:] == "\r\n\r\n"):
                break

        print request_message
        baris = request_message.split("\r\n")
        baris_request = baris[0]
        print baris_request

        a, url, c = baris_request.split(" ")

        if (url.startswith("/download")):
            respon = response_download(url)
        elif (url.startswith("/tambahfolder")):
            respon = response_tambahfolder(url)
        elif (url == '/upload'):
            respon = uploader()
        elif (url == '/submit') :
            respon = "HTTP/1.1 200 OK\r\n" \
            "Content-Type: text/plain\r\n" \
            "Content-Length: 13\r\n" \
            "\r\n" \
            "File terupload "
        elif (url == '/') :
            respon = "HTTP/1.1 200 OK\r\n" \
            "Content-Type: text/plain\r\n" \
            "Content-Length: 19\r\n" \
            "\r\n" \
            "Berhasil terhubung ke server"
        else:
            respon = "HTTP/1.1 200 OK\r\n" \
                     "Content-Type: text/plain\r\n" \
                     "Content-Length: 9\r\n" \
                     "\r\n" \
                     "Perintah tidak ditemukan"

        koneksi_client.send(respon)
    finally:
        koneksi_client.close()


while True:
    print >> sys.stderr, 'waiting for a connection'
    koneksi_client, alamat_client = sock.accept()
    s = threading.Thread(target=layani_client, args=(koneksi_client, alamat_client))
    s.start()