# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DscConfigurationUpdateParameters(Model):
    """The parameters supplied to the create or update configuration operation.

    All required parameters must be populated in order to send to Azure.

    :param log_verbose: Gets or sets verbose log option.
    :type log_verbose: bool
    :param log_progress: Gets or sets progress log option.
    :type log_progress: bool
    :param source: Required. Gets or sets the source.
    :type source: ~azure.mgmt.automation.models.ContentSource
    :param parameters: Gets or sets the configuration parameters.
    :type parameters: dict[str,
     ~azure.mgmt.automation.models.DscConfigurationParameter]
    :param description: Gets or sets the description of the configuration.
    :type description: str
    :param name: Gets or sets name of the resource.
    :type name: str
    :param tags: Gets or sets the tags attached to the resource.
    :type tags: dict[str, str]
    """

    _validation = {
        'source': {'required': True},
    }

    _attribute_map = {
        'log_verbose': {'key': 'properties.logVerbose', 'type': 'bool'},
        'log_progress': {'key': 'properties.logProgress', 'type': 'bool'},
        'source': {'key': 'properties.source', 'type': 'ContentSource'},
        'parameters': {'key': 'properties.parameters', 'type': '{DscConfigurationParameter}'},
        'description': {'key': 'properties.description', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
    }

    def __init__(self, *, source, log_verbose: bool=None, log_progress: bool=None, parameters=None, description: str=None, name: str=None, tags=None, **kwargs) -> None:
        super(DscConfigurationUpdateParameters, self).__init__(**kwargs)
        self.log_verbose = log_verbose
        self.log_progress = log_progress
        self.source = source
        self.parameters = parameters
        self.description = description
        self.name = name
        self.tags = tags
