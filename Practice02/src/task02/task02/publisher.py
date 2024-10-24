import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.parameter import Parameter

class Publisher(Node):
    def __init__(self, text = 'Hello, ROS2!'):
        super().__init__('publisher')

        # Load parameters from the config file
        self.declare_parameter('topic_name', '/spgc/receiver')
        self.declare_parameter('text', text)

        self.topic_name = self.get_parameter('topic_name').get_parameter_value().string_value
        self.text = self.get_parameter('text').get_parameter_value().string_value

        # Create a publisher
        self.publisher_ = self.create_publisher(String, self.topic_name, 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = self.text
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}" to topic: {self.topic_name}')

def main(args=None):
    rclpy.init(args=args)

    # Read command line parameter
    if len(args) > 1:
        node = Publisher(args[1])
    else:
        node = Publisher()

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()