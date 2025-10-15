import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped


class SimpleTfKinematics (Node):
    #creamos el constructor con el nombre de simple_tf_kinematics
    def __init__(self):
        super().__init__("simple_tf_kinematics")

        #Creamos dos varibles donde vamos a guardar los valores de los objetos, estatico y dinamico
        self.static_tf_broadcaster_ = StaticTransformBroadcaster(self)
        self.dynamic_tf_broadcaster_ = TransformBroadcaster(self)

        #Damos a los mensajes un sello de hora actual segun el ordenador
        self.static_transform_stamped= TransformStamped()
        self.dynamic_transform_stamped_= TransformStamped()

        #creamos la varibles de incremento en linea recta en este caso
        self.x_increment_ = 0.05
        self.last_x_ = 0.0

        self.static_transform_stamped.header.stamp = self.get_clock().now().to_msg()
        self.static_transform_stamped.header.frame_id = "bumperbot_base"
        self.static_transform_stamped.child_frame_id = "bumperbot_top"
        self.static_transform_stamped.transform.translation.x = 0.0
        self.static_transform_stamped.transform.translation.y = 0.0
        self.static_transform_stamped.transform.translation.z = 0.3
        self.static_transform_stamped.transform.rotation.x = 0.0
        self.static_transform_stamped.transform.rotation.y = 0.0
        self.static_transform_stamped.transform.rotation.z = 0.0        
        self.static_transform_stamped.transform.rotation.w = 1.0

        #Creamos los datos que le vamos a añadir al objeto dinamico
        self.dynamic_transform_stamped_.header.stamp = self.get_clock().now().to_msg()
        self.dynamic_transform_stamped_.header.frame_id = "odom"
        self.dynamic_transform_stamped_.child_frame_id = "bumperbot_base"

        self.static_tf_broadcaster_.sendTransform(self.static_transform_stamped)

        self.get_logger().info(f"publishing static transform between {self.static_transform_stamped.header.frame_id} and {self.static_transform_stamped.child_frame_id}")
        self.get_logger().info(f"publicando diferencia entre {self.dynamic_transform_stamped_.header.frame_id} and {self.static_transform_stamped.header.frame_id}")

    #creamos una funcion que servirá para controlar cada cuanto se va a publicar los mensajes en el hijo dinamico
        self.timer_= self.create_timer(0.1,self.timerCallback)
    
    def timerCallback(self):
        self.dynamic_transform_stamped_.header.stamp = self.get_clock().now().to_msg()
        self.dynamic_transform_stamped_.header.frame_id = "odom"
        self.dynamic_transform_stamped_.child_frame_id = "bumperbot_base"
        self.dynamic_transform_stamped_.transform.translation.x = self.last_x_ +self.x_increment_
        self.dynamic_transform_stamped_.transform.translation.y = 0.0
        self.dynamic_transform_stamped_.transform.translation.z = 0.0
        self.dynamic_transform_stamped_.transform.rotation.x = 0.0
        self.dynamic_transform_stamped_.transform.rotation.y = 0.0
        self.dynamic_transform_stamped_.transform.rotation.z = 0.0
        self.dynamic_transform_stamped_.transform.rotation.w = 1.0

        self.dynamic_tf_broadcaster_.sendTransform(self.dynamic_transform_stamped_)

        self.last_x_ = self.dynamic_transform_stamped_.transform.translation.x

def main():
    rclpy.init()
    simple_tf_kinematics = SimpleTfKinematics()
    rclpy.spin(simple_tf_kinematics)
    simple_tf_kinematics.destroy_node()
    rclpy.shutdown()       

if __name__== '__main__':
    main()