// Copyright (c) 2019, igrekus and contributors
// For license information, please see license.txt

let value_or_none = frappe.dc_plc.utils.value_or_none;
let set_field_title = frappe.dc_plc.utils.ui.set_field_title;
let set_info_field = frappe.dc_plc.utils.ui.set_info_field;
let render_info_field = frappe.dc_plc.utils.ui.render_info_field;
let render_field_title = frappe.dc_plc.utils.ui.render_field_title;


frappe.ui.form.on('DC_PLC_Product_Step', {
	refresh: function(frm) {
		set_field_title(frm, 'link_stage');
		set_field_title(frm, 'link_status');
	},

	link_stage: frm => {
		let field = 'link_stage';
		frappe.db.get_doc(frm.fields_dict[field].df.options, frm.fields_dict[field].value).then(result => {
			render_field_title(frm, field, value_or_none(result.title));
		});
	},

	link_status: frm => {
		let field = 'link_status';
		frappe.db.get_doc(frm.fields_dict[field].df.options, frm.fields_dict[field].value).then(result => {
			render_field_title(frm, field, value_or_none(result.title));
		});
	},
});
