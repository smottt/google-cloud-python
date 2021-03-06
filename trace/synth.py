# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp

gapic = gcp.GAPICGenerator()

for version in ['v1', 'v2']:
    library = gapic.py_library(
        'trace', version,
        config_path=f'/google/devtools/cloudtrace'
                    f'/artman_cloudtrace_{version}.yaml',
        artman_output_name=f'trace-{version}',
    )

    s.move(library / f'google/cloud/trace_{version}')
        
    # Fix up imports
    s.replace(
        'google/**/*.py',
        f"from google.devtools.cloudtrace_{version}.proto import ",
        f"from google.cloud.trace_{version}.proto import ",
    )


# Issues exist where python files should define the source encoding
# https://github.com/googleapis/gapic-generator/issues/2097
s.replace(
    'google/**/proto/*_pb2.py',
    r"(^.*$\n)*",
    r"# -*- coding: utf-8 -*-\n\g<0>")

# GAPIC-Generator is mangling some docstrings
# Missing blank line after bulleted list
s.replace(
    "google/cloud/trace_v1/gapic/trace_service_client.py",
    '                ::\n\n',
    '')
