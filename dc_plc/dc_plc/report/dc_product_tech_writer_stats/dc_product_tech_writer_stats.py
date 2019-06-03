# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from dc_plc.custom.utils import add_product_summary_links, add_translation

def execute(filters=None):
	columns = get_columns()
	data = get_data()
	return columns, data


def get_columns():
	# return ["#:Data:50", _("Product") + ":Link/DC_PLC_Product_Summary:200", _("Type") + ":Link/PLC_Product_Type:100"]
	return [
		"ID:Link/DC_PLC_Product_Summary",
		_("External number"),
		_("Internal number"),
		_("Description"),
		_("Specs"),
		_("Analogs"),
		_("Reports"),
		_("Datasheet")
	]


def get_data():

	db_name = frappe.conf.get("db_name")
	host = frappe.utils.get_url()

	result = frappe.db.sql("""SELECT
  p.name as `id`
     , p.ext_num
     , p.int_num
     , p.description
     , p.specs
     , p.analog
     , p.report
     , p.datasheet
FROM `{}`.tabDC_PLC_Product_Summary AS p;""".format(db_name), as_list=1)

	return [add_product_summary_links(row, host) for row in result]
