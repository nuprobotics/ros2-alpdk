import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class TriggerNode(Node):
    def __init__(self):
        super().__init__('trigger_node')

        # Declare and read parameters
        self.declare_parameter('service_name', '/trigger_service')
        self.declare_parameter('default_string', 'No service available')

        # Get parameters
        self.service_name = self.get_parameter('service_name').get_parameter_value().string_value
        self.default_string = self.get_parameter('default_string').get_parameter_value().string_value

        # Create a service client to call the /spgc/trigger service
        self.client = self.create_client(Trigger, '/spgc/trigger')

        # Call the service and store the response or default string if unavailable
        self.response_string = self.call_trigger_service()

        # Create a service to provide the stored response
        self.create_service(Trigger, self.service_name, self.handle_trigger_service)

    def call_trigger_service(self):
        if not self.client.service_is_ready():
            self.get_logger().warn('/spgc/trigger service not available.')
            return self.default_string

        request = Trigger.Request()
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None and future.result().success:
            self.get_logger().info(f"Received response: {future.result().message}")
            return future.result().message

        return self.default_string

    def handle_trigger_service(self, request, response):
        response.success = True
        response.message = self.response_string
        self.get_logger().info(f"Returning response: {self.response_string}")
        return response


def main(args=None):
    rclpy.init(args=args)
    node = TriggerNode()

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
