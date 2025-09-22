#Script que se subscribe a los 
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimpleSubscriber(Node): #Creamao un nodo nuevo

    def __init__(self):#inicializamos el constructor y se ejecuta automaticamente
        super().__init__("simple_subscriber") #Damos el nombre al nodo

        self.sub = self.create_subscription(String, "Disparos", self.msgCallback, 10)#creamos el caal de subscripcions
        self.sub = self.create_subscription(String , "Sonidos", self.msgCallback, 10)
    
    def msgCallback(self, msg):
        self.get_logger().info("i heard: %s" %msg.data)


def main():
    rclpy.init()
    simple_subcriber= SimpleSubscriber()
    rclpy.spin(simple_subcriber)
    simple_subcriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()