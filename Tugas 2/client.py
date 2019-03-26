import socket
import select

UDP_IP = "127.0.0.1"
IN_PORT = 5005
timeout = 5


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, IN_PORT))

while True:
    data, addr = sock.recvfrom(9216)
    data1 = data[:7] + "out.jpg" 
    print("ini adalah "+data1)
    if data1:
        print "nama file:", data1
        file_name = data1

    f = open(file_name, 'wb')

    while True:
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            data1, addr = sock.recvfrom(9216)
            f.write(data1)
        else:
            print "%s Selesai" % file_name
            f.close()
            break

