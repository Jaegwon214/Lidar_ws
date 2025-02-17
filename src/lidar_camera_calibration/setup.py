from setuptools import find_packages, setup

package_name = 'lidar_camera_calibration'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jae',
    maintainer_email='jae@todo.todo',
    description='LiDAR와 카메라 캘리브레이션을 위한 ROS2 패키지',
    license='Apache-2.0',
    # tests_require=['pytest'],  colcon build --packages-select lidar_camera_calibration 과정 중 오류 발생 - 옵션 제거 가능
    entry_points={
        'console_scripts': [
            'calibration_node = lidar_camera_calibration.calibration_node:main',
        ],
    },
)

