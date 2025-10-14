import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped


class SimpleTfKinematics (Node):
    def __init__(self):
        super().__init__("simple_tf_kinematics")

        self.static_tf_broadcaster_ = StaticTransformBroadcaster(self)

        self.static_transform_stamped = TransformStamped()
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

        self.static_tf_broadcaster_.sendTransform(self.static_transform_stamped)

        self.get_logger().info(f"publishing static transform between {self.static_transform_stamped.header.frame_id} and {self.static_transform_stamped.child_frame_id}")

def main():
    rclpy.init()
    simple_tf_kinematics = SimpleTfKinematics()
    rclpy.spin(simple_tf_kinematics)
    simple_tf_kinematics.destroy_node()
    rclpy.shutdown()       

if __name__== '__main__':
    main()