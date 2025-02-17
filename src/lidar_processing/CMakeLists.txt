cmake_minimum_required(VERSION 3.5)
project(lidar_processing)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(sensor_msgs REQUIRED)

# Install Python modules
install(
  DIRECTORY lidar_processing/
  DESTINATION lib/python${PYTHON_VERSION}/site-packages
)

# Declare ament package
ament_package()


