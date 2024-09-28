#!/usr/bin/python

# Copyright: (c) 2024, Sean Nelson <hyperkineticnerd@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: openshift_install

short_description: Ansible Module for interfacing with the openshift-installer

version_added: "1.0.0"

description: When working with Red Hat CoreOS and Red Hat OpenShift,
    this module allows calling the openshift-install program.

options:
    command:
        description: Commands for execution
        required: true
        type: str
        choices:
            - create_cluster
            - destroy_cluster
    dir:
        description: Assets directory
        required: false
        type: string
    log_level:
        description: level of output of STDOUT 
        required: false
        type: str
        choices:
            - debug
            - info
            - warn
            - error
        default: info

author:
    - Sean Nelson (@hyperkineticnerd)
'''


EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  hyperkineticnerd.openshift.butane:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  hyperkineticnerd.openshift.butane:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  hyperkineticnerd.openshift.butane:
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
import subprocess


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        command=dict(type='str', required=True),
        dir=dict(type='str', required=False, default='.'),
        log_level=dict(type='str', required=False, default='info')
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
        
    subproc_cmd = ["openshift-install"]

    if module.params['log_level']:
        subproc_cmd += [
            "--log-level",
            module.params['log_level'],
        ]

    if module.params['dir']:
        subproc_cmd += [
            "--dir",
            module.params['dir'],
        ]

    if module.params['command'] == 'create_cluster':
        subproc_cmd += [
            "create",
            "cluster",
        ]
    elif module.params['command'] == 'destroy_cluster':
        subproc_cmd += [
            "destroy",
            "cluster",
        ]
    else:
        module.exit_json(**result)

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
    if module.params['command']:
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
