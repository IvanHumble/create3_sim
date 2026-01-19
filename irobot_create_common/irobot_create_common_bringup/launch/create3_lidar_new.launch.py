#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    ld = LaunchDescription()

    # --------------------------------------------------
    # RPLIDAR NODE
    # --------------------------------------------------
    ld.add_action(Node(
        package='rplidar_ros',
        executable='rplidar_node',
        name='rplidar_node',
        parameters=[{
            'channel_type': 'serial',
            'serial_port': '/dev/ttyUSB0',
            'serial_baudrate': 256000,
            'frame_id': 'laser',   # <-- frame koji MI dodajemo u TF
            'inverted': False,
            'angle_compensate': True,
            'scan_mode': 'Sensitivity'
        }],
        output='screen'
    ))

    # --------------------------------------------------
    # STATIC TF: base_link → laser
    # --------------------------------------------------
    ld.add_action(Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='laser_tf',
        arguments=[
            '0.1', '0.0', '0.175',   # XYZ (izmjeri stvarno)
            '0.0', '0.0', '0.0',     # RPY
            'base_link',             # POSTOJI (dolazi iz Create3)
            'laser'                  # DODAJEMO
        ],
        output='screen'
    ))

    # --------------------------------------------------
    # RVIZ
    # --------------------------------------------------
    ld.add_action(Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    ))

    return ld