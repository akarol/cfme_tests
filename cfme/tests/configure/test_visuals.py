# -*- coding: utf-8 -*-

import pytest
from cfme.configure.settings import visual
from cfme.fixtures import pytest_selenium as sel
from cfme.web_ui import paginator, toolbar as tb, Quadicon
from utils import testgen
from utils.conf import cfme_data
from utils.providers import setup_provider
from utils.update import update


def pytest_generate_tests(metafunc):
    argnames, argvalues, idlist = testgen.provider_by_type(metafunc, ['virtualcenter'])
    testgen.parametrize(metafunc, argnames, argvalues, ids=idlist, scope="module")


@pytest.fixture()
def provider_init(provider_key):
    try:
        setup_provider(provider_key)
    except Exception:
        pytest.skip("It's not possible to set up this provider, therefore skipping")


@pytest.fixture(scope="module")
def set_grid():
    visual.grid_view_limit = 5


@pytest.fixture(scope="module")
def set_tile():
    visual.tile_view_limit = 5


@pytest.fixture(scope="module")
def set_list():
    visual.list_view_limit = 5


@pytest.mark.parametrize('page', cfme_data.get('grid_pages'), scope="module")
def gtest_grid_page_per_item(provider_init, page, set_grid):
    limit = visual.grid_view_limit
    sel.force_navigate(page)
    tb.select('Grid View')
    if int(paginator.rec_total()) >= int(limit):
        assert int(paginator.rec_end()) == int(limit), "Gridview Failed for page {}!".format(page)


@pytest.mark.parametrize('page', cfme_data.get('grid_pages'), scope="module")
def test_tile_page_per_item(provider_init, page, set_tile):
    limit = visual.tile_view_limit
    sel.force_navigate(page)
    tb.select('Tile View')
    if int(paginator.rec_total()) >= int(limit):
        assert int(paginator.rec_end()) == int(limit), "Tileview Failed for page {}!".format(page)


@pytest.mark.parametrize('page', cfme_data.get('grid_pages'), scope="module")
def test_list_page_per_item(provider_init, page, set_list):
    limit = visual.list_view_limit
    sel.force_navigate(page)
    tb.select('List View')
    if int(paginator.rec_total()) >= int(limit):
        assert int(paginator.rec_end()) == int(limit), "Listview Failed for page {}!".format(page)


@pytest.fixture
def set_checkboxes():
    visual.uncheck_checkboxes()


def reset_checkboxes():
    with update(visual):
        visual.infra_provider_quad = True


@pytest.mark.parametrize('page', cfme_data.get('quadicon_pages'), scope="module")
def test_grid_icons_noquads(page, set_checkboxes, request):
    sel.force_navigate(page)
    import pdb
    pdb.set_trace()
    #if(visual.check_noquad_exists):
     #   print "pass"
      #assert visual.check_quad_exists, "Pass"
    name = Quadicon.get_first_quad_title()
    if sel.is_displayed(Quadicon.only_image_visible(name)):
        print Quadicon.only_image_visible(name)
        print sel.is_displayed(Quadicon.only_image_visible(name))
    request.addfinalizer(reset_checkboxes)
