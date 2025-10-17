import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from tf2_ros import TransformBroadcaster , TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from geometry_msgs.msg import TransformStamped
from bumperbot_msgs.srv import GetTransform
from tf_transformations import quaternion_from_euler, quaternion_multiply, quaternion_inverse



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
        #Creamos variables para almacenar la rotación
        self.rotations_counter_ = 0
        self.last_orientation_ = quaternion_from_euler(0, 0, 0)
        self.orientation_increment_ =quaternion_from_euler(0,0,0.5)


        #creamos dos variables para almacenar las transformacion del buffer y su subscripcion
        self.tf_buffer_ = Buffer()
        self.tf_listener_ =TransformListener(self.tf_buffer_, self)

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

        #Creamos una funcion que servirá para controlar cada cuanto se va a publicar los mensajes en el hijo dinamico
        self.timer_= self.create_timer(0.1,self.timerCallback)

        #Vamos a crear una variable para almacenar el listener
        # 1º definimos el archivo srv, 2º le damos un nombre al servicio listener, 3º funcion donde vamos a realizar lo que necesitamos 
        self.get_transform_srv_= self.create_service(GetTransform, "get_transform", self.getTransformCallback)

    
    def timerCallback(self):
        self.dynamic_transform_stamped_.header.stamp = self.get_clock().now().to_msg()
        self.dynamic_transform_stamped_.header.frame_id = "odom"
        self.dynamic_transform_stamped_.child_frame_id = "bumperbot_base"
        self.dynamic_transform_stamped_.transform.translation.x = self.last_x_ +self.x_increment_
        self.dynamic_transform_stamped_.transform.translation.y = 0.0
        self.dynamic_transform_stamped_.transform.translation.z = 0.0
        q = quaternion_multiply(self.last_orientation_,self.orientation_increment_)
        self.dynamic_transform_stamped_.transform.rotation.x = q[0]
        self.dynamic_transform_stamped_.transform.rotation.y = q[1]
        self.dynamic_transform_stamped_.transform.rotation.z = q[2]
        self.dynamic_transform_stamped_.transform.rotation.w = q[3]

        self.dynamic_tf_broadcaster_.sendTransform(self.dynamic_transform_stamped_)

        self.last_x_ = self.dynamic_transform_stamped_.transform.translation.x
        self.rotations_counter_ += 1
        self.last_orientation_ = q

        if self.rotations_counter_ >= 100:
            self.orientation_increment_= quaternion_inverse(self.orientation_increment_)
            self.rotations_counter_= 0

    # Definimos la funcion a usar dentro del servicio
    def getTransformCallback(self, req, res ):
        #Creamos un log para asegurarnos que va funcionando el flujo
        self.get_logger().info(f"Requested Transform between {req.frame_id} and  {req.child_frame_id}")
        #creamos una variable que almacena una valor de fecha y hora
        requested_transform = TransformStamped()
        try:
            #Intentamos almacenar dentro de la varible que devuelve la transformacion entre dos frames
            requested_transform = self.tf_buffer_.lookup_transform(req.frame_id, req.child_frame_id, rclpy.time.Time())
            #Si no hay esos datos de transformacion se lanza una excepcion
        except TransformException as e:
            self.get_logger().error(f"An error occurred while transforming {req.frame_id} and {req.child_frame_id}")
            res.success = False
            return res
            
        res.transform = requested_transform
        res.success = True
        return res

def main():
    rclpy.init()
    simple_tf_kinematics = SimpleTfKinematics()
    rclpy.spin(simple_tf_kinematics)
    simple_tf_kinematics.destroy_node()
    rclpy.shutdown()       

if __name__== '__main__':
    main()