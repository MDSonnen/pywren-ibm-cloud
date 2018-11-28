#
# (C) Copyright IBM Corp. 2018
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
#

import logging
from pywren_ibm_cloud import wrenlogging
from pywren_ibm_cloud.action.wrenhandler import ibm_cloud_function_handler

logger = logging.getLogger('__main__')
wrenlogging.ow_config(logging.DEBUG)


def main(args):
    logger.info("Starting IBM Cloud Function execution")
    ibm_cloud_function_handler(args)
    return {"greeting": "Finished"}
