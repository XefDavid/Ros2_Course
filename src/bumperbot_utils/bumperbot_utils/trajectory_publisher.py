import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import PoseStamped

class trajectoryPublisher(Node):
    def __init__(self):
        super().__init__("trajectory_publisher")

        self.odometry_subs = self.create_subscription(Odometry, "/bumperbot_controller/odom", self.odom_callback, 10)
        self.get_logger().info("Escuchando el nodo /bumperbot_controller/odom")

        self.publish_trajectory = self.create_publisher(Path,"/bumperbot_controller/trajectory", 10)
        self.get_logger().info("Nodo /bumperbot_controller/trajectory funcionando!!")

        self.trajectory = Path()
        self.trajectory.header.frame_id = "odom"

    def odom_callback(self, msg):
        pose = PoseStamped()
        pose.header = msg.header
        pose.pose = msg.poso.pose

        self.trajectory.poses.append(pose)
        self.trajectory.header.stamp = self.get_clock().now().to_msg()

        self.publish_trajectory.publish(self.trajectory)

        self.get_logger().info(f"la funcion funcionando {msg.header}")

def main():
    rclpy.init()
    trajectory_publisher = trajectoryPublisher()
    rclpy.spin(trajectory_publisher)
    trajectory_publisher.destroy_node()
    rclpy.shutdown()

if __name__== "__main__":
    main()
