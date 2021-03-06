# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data()
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "title",
			"label": _("Title"),
			"width": "300",
		},
		{
			"label": _("Number of products"),
			"fieldname": "prod_num",
			"align": "left"
		},
	]


def get_data():
	db_name = frappe.conf.get("db_name")

	raw_result = frappe.db.sql("""
	SELECT
		`prj`.`name`
		,`prj`.`title`
		, COUNT(`prod`.`name`) AS `prod_num`
	FROM `{}`.`tabDC_PLC_RND_Project` AS `prj`
	LEFT JOIN `{}`.`tabDC_PLC_Product_Summary` AS `prod`
		ON (`prod`.`link_rnd_project` = `prj`.`name`)
	GROUP BY `prj`.`name`
	ORDER BY `prj`.`title` ASC;""".format(db_name, db_name), as_list=1)

	result = [prepare_rnd_project_filter_row(row) for row in raw_result]

	return result


def prepare_rnd_project_filter_row(data):
	id_, title, number = data
	return ['{}|{}'.format(title, id_), number]
