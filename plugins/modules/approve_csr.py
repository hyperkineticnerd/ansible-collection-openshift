#!/usr/bin/python

# Copyright: (c) 2024, Sean Nelson <hyperkineticnerd@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: approve_csr

short_description: Ansible Module for approving OpenShift Certificate Signing Requests

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: When working with Red Hat OpenShift, sometimes a CSR needs to be approved.

options:
    name:
        description: Name of the CSR to approve.
        required: true
        type: str

author:
    - Sean Nelson (@hyperkineticnerd)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  hyperkineticnerd.openshift.approve_csr:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  hyperkineticnerd.openshift.approve_csr:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  hyperkineticnerd.openshift.approve_csr:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        src=dict(type='str', required=True),
        dest=dict(type='str', required=False, default=''),
        check=dict(type='bool', required=False, default=False),
        pretty=dict(type='bool', required=False, default=False),
        raw=dict(type='bool', required=False, default=False),
        strict=dict(type='bool', required=False, default=False),
        version=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        rc='',
        stderr='',
        stdout=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)
        
    subproc_cmd = ["butane"]

    if module.params['dest']:
        subproc_cmd += [
            "--output",
            module.params['dest'],
        ]

    # if module.params['check']:
    #     subproc_cmd += ["--check",]

    if module.params['pretty']:
        subproc_cmd += ["--pretty",]

    if module.params['raw']:
        subproc_cmd += ["--raw",]

    if module.params['strict']:
        subproc_cmd += ["--strict",]

    if module.params['version']:
        subproc_cmd += ["--version",]

    subproc_cmd += [module.params['src']]

    subproc_ret = subprocess.run(subproc_cmd, capture_output=True)

    result.update({
        'rc': subproc_ret.returncode,
        'stderr': subproc_ret.stderr,
        'stdout': subproc_ret.stdout
    })

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    # result['original_message'] = module.params['name']
    # result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['src']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    # if module.params['name'] == 'fail me':
    #     module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
