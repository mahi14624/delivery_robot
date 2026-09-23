import rclpy
import random
from rclpy.node import Node
from robot_interfaces.msg import RobotStatus

class NavPublisher(Node):
    def __init__(self):
        super().__init__('nav_publisher')
        self.publisher_ = self.create_publisher(RobotStatus, 'robot_status', 10)
        timer_period = 1.0  
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info('NavPublisher node has been started.')
        self.distance_remaining=100.0
        self.speed=2.5
        self.timer_period =timer_period

    def timer_callback(self):
        msg=RobotStatus()
        msg.distance_remaining=max(self.distance_remaining, 0.0)
        msg.speed=self.speed
        msg.obstacle_detected=random.random() < 0.2
        self.publisher_.publish(msg)
        self.get_logger().info(
        f'Published -> distance_remaining={msg.distance_remaining:.1f} m, '
        f'speed={msg.speed:.1f} m/s, '
        f'obstacle_detected={msg.obstacle_detected}'
        )
        self.distance_remaining -= self.speed * self.timer_period
        if self.distance_remaining <= 0.0:
            self.distance_remaining = 100.0
        
def main(args=None):
    rclpy.init(args=args)

    node = NavPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()