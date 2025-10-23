import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class odomSubscriber(Node):
    def __init__(self):
        super().__init__("odom_susbcriber")

        self.subscription = self.create_subscription( Odometry,"/bumperbot_controller/odom",self.odom_callback,10)
        self.get_logger().info("Conecectado a /bumperbot_controller/odom")
        
    
    def odom_callback(self,msg):
        #importante!! odometry de ros2 no tiene msg.data....
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y        
        self.get_logger().info(f"Mensaje recibido de Odometria:\n x:{x} \n y:{y}")

def main():
    rclpy.init()
    odom_subscriber = odomSubscriber()
    rclpy.spin(odom_subscriber)
    odom_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()