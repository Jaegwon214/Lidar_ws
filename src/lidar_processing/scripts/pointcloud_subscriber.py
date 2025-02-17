
import numpy as np
import sensor_msgs_py.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2

def pointcloud_callback(msg: PointCloud2):
    # PointCloud2 메시지에서 데이터를 읽기
    points = []
    for point in pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True):
        x, y, z = point
        distance = np.sqrt(x**2 + y**2 + z**2)  # 거리 계산
        azimuth = np.arctan2(y, x) * 180 / np.pi  # 방위각 (도 단위)
        elevation = np.arctan2(z, np.sqrt(x**2 + y**2)) * 180 / np.pi  # 고도각 (도 단위)
        points.append((x, y, z, distance, azimuth, elevation))
    
    # 고도각이 -90도 이상 90도 이하이고 방위각이 -180도 이상 180도 이하인 포인트들만 선택
    selected_points = [
        (x, y, z, distance, azimuth, elevation)
        for (x, y, z, distance, azimuth, elevation) in points
        if -90 <= elevation <= 90 and -180 <= azimuth <= 180  # 고도각과 방위각 제한
    ]
    
    # 선택된 포인트들 출력
    for i, point in enumerate(selected_points[:100]):  # 최대 100개의 포인트만 출력
        print(f"포인트 {i + 1}: x={point[0]}, y={point[1]}, z={point[2]}")
        print(f"거리: {point[3]:.2f}m, 방위각: {point[4]:.2f}°, 고도각: {point[5]:.2f}°")

# ROS2 노드 생성 및 실행
import rclpy
from rclpy.node import Node

class PointCloudSubscriber(Node):
    def __init__(self):
        super().__init__('pointcloud_listener')
        self.subscription = self.create_subscription(
            PointCloud2,
            '/velodyne_points',  # Velodyne LIDAR 토픽 이름
            pointcloud_callback,
            10)

def main():
    rclpy.init()
    node = PointCloudSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
