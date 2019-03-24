from concurrent import futures
import time
import logging
import threading
import grpc
import fluffy_pb2
import fluffy_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

IPList=[]
class RouteService(fluffy_pb2_grpc.RouteServiceServicer):

    def request(self, request, context):
    	print("Client Connected and sent a message: "+request.payload.decode("utf-8"))
    	return fluffy_pb2.Route(payload=bytes('Server receive the message',"utf-8"))



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fluffy_pb2_grpc.add_RouteServiceServicer_to_server(RouteService(), server)
    server.add_insecure_port('localhost:3000')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

def update_list():
    global IPList
    while True:
        with open('routingtable.txt') as f:
            for line in f:
                if line.find("expired")==-1 and line.find("(none)")==-1:
                    IPList.append(line.split()[0])
        IPList.pop(0)
        time.sleep(6)
        IPList.clear()
        
def client():
    global IPList
    print("client")
    print(IPList)
    while True:
        for ip in IPList:
            channel = grpc.insecure_channel(ip+':3000')
            payload="Sending Hello to server"
            stub = fluffy_pb2_grpc.RouteServiceStub(channel)
            response = stub.request(fluffy_pb2.Route(payload=bytes(payload, 'utf-8')))
            print(response.payload.decode("utf-8"))
        time.sleep(6)


if __name__ == '__main__':
    logging.basicConfig()
    t1= threading.Thread(target=update_list)
    t2 = threading.Thread(target=serve)
    time.sleep(1) 
    print("Server is started at localhost:3000")
    t3 = threading.Thread(target=client)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

#serve()
