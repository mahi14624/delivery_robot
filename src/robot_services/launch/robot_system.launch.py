from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot_services',
            executable='nav_service_server',
            name='nav_service_server',
            output='screen',
        ),
        Node(
            package='robot_services',
            executable='nav_publisher',
            name='nav_publisher',
            output='screen',
        ),
        Node(
            package='robot_services',
            executable='nav_subscriber',
            name='nav_subscriber',
            output='screen',
        ),
    ])
