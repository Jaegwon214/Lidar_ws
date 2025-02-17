#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, PointCloud2
from message_filters import ApproximateTimeSynchronizer, Subscriber as MFSubscriber
from cv_bridge import CvBridge
import cv2

# calibration_algorithm.py 모듈에서 캘리브레이션 함수를 import 합니다.
from lidar_camera_calibration.calibration_algorithm import calibrate_extrinsics

class CalibrationNode(Node):
    def __init__(self):
        super().__init__('calibration_node')
        self.bridge = CvBridge()

        # 동기화된 메시지를 받기 위한 message_filters.Subscriber 사용
        self.image_sub = MFSubscriber(self, Image, '/yolov5/image_raw')  # 예: '/yolov5/image_raw'
        self.lidar_sub = MFSubscriber(self, PointCloud2, '/velodyne_points')
        self.ts = ApproximateTimeSynchronizer(
            [self.image_sub, self.lidar_sub],
            queue_size=10,
            slop=0.1  # 0.1초 이내의 타임스탬프 차이를 허용
        )
        self.ts.registerCallback(self.sync_callback)

        # 센서 연결 상태 및 주기 모니터링을 위한 일반 subscriber (동일한 토픽 구독)
        self.image_monitor_sub = self.create_subscription(
            Image,
            '/yolov5/image_raw',  # 예: '/yolov5/image_raw'
            self.image_monitor_callback,
            10
        )
        self.lidar_monitor_sub = self.create_subscription(
            PointCloud2,
            '/velodyne_points',
            self.lidar_monitor_callback,
            10
        )

        self.last_image_time = None
        self.last_lidar_time = None

        # 주기적으로 센서 연결 상태를 체크하는 타이머 (2초 간격)
        self.create_timer(2.0, self.check_connectivity)

    def sync_callback(self, image_msg, lidar_msg):
        # 동기화된 메시지를 받으면 OpenCV를 사용해 이미지 변환 후 창에 표시
        try:
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, desired_encoding="bgr8")
        except Exception as e:
            self.get_logger().error(f"Image conversion error: {e}")
            return

        # 동기화된 메시지 정보를 로그에 출력
        self.get_logger().info(
            f'Image received - stamp: {image_msg.header.stamp.sec}.{image_msg.header.stamp.nanosec}, '
            f'size: {image_msg.height}x{image_msg.width}'
        )
        self.get_logger().info(
            f'LiDAR received - stamp: {lidar_msg.header.stamp.sec}.{lidar_msg.header.stamp.nanosec}'
        )
        self.get_logger().info('Synchronized data received')

        # 캘리브레이션 알고리즘 호출 (실제 캘리브레이션 타겟 검출/매칭 결과를 입력해야 함)
        try:
            transformation_matrix = calibrate_extrinsics(cv_image, lidar_msg)
            self.get_logger().info(f'Calculated transformation matrix:\n{transformation_matrix}')
        except Exception as e:
            self.get_logger().error(f"Calibration algorithm error: {e}")

        # OpenCV 창에 이미지 표시
        cv2.imshow("Camera Image", cv_image)
        cv2.waitKey(1)
        # 주석: GUI 창 출력이 필요 없으면 위 두 줄을 주석 처리하세요.

    def image_monitor_callback(self, msg):
        now = self.get_clock().now()
        if self.last_image_time is not None:
            dt = (now - self.last_image_time).nanoseconds / 1e9
            frequency = 1.0 / dt if dt > 0 else 0.0
            self.get_logger().info(f'Camera sensor frequency: {frequency:.2f} Hz')
        self.last_image_time = now

    def lidar_monitor_callback(self, msg):
        now = self.get_clock().now()
        if self.last_lidar_time is not None:
            dt = (now - self.last_lidar_time).nanoseconds / 1e9
            frequency = 1.0 / dt if dt > 0 else 0.0
            self.get_logger().info(f'LiDAR sensor frequency: {frequency:.2f} Hz')
        self.last_lidar_time = now

    def check_connectivity(self):
        now = self.get_clock().now()
        if self.last_image_time is None or (now - self.last_image_time).nanoseconds / 1e9 > 5:
            self.get_logger().warn("Camera data not received recently!")
        else:
            self.get_logger().info("Camera is connected.")
        if self.last_lidar_time is None or (now - self.last_lidar_time).nanoseconds / 1e9 > 5:
            self.get_logger().warn("LiDAR data not received recently!")
        else:
            self.get_logger().info("LiDAR is connected.")

def main(args=None):
    rclpy.init(args=args)
    node = CalibrationNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    cv2.destroyAllWindows()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

