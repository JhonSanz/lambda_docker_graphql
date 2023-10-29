#!/usr/bin/env python3

import aws_cdk as cdk

from positions_backend_micro.positions_backend_micro_stack import PositionsBackendMicroStack


app = cdk.App()
PositionsBackendMicroStack(app, "PositionsBackendMicroStack")

app.synth()
