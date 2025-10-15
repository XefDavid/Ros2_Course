import rclpy
from rclpy.node import Node
from bumperbot_msgs.srv import AddTwoInts #importamos la estructura

class SimpleServiceServer (Node):
    def __init__(self):
        super().__init__("simple_service_server")

        self.service_ = self.create_service(AddTwoInts, "add_two_ints", self.serviceCallback)
        #Create_service() => Es una funcion de rosclass, que cera un servicio de servidor dentro de un nodo.
        #Se crea con la estructura, el nombre  y una funcion que maneja 

        self.get_logger().info("Service add_two_ints => Ready")#log para ver que funciona el flujo
    
    def serviceCallback(self, req, res):
        self.get_logger().info(f"New request received number a =>{req.a}, number b =>{req.b}")

        res.sum = req.a + req.b

        self.get_logger().info(f"Devolviendo resultado de la suma => {res.sum}")

        return res

def main():
    rclpy.init()
    simple_service_server = SimpleServiceServer()
    rclpy.spin(simple_service_server)
    simple_service_server.destroy_node()
    rclpy.shutdown()

if __name__=="__main__":
    main()