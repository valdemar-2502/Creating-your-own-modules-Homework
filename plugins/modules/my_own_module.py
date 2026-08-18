#!/usr/bin/python

# Copyright: (c) 2026, Vladimir <vladimir@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: Creates a text file with given content on the remote host

version_added: "1.0.0"

description:
    - This module creates (or updates) a text file at a given path on the remote
      host, writing the given content into it.
    - The module is idempotent — if the file already exists with the requested
      content, no changes are made.

options:
    path:
        description: Full path to the file that should be created on the remote host.
        required: true
        type: str
    content:
        description: Content that should be written into the file.
        required: true
        type: str

author:
    - Vladimir (@yourGitHubHandle)
'''

EXAMPLES = r'''
- name: Create a file with content
  my_own_namespace.yandex_cloud_elk.my_test:
    path: /tmp/my_test_file.txt
    content: "hello world"
'''

RETURN = r'''
path:
    description: The path of the file that was created or updated.
    type: str
    returned: always
    sample: '/tmp/my_test_file.txt'
content:
    description: The content that was written to the file.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: Human readable result message.
    type: str
    returned: always
    sample: 'file created'
'''

import os
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
        path='',
        content='',
        message='',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    path = module.params['path']
    content = module.params['content']

    result['path'] = path
    result['content'] = content

    file_exists = os.path.isfile(path)
    current_content = None
    if file_exists:
        try:
            with open(path, 'r') as f:
                current_content = f.read()
        except IOError as e:
            module.fail_json(msg='Unable to read existing file: %s' % str(e), **result)

    needs_change = (not file_exists) or (current_content != content)

    if module.check_mode:
        result['changed'] = needs_change
        module.exit_json(**result)

    if needs_change:
        try:
            directory = os.path.dirname(path)
            if directory and not os.path.isdir(directory):
                os.makedirs(directory)
            with open(path, 'w') as f:
                f.write(content)
            result['changed'] = True
            result['message'] = 'file created' if not file_exists else 'file content updated'
        except (IOError, OSError) as e:
            module.fail_json(msg='Unable to write file: %s' % str(e), **result)
    else:
        result['changed'] = False
        result['message'] = 'file already up to date'

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
