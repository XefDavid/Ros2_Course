import rclpy
from rclpy.node import Node
from bumperbot_msgs.srv import AddTwoInts #importamos la configuracion del srv
import sys

class SimpleServiceClient(Node):
    def __init__(self, a, b): #en este constructor no solo recibe self, tambien los dos argumentos a y b
        super().__init__("simple_service_client")

        #Instanciamos una variable en la que usamos la funcion de ros2 create_client,
        self.client_= self.create_client(AddTwoInts,"add_two_ints")

        #este cliente espera a que es sercio este disponible, que haya un servidor escuchando /add_two_ints
        #si esta disponible devuelve true  si no cada segundo prueba a ver si lo esta , hasta que se rompa el bucle...
        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service not available, waiting again ..")

        
        self.req_= AddTwoInts.Request() #esta linea prepara un formulario con los valores que queremos enviar
        self.req_.a = a
        self.req_.b = b

        self.future_ = self.client_.call_async(self.req_) #se crea una solicitus asyncrona para que siga el flujo de trabajo, por eso se alamacena en future, porque ahi es donde recibirá la respuesta
        self.future_.add_done_callback(self.responseCallback) #cuando la respuesta este lista llama a la funcion

    def responseCallback(self, future):  
        self.get_logger().info(f"service response {future.result().sum}") 

def main():
    rclpy.init()

    if len(sys.argv) != 3:
        print("wrong number of arguments!! Usage:simple service client A B")
        return -1
    
    simple_service_client = SimpleServiceClient(int(sys.argv[1]),int(sys.argv[2]))
    rclpy.spin(simple_service_client)
    simple_service_client.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()