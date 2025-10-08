import rclpy
import math
from rclpy.node import Node
from turtlesim.msg import Pose

# construimos la clase
class SimpleTurtlesimKinematics(Node):
    # creamos el constructor
    def __init__(self):
        super().__init__("simple_turtlesim_kinematics")

        # creamos los dos topicos con la pose , la ruta de cada topic y los mansajes en cola
        self.turtle1_pose_sub_ = self.create_subscription(Pose, "/turtle1/pose", self.turtle1PoseCallback, 10)
        self.turtle2_pose_sub  = self.create_subscription(Pose, "/turtle2/pose", self.turtle2PoseCallback, 10)

        self.last_turtle1_pose = Pose()
        self.last_turtle2_pose = Pose()

    # definimos las funciones donde vamos a calcular la translacion entre los dos puntos
    # primero definimos el punto del punto 1, que lo dejamos estatico sin comparacion, para poder compararlos con el punto 2
    def turtle1PoseCallback(self, msg):
        self.last_turtle1_pose = msg
    # aqui damos el valor la translacion al tener el valor de los dos puntos
    def turtle2PoseCallback(self, msg):
        self.last_turtle2_pose = msg
        # calculamos la translacion ente los dos puntos
        Tx = self.last_turtle2_pose.x - self.last_turtle1_pose.x
        Ty = self.last_turtle2_pose.y - self.last_turtle1_pose.y
        # calculamos la diferencia entre puntos R
        theta_rad = self.last_turtle2_pose.theta- self.last_turtle1_pose.theta
        theta_deg = 180 * theta_rad/3.14

    # imprimimos por pantalla
        self.get_logger(). info("""\n
                Translation Vector turtle1 => turtle2 \n
                Tx: %f \n
                Ty: %f \n
                Rotation Matrix turtle1 => turtle2 \n
                theta(rad): %f\n
                theta(deg): %f\n
                |R11         R12| : |%f    %f|\n
                |R21         R22| : |%f     %f|\n""" %(Tx,Ty,theta_rad,theta_deg,math.cos(theta_rad),
                                                       -math.sin(theta_rad),math.sin(theta_rad),math.cos(theta_rad)))
def main():
    rclpy.init()
    Simple_Turtlesim_Kinematics = SimpleTurtlesimKinematics()
    rclpy.spin(Simple_Turtlesim_Kinematics)
    Simple_Turtlesim_Kinematics.destroy_node()
    rclpy.shutdown()



if __name__==  '__main__':
    main()


