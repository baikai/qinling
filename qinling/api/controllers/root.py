# Copyright 2013 - Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from oslo_log import log as logging
import pecan
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from qinling.api.controllers.v1 import resources
from qinling.api.controllers.v1 import root as v1_root

LOG = logging.getLogger(__name__)

API_STATUS = wtypes.Enum(str, 'SUPPORTED', 'CURRENT', 'DEPRECATED')


class APIVersion(resources.Resource):
    """An API Version."""

    id = wtypes.text
    "The version identifier."

    status = API_STATUS
    "The status of the API (SUPPORTED, CURRENT or DEPRECATED)."

    links = wtypes.ArrayType(resources.Link)
    "The link to the versioned API."

    @classmethod
    def sample(cls):
        return cls(
            id='v1.0',
            status='CURRENT',
            links=[
                resources.Link(target_name='v1', rel="self",
                               href='http://example.com:7070/v1')
            ]
        )


class APIVersions(resources.Resource):
    """API Versions."""
    versions = wtypes.ArrayType(APIVersion)

    @classmethod
    def sample(cls):
        v1 = APIVersion(id='v1.0', status='CURRENT', rel="self",
                        href='http://example.com:7070/v1')
        return cls(versions=[v1])


class RootController(object):
    v1 = v1_root.Controller()

    @wsme_pecan.wsexpose(APIVersions)
    def index(self):
        LOG.info("Fetching API versions.")

        host_url_v1 = '%s/%s' % (pecan.request.host_url, 'v1')
        api_v1 = APIVersion(
            id='v1.0',
            status='CURRENT',
            links=[resources.Link(href=host_url_v1, target='v1',
                                  rel="self", )]
        )

        return APIVersions(versions=[api_v1])
