# -*- coding: utf-8 -*-


import pytest
from cfme.configure import settings as st
from cfme.fixtures import pytest_selenium as sel
from utils.providers import setup_a_provider
from cfme.cloud import instance  # NOQA


@pytest.fixture(scope="module")
def setup_first_provider():
    setup_a_provider(validate=True, check_existing=True)


#@pytest.mark.parametrize('filters',
 #                       [[['Cloud', 'Instances', 'Images', 'Platform / Amazon']]])
def test_cloudimage_defaultfilters(filters, setup_first_provider):
    filters = [[['Cloud', 'Instances', 'Images', 'Platform / Amazon']]]
    df = st.DefaultFilter(name='Platform / Amazon')
    df.update({'filters': [(k, True) for k in filters]})
    sel.force_navigate('clouds_images_filter_folder', context={'folder_name': 'Global Filters'})
    assert sel.is_displayed_text(df.name), "Default Filter settings Failed!"


@pytest.mark.parametrize('filters',
                        [[['Cloud', 'Instances', 'Instances', 'Platform / Openstack']]])
def test_cloudinstance_defaultfilters(request, filters, setup_first_provider):
    df = st.DefaultFilter(name='Platform / Openstack')
    df.update({'filters': [(k, True) for k in filters]})
    sel.force_navigate('clouds_instances_filter_folder', context={'folder_name': 'Global Filters'})
    assert sel.is_displayed_text(df.name), "Default Filter settings Failed!"


@pytest.mark.parametrize('filters',
                        [[['Infrastructure', 'Hosts', 'Platform / HyperV']]])
def test_infrastructurehost_defaultfilters(filters, setup_first_provider):
    df = st.DefaultFilter(name='Platform / HyperV')
    df.update({'filters': [(k, True) for k in filters]})
    sel.force_navigate('infrastructure_hosts')
    assert sel.is_displayed_text(df.name), "Default Filter settings Failed!"


@pytest.mark.parametrize('filters',
                        [[['Infrastructure', 'Virtual Machines', 'VMs', 'Platform / VMware']]])
def test_infrastructurevms_defaultfilters(filters, setup_first_provider):
    df = st.DefaultFilter(name='Platform / VMware')
    df.update({'filters': [(k, True) for k in filters]})
    sel.force_navigate('infra_vms_filter_folder', context={'folder_name': 'Global Filters'})
    assert sel.is_displayed_text(df.name), "Default Filter settings Failed!"


@pytest.mark.parametrize('filters',
                    [[['Infrastructure', 'Virtual Machines', 'Templates', 'Platform / Redhat']]])
def test_infrastructuretemplates_defaultfilters(filters, setup_first_provider):
    df = st.DefaultFilter(name='Platform / Redhat')
    df.update({'filters': [(k, True) for k in filters]})
    sel.force_navigate('infra_templates_filter_folder', context={'folder_name': 'Global Filters'})
    assert sel.is_displayed_text(df.name), "Default Filter settings Failed!"
