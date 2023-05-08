import aws_cdk as core
import aws_cdk.assertions as assertions

from gptapi.gptapi_stack import GptapiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in gptapi/gptapi_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GptapiStack(app, "gptapi")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
