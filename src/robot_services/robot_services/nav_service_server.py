import rclpy
from rclpy.node import Node
from robot_interfaces.srv import EstimateArrivalTime

class NavServiceServer(Node):
    def __init__(self):
        super().__init__('nav_service_server')
        self.srv = self.create_service(EstimateArrivalTime, 'estimate_arrival_time', self.estimate_arrival_time_callback)
        self.get_logger().info('NavServiceServer node has been started.')

    def estimate_arrival_time_callback(self,request, response):
        if request.speed > 0.0:
            seconds_remaining = request.distance_remaining / request.speed
            response.minutes_remaining = seconds_remaining / 60.0
        else:
            response.minutes_remaining = float('inf')
            self.get_logger().info(
            f'Service request -> Distance: {request.distance_remaining:.1f}m, '
            f'Speed: {request.speed:.1f}m/s => '
            f'ETA: {response.minutes_remaining:.1f} min'
          )        
        return response
    
def main(args=None):
    rclpy.init(args=args)

    node = NavServiceServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()