import frappe


# TODO properly escape filter items
def get_full_stats(filters):
	db_name = frappe.conf.get('db_name')

	sql = f"""SELECT
	`p`.`name` as `id`
	, CONCAT(`mile`.`index`, '.', `stage`.`index`, '.', `step`.`index`, ' ', `step`.`title`) AS `step` 
	, `p`.`ext_num`
	, `p`.`int_num`
	, `letter`.`title` AS `letter`
	, `type`.`title` AS `type`
	, `proj`.`title` AS `project`
	, "stub" AS `cons`
	, "stub" AS `devs`
	, `p`.`chip`
	, `p`.`asm_board`
	, `pak`.`title` AS `package`
	, `fun`.`title` AS `function`
	, `p`.`application`
	, `p`.`description`
	, `p`.`specs`
	, `p`.`analog`
	, `p`.`desdoc_num`
	, `p`.`opcon`
	, `p`.`process_map`
	, `p`.`report`
	, `p`.`datasheet`
	, `p`.`final_description`
	, `p`.`rel_check_dept_head`
	, `p`.`rel_check_rnd_spec`
	, `p`.`rel_check_developer`
	, `p`.`rel_check_opcon`
	, `p`.`rel_check_procmap`
	, `p`.`rel_check_tech_writer`
	, `p`.`rel_check_desdoc`
	FROM `{db_name}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_Product_Step` AS `step` ON `p`.`link_step` = `step`.`name`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_Product_Stage` AS `stage` ON `step`.`link_stage` = `stage`.`name`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_Product_Milestone` AS `mile` ON `stage`.`link_milestone` = `mile`.`name`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_Product_Letter` AS `letter` ON `p`.`link_letter` = `letter`.`name`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_Product_Type` AS `type` ON `p`.`link_type` = `type`.`name`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
	LEFt JOIN
		`{db_name}`.`tabDC_PLC_Package` AS `pak` ON `p`.`link_package` = `pak`.`name`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`
	LEFT OUTER JOIN
		`{db_name}`.`tabDC_PLC_Developers_in_Product` AS `dev` ON `p`.`name` = `dev`.`parent`"""

	if filters:
		proj = filters.get('link_rnd_project', '%')
		proj_clause = "(`proj`.`name` LIKE '%' OR `proj`.`name` IS NULL)" if proj == '%' else f"`proj`.`name` LIKE '{proj}'"

		type_ = filters.get('link_type', '%')
		type_clause = "(`type`.`name` LIKE '%' OR `type`.`name` IS NULL)" if type_ == '%' else f"`type`.`name` LIKE '{type_}'"

		letter = filters.get('link_letter', '%')
		model_clause = "(`p`.`link_letter` LIKE '%' OR `p`.link_letter IS NULL)" if letter == '%' else f"`p`.`link_letter` LIKE '{letter}'"

		func = filters.get('link_function', '%')
		func_clause = "(`fun`.`name` LIKE '%' OR `fun`.`name` IS NULL)" if func == '%' else f"`fun`.`name` LIKE '{func}'"

		pack = filters.get('link_package', '%')
		pack_clause = "(`pak`.`name` LIKE '%' OR `pak`.`name` IS NULL)" if pack == '%' else f"`pak`.`name` LIKE '{pack}'"

		dev = filters.get('developer', '%')
		if dev == 'HR-EMP-00094':
			dev_clause = "`dev`.`link_employee` IS NULL"
		else:
			dev_clause = "(`dev`.`link_employee` LIKE '%' OR `dev`.`link_employee` IS NULL)" if dev == '%' else f"`dev`.`link_employee` LIKE '{dev}'"

		sql += f"""
	WHERE
	{proj_clause}
	AND
	{type_clause}
	AND
	{model_clause}
	AND
	{func_clause}
	AND
	{pack_clause}
	AND
	{dev_clause}
	"""

	sql += "GROUP BY `p`.`name` ORDER BY `id`"

	return frappe.db.sql(sql + ';', as_list=1)


def get_developers_for_product():
	db_name = frappe.conf.get('db_name')
	sql = """SELECT t.parent,
GROUP_CONCAT(CONCAT(emp.last_name, " ", emp.first_name, " ", emp.middle_name)) AS developers
FROM `{}`.`tabDC_PLC_Developers_in_Product` AS t
INNER JOIN `{}`.`tabEmployee` AS emp
ON t.link_employee = emp.employee
GROUP BY t.parent;""".format(db_name, db_name)
	return {res[0]: res[1] for res in frappe.db.sql(sql, as_list=1)}


def get_consultants_for_product():
	db_name = frappe.conf.get('db_name')
	sql = """SELECT t.parent,
GROUP_CONCAT(CONCAT(emp.last_name, " ", emp.first_name, " ", emp.middle_name)) AS developers
FROM `{}`.tabDC_PLC_Consulants_in_Product AS t
INNER JOIN `{}`.`tabEmployee` AS emp
ON t.link_employee = emp.employee
GROUP BY t.parent;""".format(db_name, db_name)
	return {res[0]: res[1] for res in frappe.db.sql(sql, as_list=1)}


def get_dept_head_stats(filters):
	db_name = frappe.conf.get('db_name')

	sql = f"""SELECT
	`p`.`name` as `id`
	, CONCAT(`mil`.`index`, '.', `stage`.`index`, '.', `step`.`index`, ' ', `step`.`title`) AS `step`
	, `proj`.`title` AS `project`
	, "stub" AS `cons`
	, "stub" AS `devs`
	, `fun`.`title` AS `function`
	, `p`.`description`
	, `p`.`ext_num`
	, `p`.`int_num` 
	, `p`.`rel_check_dept_head`
	, `p`.`rel_date_dept_head`
	FROM `{db_name}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_Product_Step` AS `step` ON `p`.`link_step` = `step`.`name`
	LEFT JOIN 
		`{db_name}`.`tabDC_PLC_Product_Stage` AS `stage` ON `stage`.`name` = `step`.`link_stage`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_Product_Milestone` AS `mil` ON `mil`.`name` = `stage`.`link_milestone`
"""

	if filters:
		step = filters.get('link_step', '%')
		step_clause = f"(`step`.`name` LIKE '%' OR `p`.`link_step` IS NULL)" if step == '%' else f"`p`.`link_step` = '{step}'"

		sql += f"""
		WHERE
			{step_clause}
		"""

	sql += 'GROUP BY `p`.`name` ORDER BY `id`'

	return frappe.db.sql(sql + ';', as_list=1)


def get_rnd_spec_stats(filters):
	db_name = frappe.conf.get('db_name')

	sql = f"""SELECT
	`p`.`name` AS `id`
	, CONCAT(`mile`.`index`, '.', `stage`.`index`, '.', `step`.`index`, ' ', `step`.`title`) AS `step`
	, `proj`.`title` AS `project`
	, `letter`.`title` AS `letter`
	, `func`.`title` AS `function`
	, `p`.`ext_num`
	, `p`.`int_num`
	, `p`.`rel_check_rnd_spec`
	, `p`.`rel_date_rnd_spec`
	FROM `{db_name}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_Product_Function` AS `func` ON `p`.`link_function` = `func`.`name`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_Product_Letter` AS `letter` ON `p`.`link_letter` = `letter`.`name`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_Product_Step` AS `step` ON `p`.`link_step` = `step`.`name`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_Product_Stage` AS `stage` ON `step`.`link_stage` = `stage`.`name`
	LEFT JOIN
		`{db_name}`.`tabDC_PLC_Product_Milestone` AS `mile` ON `stage`.`link_milestone` = `mile`.`name`;"""
	return frappe.db.sql(sql + ";", as_list=1)


def get_developer_stats(filters):
	db_name = frappe.conf.get('db_name')

	sql = """SELECT
	`p`.`name` as `id`
	, `proj`.`title` AS `project`
	, "stub"
	, "stub"
	, `type`.`title` AS `type`
	, `letter`.`title` AS `letter`
	, `fun`.`title` AS `function`
	, `p`.`chip`
	, `p`.`asm_board`
	, `pak`.`title` AS `package`
	, `p`.`description`
	, `p`.`specs`
	, `p`.`report`
	, `p`.`analog`
	, `p`.`ext_num`
	, `p`.`int_num`
	, `p`.`rel_check_dept_head`
	, `p`.`rel_check_developer`
	, `p`.`rel_date_developer`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Type` AS `type` ON `p`.`link_type` = `type`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Letter` AS `letter` ON `p`.`link_letter` = `letter`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Package` AS `pak` ON `p`.`link_package` = `pak`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`
	LEFT OUTER JOIN
		`{}`.`tabDC_PLC_Developers_in_Product` AS `dev` ON `p`.`name` = `dev`.`parent`
	LEFT OUTER JOIN
		`{}`.`tabDC_PLC_Consulants_in_Product` AS `con` ON `p`.`name` = `con`.`parent`
		""".format(db_name, db_name, db_name, db_name, db_name, db_name, db_name, db_name)

	if filters:
		dev = filters.get('developer', '%')
		con = filters.get('consultant', '%')
		if dev == 'HR-EMP-00094':
			dev_clause = "`dev`.`link_employee` IS NULL"
		else:
			dev_clause = "(`dev`.`link_employee` LIKE '%' OR `dev`.`link_employee` IS NULL)" if dev == '%' else "`dev`.`link_employee` LIKE '{}'".format(dev)
		if con == 'HR-EMP-00094':
			cons_clause = "`con`.`link_employee` IS NULL"
		else:
			cons_clause = "(`con`.`link_employee` LIKE '%' OR `con`.`link_employee` IS NULL)" if con == '%' else "`con`.`link_employee` LIKE '{}'".format(con)

		sql += """
	WHERE
	{}
	AND
	{}
	""".format(dev_clause, cons_clause)

	sql += "GROUP BY `p`.`name` ORDER BY `id`"

	return frappe.db.sql(sql + ";", as_list=1)


def get_opcon_stats(filters):
	db_name = frappe.conf.get('db_name')

	sql = """SELECT
	`p`.`name` as `id`
	, `proj`.`title` AS `project`
	, `type`.`title` AS `type`
	, `letter`.`title` AS `letter`
	, `fun`.`title` AS `function`
	, `p`.`ext_num`
	, `p`.`opcon`
	, `p`.`int_num`
	, `p`.`rel_check_opcon`
	, `p`.`rel_date_opcon`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Type` AS `type` ON `p`.`link_type` = `type`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Letter` AS `letter` ON `p`.`link_letter` = `letter`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Package` AS `pak` ON `p`.`link_package` = `pak`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`;""".format(db_name, db_name, db_name, db_name, db_name, db_name)

	return frappe.db.sql(sql + ";", as_list=1)


def get_procmap_stats(filters):
	db_name = frappe.conf.get('db_name')

	sql = """SELECT
	`p`.`name` as `id`
	, `proj`.`title` AS `project`
	, `fun`.`title` AS `function`
	, `p`.`ext_num`
	, `p`.`process_map`
	, `p`.`opcon`
	, `p`.`int_num`
	, `p`.`rel_check_procmap`
	, `p`.`rel_date_procmap`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`;""".format(db_name, db_name, db_name)

	return frappe.db.sql(sql + ";", as_list=1)


def get_tech_writer_stats(filters):
	db_name = frappe.conf.get('db_name')

	sql = """SELECT
	`p`.`name` AS `id`
	, `fun`.`title` AS `function`
	, `pack`.`title` AS `package`
	, `p`.`description`
	, `p`.`specs`
	, `p`.`report`
	, `p`.`analog`
	, `p`.`ext_num`
	, `p`.`int_num`
	, `p`.`application`
	, `p`.`datasheet`
	, `p`.`final_description`
	, `p`.`rel_check_tech_writer`
	, `p`.`rel_date_tech_writer`
	FROM `{}`.tabDC_PLC_Product_Summary AS p
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`
	LEFt JOIN
		`{}`.`tabDC_PLC_Package` AS `pack` ON `p`.`link_package` = `pack`.`name`;""".format(db_name, db_name, db_name)

	return frappe.db.sql(sql + ";", as_list=1)


def get_desdoc_stats(filters):
	db_name = frappe.conf.get('db_name')

	sql = """SELECT
	`p`.`name` AS `id`
	, `proj`.`title` AS `porject`
	, `type`.`title` AS `type`
	, `fun`.`title` AS `function`
	, `p`.`ext_num`
	, `p`.`opcon`
	, `p`.`int_num`
	, `p`.`desdoc_num`
	, `p`.`rel_check_desdoc`
	, `p`.`rel_date_desdoc`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.`link_rnd_project` = `proj`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Type` AS `type` ON `p`.`link_type` = `type`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`;""".format(db_name, db_name, db_name, db_name)

	return frappe.db.sql(sql + ";", as_list=1)

