import rclpy
from rclpy.node import Node
from robot_interfaces.msg import RobotStatus
from robot_interfaces.srv import EstimateArrivalTime

class NavSubscriber(Node):
    def __init__(self):
        super().__init__('nav_subscriber')
        self.subscription = self.create_subscription(RobotStatus,'robot_status',self.status_callback,10)
        self.client = self.create_client(EstimateArrivalTime, 'estimate_arrival_time')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again')
        self.latest_msg = None
            
    def status_callback(self, msg):
        self.latest_msg = msg
        
        request = EstimateArrivalTime.Request()
        request.distance_remaining = msg.distance_remaining
        request.speed = msg.speed
        
        future = self.client.call_async(request)
        future.add_done_callback(self.service_response_callback)
        
        
    def service_response_callback(self, future):
        msg=self.latest_msg
        try:
            response =future.result()
            
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
            return
        eta = response.minutes_remaining
                
        if msg.obstacle_detected:
            self.get_logger().warn  (f'Obstacle detected. Distance: {msg.distance_remaining:.1f}m | ' f'ETA:{eta:.1f} mins')
        else:
            self.get_logger().info(f'Distance: {msg.distance_remaining:.1f}m | ETA: {eta:.1f} mins')



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