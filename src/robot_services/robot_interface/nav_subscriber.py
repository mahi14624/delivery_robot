import rclpy
from rclpy.node import Node
from robot_interfaces.msg import RobotStatus

class NavSubscriber(Node):
    def __init__(self):
        super().__init__('nav_subscriber')
        self.subscription = self.create_subscription(RobotStatus,'robot_status',self.listener_callback,10)
        self.get_logger().info('NavSubscriber node has been started.')

    def listener_callback(self, msg):
        if msg.obstacle_detected:
            self.get_logger().warn(f'Obstacle detected. Distance: {msg.distance_remaining:.1f}m ')
        else:
            self.get_logger().info(f'Distance: {msg.distance_remaining:.1f}m ')



def main(args=None):
    rclpy.init(args=args)
    node = NavSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
