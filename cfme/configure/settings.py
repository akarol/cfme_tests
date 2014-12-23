# -*- coding: utf-8 -*-

""" Module dealing with Configure/My Setting section."""

from functools import partial
import cfme.fixtures.pytest_selenium as sel
import cfme.web_ui.tabstrip as tabs
import cfme.web_ui.toolbar as tb
from cfme.web_ui import Quadicon, Form, Region, Select, fill, form_buttons, flash, Table
from cfme.web_ui.menu import nav
from utils.update import Updateable


details_page = Region(infoblock_type='detail')

cfg_btn = partial(tb.select, 'Configuration')
timeprofile_table = Table("//div[@id='main_div']//table[@class='style3']")


nav.add_branch(
    'my_settings',
    {
        'my_settings_time_profiles':
        [
            lambda _: tabs.select_tab("Time Profiles"),
            {
                "timeprofile_new":
                lambda _: cfg_btn('Add a new Time Profile'),

                "timeprofile_edit":
                lambda ctx: timeprofile_table.click_cell("description", ctx.description),

            }
        ],
        'my_settings_visual': [lambda _: tabs.select_tab("Visual"), {}],
        'my_settings_default_filters': [lambda _: tabs.select_tab("Default Filters"), {}],
        'my_settings_default_views': [lambda _: tabs.select_tab("Default Views"), {}],
    }
)


class Timeprofile(Updateable):
    timeprofile_form = Form(
        fields=[
            ("description", "//input[@id='description']"),
            ("scope", Select("//select[@id='profile_type']")),
            ("timezone", Select("//select[@id='profile_tz']")),
            ("days", "//input[@id='all_days']"),
            ("hours", "//input[@id='all_hours']"),
        ]
    )

    save_button = form_buttons.FormButton("Add this Time Profile")

    def __init__(self, description=None, scope=None, days=None, hours=None, timezone=None):
        self.description = description
        self.scope = scope
        self.days = days
        self.hours = hours
        self.timezone = timezone

    def create(self):
        sel.force_navigate('timeprofile_new')
        fill(self.timeprofile_form, {'description': self.description,
                                     'scope': self.scope,
                                     'days': self.days,
                                     'hours': self.hours,
                                     'timezone': self.timezone,
                                     },
             action=self.save_button)
        flash.assert_success_message('Time Profile "{}" was added'.format(self.description))

    def update(self, updates):
        sel.force_navigate("timeprofile_edit", context=self)
        fill(self.timeprofile_form, {'description': updates.get('description'),
                                     'scope': updates.get('scope'),
                                     'timezone': updates.get('timezone')},
             action=form_buttons.save)
        flash.assert_success_message(
            'Time Profile "{}" was saved'.format(updates.get('description', self.description)))

    def copy(self):
        sel.force_navigate("my_settings_time_profiles")
        row = timeprofile_table.find_row_by_cells({'description': self.description})
        sel.check(sel.element(".//input[@type='checkbox']", root=row[0]))
        cfg_btn('Copy selected Time Profile')
        new_timeprofile = Timeprofile(description=self.description + "copy",
                         scope=self.scope)
        fill(self.timeprofile_form, {'description': new_timeprofile.description,
                              'scope': new_timeprofile.scope},
             action=self.save_button)
        flash.assert_success_message(
            'Time Profile "{}" was added'.format(new_timeprofile.description))
        return new_timeprofile

    def delete(self):
        sel.force_navigate("my_settings_time_profiles")
        row = timeprofile_table.find_row_by_cells({'description': self.description})
        sel.check(sel.element(".//input[@type='checkbox']", root=row[0]))
        cfg_btn('Delete selected Time Profiles', invokes_alert=True)
        sel.handle_alert()
        flash.assert_success_message(
            'Time Profile "{}": Delete successful'.format(self.description))


class Visual(Updateable):

    pretty_attrs = ['name']

    item_form = Form(
        fields=[
            ('grid_view', Select('//select[@id="perpage_grid"]')),
            ('tile_view', Select('//select[@id="perpage_tile"]')),
            ('list_view', Select('//select[@id="perpage_list"]')),
            ('reports', Select('//select[@id="perpage_reports"]')),
        ])

    quadicons_form = Form(
        fields=[
            ('infra_provider_quad', "//input[@id='quadicons_ems']"),
            ('cloud_provider_quad', "//input[@id='quadicons_ems_cloud']"),
            ('host_quad', "//input[@id='quadicons_host']"),
            ('datastore_quad', "//input[@id='quadicons_storage']"),
            ('datastoreitem_quad', "//input[@id='quadicons_storageitem']"),
            ('vm_quad', "//input[@id='quadicons_vm']"),
            ('vmitem_quad', "//input[@id='quadicons_vmitem']"),
            ('template_quad', "//input[@id='quadicons_miq_template']"),
        ])

    save_button = form_buttons.FormButton("Add this Time Profile")

    def __init__(self, grid_view=None, tile_view=None, list_view=None,
                infra_provider_quad=False, cloud_provider_quad=False,
                host_quad=False, datastore_quad=False, datastoreitem_quad=False,
                vm_quad=False, vmitem_quad=False, template_quad=False):
        self.grid_view = grid_view
        self.tile_view = tile_view
        self.list_view = list_view
        self.infra_provider_quad = infra_provider_quad
        self.cloud_provider_quad = cloud_provider_quad
        self.host_quad = host_quad
        self.datastore_quad = datastore_quad
        self.datastoreitem_quad = datastoreitem_quad
        self.vm_quad = vm_quad
        self.vmitem_quad = vmitem_quad
        self.template_quad = template_quad

    @property
    def grid_view_limit(self):
        sel.force_navigate("my_settings_visual")
        return int(sel.text(self.item_form.grid_view.first_selected_option))

    @grid_view_limit.setter
    def grid_view_limit(self, value):
        sel.force_navigate("my_settings_visual")
        fill(self.item_form.grid_view, str(value))
        sel.click(form_buttons.save)

    @property
    def tile_view_limit(self):
        sel.force_navigate("my_settings_visual")
        return int(sel.text(self.item_form.tile_view.first_selected_option))

    @tile_view_limit.setter
    def tile_view_limit(self, value):
        sel.force_navigate("my_settings_visual")
        fill(self.item_form.tile_view, str(value))
        sel.click(form_buttons.save)

    @property
    def list_view_limit(self):
        sel.force_navigate("my_settings_visual")
        return int(sel.text(self.item_form.list_view.first_selected_option))

    @list_view_limit.setter
    def list_view_limit(self, value):
        sel.force_navigate("my_settings_visual")
        fill(self.item_form.list_view, str(value))
        sel.click(form_buttons.save)

    def update(self, updates):
        sel.force_navigate("my_settings_visual", context=self)
        fill(self.quadicons_form, {'infra_provider_quad': updates.get('infra_provider_quad'),
                                   'cloud_provider_quad': updates.get('cloud_provider_quad'),
                                   'host_quad': updates.get('host_quad'),
                                   'datastore_quad': updates.get('datastore_quad'),
                                   'datastoreitem_quad': updates.get('datastoreitem_quad'),
                                   'vm_quad': updates.get('vm_quad'),
                                   'vmitem_quad': updates.get('vmitem_quad'),
                                   'template_quad': updates.get('template_quad')})
        sel.click(form_buttons.save)

    def uncheck_checkboxes(self):
        sel.force_navigate("my_settings_visual")
        fill(self.quadicons_form, {'infra_provider_quad': self.infra_provider_quad,
                                   'cloud_provider_quad': self.cloud_provider_quad,
                                   'host_quad': self.host_quad,
                                   'datastore_quad': self.datastore_quad,
                                   'datastoreitem_quad': self.datastoreitem_quad,
                                   'vm_quad': self.vm_quad,
                                   'vmitem_quad': self.vmitem_quad,
                                   'template_quad': self.template_quad})
        sel.click(form_buttons.save)

    def check_noquad_exists(self):
        #locator = ("//div[@id='quadicon']/../../../tr/td/a/../img")
        #if sel.is_displayed(locator):
          #  return True

        sel.force_navigate("")
        name = Quadicon.get_first_quad_title()
        import pdb
        pdb.set_trace()
        if sel.is_displayed(Quadicon.only_image_visible(name)):
            return True

visual = Visual()
