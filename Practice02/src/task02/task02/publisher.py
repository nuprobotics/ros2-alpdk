import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.parameter import Parameter

class Publisher(Node):
    def __init__(self):
        super().__init__('string_publisher')

        # Load parameters from the config file
        self.declare_parameter('topic_name', '/spgc/receiver')
        self.declare_parameter('text', 'Hello, ROS2!')

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
    node = Publisher()

    # Read command line parameter
    if len(args) > 1:
        try:
            # Overriding the default message if provided
            node.text = args[1]
            node.set_parameters([Parameter('text', value=node.text)])
        except Exception as e:
            node.get_logger().error(f'Error setting text parameter: {e}')

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()