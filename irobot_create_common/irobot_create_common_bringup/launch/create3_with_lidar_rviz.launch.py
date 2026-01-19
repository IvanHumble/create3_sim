#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory

ARGUMENTS = [
    DeclareLaunchArgument('gazebo', default_value='classic',
                          choices=['classic', 'ignition'],
                          description='Which gazebo simulator to use'),
    DeclareLaunchArgument('namespace', default_value='',
                          description='Robot namespace'),
]


def generate_launch_description():
    # Directories
    pkg_create3_common_bringup = get_package_share_directory('irobot_create_common_bringup')
    pkg_create3_control = get_package_share_directory('irobot_create_control')

    # Paths
    control_launch_file = PathJoinSubstitution(
        [pkg_create3_control, 'launch', 'include', 'control.py'])
    
    # Includes
    diffdrive_controller = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([control_launch_file]),
        launch_arguments=[('namespace', LaunchConfiguration('namespace'))]
    )

    # URDF xacro
    create3_description = os.path.join(
        get_package_share_directory('irobot_create_description'),
        'urdf',
        'create3.urdf.xacro'
    )

    lidar_xacro = os.path.join(
        get_package_share_directory('rplidar_ros'),
        'robot_description',
        'urdf',
        'lidar.xacro'
    )

    rviz_config = os.path.join(
        get_package_share_directory('rplidar_ros'),
        'rviz',
        'rplidar_ros.rviz'
    )

    # Build robot_description using xacro (Command requires xacro to be on PATH)
    from launch.substitutions import Command
    robot_description = Command([
        "xacro ", create3_description,
        #" lidar_xacro:=", lidar_xacro
    ])

    # Include Create3 driver (if you want to start it from this launch; optional)
    # create3_nodes_launch = os.path.join(
    #     get_package_share_directory('irobot_create_common_bringup'),
    #     'launch',
    #     'create3_nodes.launch.py'
    # )
    # include_create3 = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(create3_nodes_launch)
    # )

    ld = LaunchDescription()

    # OPTIONAL: Include the create3_nodes launch if you want that started together.
    # If you already started it in a separate terminal, you can comment this out.
    #ld.add_action(include_create3)

    # robot_state_publisher (publish TF for URDF links)
    # ld.add_action(Node(
    #     package='robot_state_publisher',
    #     executable='robot_state_publisher',
    #     parameters=[{'robot_description': robot_description}],
    #     output='screen'
    # ))

    # ld.add_action(Node(
    #     package='irobot_create_nodes',
    #     executable='motion_control',
    #     name='motion_control',
    #     parameters=[{'use_sim_time': False}],
    #     remappings=[
    #         ('/tf', 'tf'),
    #         ('/tf_static', 'tf_static')
    #     ],
    #     output='screen'
    # ))

    # ld.add_action(Node(
    # package='tf2_ros',
    # executable='static_transform_publisher',
    # arguments=[
    #     '0', '0', '0.05',
    #     '0', '0', '0',
    #     'base_footprint',
    #     'base_link'
    # ],
    # output='screen'
    # ))
    
    # ld.add_action(Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     name='laser_tf',
    #     arguments=[
    #         '0.1', '0.0', '0.175',   # xyz iz xacro
    #         '0.0', '0.0', '0.0',     # rpy iz xacro
    #         'base_link',              # parent link iz xacro
    #         'laser'                   # child link iz xacro
    #     ],
    #     output='screen'
    # ))
    # # --- EKF for odom → base_link TF ---
    # ld.add_action(Node(
    #     package='robot_localization',
    #     executable='ekf_node',
    #     name='ekf_filter_node',
    #     output='screen',
    #     parameters=[{
    #         'frequency': 30.0,
    #         'two_d_mode': True,
    #         'publish_tf': True,

    #         'map_frame': 'map',
    #         'odom_frame': 'odom',
    #         'base_link_frame': 'base_link',
    #         'world_frame': 'odom',

    #         # Koristimo odometriju robota
    #         'odom0': '/odom',
    #         'odom0_config': [
    #             True, True, False,
    #             False, False, True,
    #             False, False, False,
    #             False, False, False,
    #             False, False, False
    #         ]
    #     }]
    # ))
    
    # RPLidar node (adjust serial port as needed)
    ld.add_action(Node(
        package='rplidar_ros',
        executable='rplidar_node',
        name='rplidar_node',
        parameters=[{
            'channel_type': 'serial',
            'serial_port': '/dev/ttyUSB0',
            'serial_baudrate': 256000,
            'frame_id': 'laser',
            'inverted': False,
            'angle_compensate': True,
            'scan_mode': 'Sensitivity'
        }],
        output='screen'
    ))

    # RViz
    ld.add_action(Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen'
    ))



    return ld