// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

let check_handle = (o) => {
	let relevant = o.checked;
	let name = o.id;
	frappe.call({
		method: "dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary.set_opcon_relevant",
		args: {
			name: name,
			relevant: relevant ? 1 : 0,
		},
		callback: r => {
			let { date, check } = r.message;
			$('.rel_label_' + name)[0].innerHTML = "&nbsp;&nbsp;" + date;
			o.checked = !!check;
		}
	});
};

frappe.query_reports["DC Product Opcon Stats"] = {
	"filters": [

	],
<<<<<<< Updated upstream
	formatter: frappe.dc_plc.product_link_formatter,
=======
	formatter: frappe.dc_plc.utils.product_link_formatter,
	onload: report => {
		let highlight_cols = [8, 9];
		let sheet = window.document.styleSheets[0];
		highlight_cols.forEach((el) => {
			sheet.insertRule(`.dt-instance-1 .dt-cell--col-${el} { background-color: rgba(255, 252, 29, 0.27); }`, sheet.cssRules.length);
		});
	}
};
