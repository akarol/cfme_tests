# -*- coding: utf-8 -*-
import fauxfactory
import pytest

from cfme.automate import explorer as automate
from cfme.common.provider import cleanup_vm
import cfme.configure.access_control as ac
from cfme.provisioning import do_vm_provisioning
from utils import normalize_text, testgen, version
from utils.log import logger
from utils.wait import wait_for


pytestmark = [
    pytest.mark.meta(server_roles="+automate +notifier"),
    pytest.mark.usefixtures('uses_infra_providers')
]


def pytest_generate_tests(metafunc):
    # Filter out providers without provisioning data or hosts defined
    argnames, argvalues, idlist = testgen.infra_providers(
        metafunc, 'provisioning', template_location=["provisioning", "template"])

    new_idlist = []
    new_argvalues = []
    for i, argvalue_tuple in enumerate(argvalues):
        args = dict(zip(argnames, argvalue_tuple))
        if not args['provisioning']:
            # No provisioning data available
            continue

        if args['provider'].type == "scvmm":
            continue

        # required keys should be a subset of the dict keys set
        if not {'template', 'host', 'datastore'}.issubset(args['provisioning'].viewkeys()):
            # Need all three for template provisioning
            continue

        new_idlist.append(idlist[i])
        new_argvalues.append(argvalues[i])

    testgen.parametrize(metafunc, argnames, new_argvalues, ids=new_idlist, scope="module")


@pytest.fixture(scope="function")
def vm_name():
    vm_name = 'test_quota_prov_%s' % fauxfactory.gen_alphanumeric()
    return vm_name


@pytest.fixture(scope="module")
def domain(request):
    if version.current_version() < "5.3":
        return None
    domain = automate.Domain(name=fauxfactory.gen_alphanumeric(), enabled=True)
    domain.create()
    request.addfinalizer(lambda: domain.delete() if domain.exists() else None)
    return domain


@pytest.fixture(scope="module")
def cls(request, domain):
    tcls = automate.Class(name="ProvisionRequestQuotaVerification",
        namespace=automate.Namespace.make_path("Infrastructure", "VM", "Provisioning", "StateMachines",
            parent=domain, create_on_init=True))
    tcls.create()
    request.addfinalizer(lambda: tcls.delete() if tcls.exists() else None)
    return tcls


@pytest.fixture(scope="module")
def copy_methods(domain):
    methods = ['rejected', 'validate_quotas']
    for method in methods:
        ocls = automate.Class(name="ProvisionRequestQuotaVerification",
            namespace=automate.Namespace.make_path("Infrastructure", "VM", "Provisioning", "StateMachines",
                parent=automate.Domain(name="ManageIQ (Locked)")))

        method = automate.Method(name=method, cls=ocls)

        method = method.copy_to(domain)


@pytest.fixture(scope="module")
def set_domain_priority(domain):
    automate.set_domain_order(domain)


def test_group_quota_max_memory_check_by_tagging(
        provider, provisioning, vm_name, request,
        domain, cls, copy_methods, set_domain_priority):
    """ Tests provisioning from a template

    Metadata:
        test_flag: provision
        suite: infra_provisioning

    """

    # generate_tests makes sure these have values
    template, host, datastore = map(provisioning.get, ('template', 'host', 'datastore'))

    request.addfinalizer(lambda: cleanup_vm(vm_name, provider))

    provisioning_data = {
        'vm_name': vm_name,
        'host_name': {'name': [host]},
        'datastore_name': {'name': [datastore]}
    }

    # Same thing, different names. :\
    if provider.type == 'rhevm':
        provisioning_data['provision_type'] = 'Native Clone'
    elif provider.type == 'virtualcenter':
        provisioning_data['provision_type'] = 'VMware'

    try:
        provisioning_data['vlan'] = provisioning['vlan']
    except KeyError:
        # provisioning['vlan'] is required for rhevm provisioning
        if provider.type == 'rhevm':
            raise pytest.fail('rhevm requires a vlan value in provisioning info')

    group = ac.Group(name='Administrator')
    group.edit_tags("Quota - Max Memory *", '2')

    do_vm_provisioning(template, provider, vm_name, provisioning_data, request,
                     num_sec=900)

    # Add check for quota validation
    group.remove_tag("Quota - Max Memory *", '2')
    # cleanup vm

"""
Group quota
test_group_quota_max_storage_check_by_tagging
test_group_quota_max_cpu_check_by_tagging
test_group_quota_max_memory_check_by_automate
test_group_quota_max_storage_check_by_atomate
test_group_quota_max_cpu_check_by_automate

user quota
test_user_quota_max_memory_check_by_tagging
test_user_quota_max_storage_check_by_tagging
test_user_quota_max_cpu_check_by_tagging
test_user_quota_max_memory_check_by_automate
test_user_quota_max_storage_check_by_automate
test_max_vm_quota_check_by_automate
"""
