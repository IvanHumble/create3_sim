#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    rviz_config = os.path.join(
        get_package_share_directory('rplidar_ros'),
        'rviz',
        'rplidar_ros.rviz'
    )

    ld = LaunchDescription()

    # ------------------------------------------------
    # STATIC TF: base_link -> laser
    # ------------------------------------------------
    ld.add_action(Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0.1', '0', '0.175',   # xyz (PRILAGODI AKO TREBA)
            '0', '0', '0',        # rpy
            'base_link',
            'laser'
        ]
    ))

    # ------------------------------------------------
    # RPLIDAR
    # ------------------------------------------------
    ld.add_action(Node(
        package='rplidar_ros',
        executable='rplidar_node',
        name='rplidar_node',
        parameters=[{
            'channel_type': 'serial',
            'serial_port': '/dev/ttyUSB0',
            'serial_baudrate': 256000,
            'frame_id': 'laser'
        }],
        output='screen'
    ))

    # ------------------------------------------------
    # RVIZ
    # ------------------------------------------------
    ld.add_action(Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen'
    ))

    return ld