(window.webpackJsonp=window.webpackJsonp||[]).push([[13],{210:function(e,t,a){"use strict";a.r(t);var o=a(28),i=Object(o.a)({},(function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("ContentSlotsDistributor",{attrs:{"slot-key":e.$parent.slotKey}},[a("h1",{attrs:{id:"database-tables"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#database-tables"}},[e._v("#")]),e._v(" Database Tables")]),e._v(" "),a("p",[e._v("Research Hub Dataset Manager relies on data stored in the /database/database.db file, which contains a number of tables listed below.")]),e._v(" "),a("div",{staticClass:"custom-block warning"},[a("p",{staticClass:"custom-block-title"},[e._v("NOTE")]),e._v(" "),a("p",[e._v("The Tool's database structure is drawn from the one used in the previous datasets maintenance practice. Accoringly, there are tables or columns that appear somewhat redundant or unused. This may change in future.")])]),e._v(" "),a("h2",{attrs:{id:"bridgepop"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#bridgepop"}},[e._v("#")]),e._v(" BridgePop")]),e._v(" "),a("p",[e._v('The "BridgePop" table contains records drawn from '),a("a",{attrs:{href:"https://www.cdc.gov/nchs/nvss/bridged_race.htm",target:"_blank",rel:"noopener noreferrer"}},[e._v("U.S. Census Populations With Bridged Race Categories"),a("OutboundLink")],1),e._v(" by the National Vial Statistics System. The records are in a disaggregated format--by year, county, bridged race group and gender, ethnicity (hispanic or not), and age--as in the original format. Records in this table are used for obtaining the population base for calculating the relevant rates in the dataset outputs.")]),e._v(" "),a("p",[e._v('The "BridgePop" table has the following columns:')]),e._v(" "),a("ul",[a("li",[a("code",[e._v("year")]),e._v(" (INTEGER): Year of each record.")]),e._v(" "),a("li",[a("code",[e._v("fk_population_county")]),e._v(' (INTEGER): A foreign key to the "County" table.')]),e._v(" "),a("li",[a("code",[e._v("age")]),e._v(" (INTEGER): .")]),e._v(" "),a("li",[a("code",[e._v("race_gender")]),e._v(" (INTEGER): .")]),e._v(" "),a("li",[a("code",[e._v("hispanic")]),e._v(" (INTEGER): .")]),e._v(" "),a("li",[a("code",[e._v("value")]),e._v(" (INTEGER): Data value.")])]),e._v(" "),a("h2",{attrs:{id:"bridgepopold"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#bridgepopold"}},[e._v("#")]),e._v(" BridgePopOld")]),e._v(" "),a("p",[e._v('The "BridgePopOld" table contains aggregated records drawn from '),a("a",{attrs:{href:"https://www.cdc.gov/nchs/nvss/bridged_race.htm",target:"_blank",rel:"noopener noreferrer"}},[e._v("U.S. Census Populations With Bridged Race Categories"),a("OutboundLink")],1),e._v(" by the National Vial Statistics System--in an old. The table is no longer maintained beyond the 2016 population estimates.")]),e._v(" "),a("p",[e._v('The "BridgePopOld" table has the following columns:')]),e._v(" "),a("ul",[a("li",[a("code",[e._v("fk_bridgepop_county")]),e._v(' (INTEGER): A foreign key to the "County" table.')]),e._v(" "),a("li",[a("code",[e._v("year")]),e._v(" (INTEGER): Year of each record.")]),e._v(" "),a("li",[a("code",[e._v("fk_bridgepop_typepop")]),e._v(' (INTEGER): A foreign key to the "TypePop" table.')]),e._v(" "),a("li",[a("code",[e._v("value")]),e._v(" (INTEGER): Data value.")])]),e._v(" "),a("h2",{attrs:{id:"county"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#county"}},[e._v("#")]),e._v(" County")]),e._v(" "),a("p",[e._v('The "County" table contains information on Illinois counties and their characteristics.')]),e._v(" "),a("p",[e._v('The "County" table has the following columns:')]),e._v(" "),a("ul",[a("li",[a("code",[e._v("id")]),e._v(" (INTEGER): Unique identifier for each county.")]),e._v(" "),a("li",[a("code",[e._v("fips_number")]),e._v(" (REAL): The Federal Information Process Standard (FIPS) number for each county.")]),e._v(" "),a("li",[a("code",[e._v("county_name")]),e._v(" (TEXT): County name.")]),e._v(" "),a("li",[a("code",[e._v("judicial_circuit")]),e._v(" (TEXT): The Illinois circuit court under whose jurisdiction each county falls.")]),e._v(" "),a("li",[a("code",[e._v("fk_county_typeunit")]),e._v(' (REAL): A foreign key to the "TypeUnit" table.')]),e._v(" "),a("li",[a("code",[e._v("alphabetical_oder")]),e._v(" (REAL): The number of each county in alphebetical order.")]),e._v(" "),a("li",[a("code",[e._v("region")]),e._v(" (TEXT): Region of the county: Northern minus Cook, Northern - Cook, Central, or Southern")]),e._v(" "),a("li",[a("code",[e._v("community_type")]),e._v(' (TEXT): Categorization based on the proportion of rural area in a county: 1) "Completely Rural" means 100% rural, 2) "Mostly rural" means >50% rural, 3) "Mostly urban" means <50% rural, and 4) "Completely urban" means 0% rural')]),e._v(" "),a("li",[a("code",[e._v("percent_rural")]),e._v(" (REAL): Percentage of rural area in a county")])]),e._v(" "),a("h2",{attrs:{id:"countycombined"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#countycombined"}},[e._v("#")]),e._v(" CountyCombined")]),e._v(" "),a("p",[e._v('The "CombinedCounty" table contains information regarding cases in which data for multiple counties are reported by a single county or a separate body of organization.')]),e._v(" "),a("p",[e._v('The "CountyCombined" table has the following columns:')]),e._v(" "),a("ul",[a("li",[a("code",[e._v("id")]),e._v(" (INTEGER): Unique indentifier for combined county records.")]),e._v(" "),a("li",[a("code",[e._v("fk_combinedcounty_indicator")]),e._v(' (INTEGER): A foreign key to the "Indicator" table.')]),e._v(" "),a("li",[a("code",[e._v("year")]),e._v(" (INTEGER): Year when the given combined county record is applicable.")]),e._v(" "),a("li",[a("code",[e._v("fk_container_county")]),e._v(' (INTEGER): A foreign key to the "County" table for the reporting county.')]),e._v(" "),a("li",[a("code",[e._v("fk_contained_county")]),e._v(' (INTEGER): A foreign key to the "County" table for the county reporting its data via another county.')])]),e._v(" "),a("h2",{attrs:{id:"data"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#data"}},[e._v("#")]),e._v(" Data")]),e._v(" "),a("p",[e._v('The "Data" table is a storage for all the actual values from data sources except for the population estimates.')]),e._v(" "),a("p",[e._v('The "Data" table has the following columns:')]),e._v(" "),a("ul",[a("li",[a("code",[e._v("fk_data_variable")]),e._v(' (INTEGER): A foreign key to the "Variable" table.')]),e._v(" "),a("li",[a("code",[e._v("fk_data_county")]),e._v(' (INTEGER): A foreign key to the "County" table.')]),e._v(" "),a("li",[a("code",[e._v("year")]),e._v(" (INTEGER): Year of each record.")]),e._v(" "),a("li",[a("code",[e._v("value")]),e._v(" (REAL): Data value.")])]),e._v(" "),a("h2",{attrs:{id:"dataset"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#dataset"}},[e._v("#")]),e._v(" Dataset")]),e._v(" "),a("p",[e._v('The "Dataset" table contains information about each dataset output, including the information that will be saved as its metadata file.')]),e._v(" "),a("p",[e._v('The "Dataset" table has the following columns:')]),e._v(" "),a("ul",[a("li",[a("code",[e._v("id")]),e._v(" (INTEGER): Unique identifier for each output table.")]),e._v(" "),a("li",[a("code",[e._v("source_group")]),e._v(" (INTEGER): Source group of each output table: 1 is AOIC, 2 is CHRI, 3 is IDOC, 4 is IDJJ, 5 is ISP, and 6 is others.")]),e._v(" "),a("li",[a("code",[e._v("name")]),e._v(" (TEXT): Name of each output table (as in the resulting "),a("code",[e._v(".csv")]),e._v(" file).")]),e._v(" "),a("li",[a("code",[e._v("old_name")]),e._v(" (TEXT): Name of each output table as in the previous dataset maintenance system.")]),e._v(" "),a("li",[a("code",[e._v("standard")]),e._v(" (INTEGER): 1 if the table is in the standard format, 0 otherwise.")]),e._v(" "),a("li",[a("code",[e._v("active")]),e._v(" (INTEGER): 1 if the table is actively maintained, 0 otherwise.")]),e._v(" "),a("li",[a("code",[e._v("fk_output_package")]),e._v(' (INTEGER): A foreign key to the "Package" table.')]),e._v(" "),a("li",[a("code",[e._v("name_full")]),e._v(" (TEXT): Full name of each output table; included in the metadata.")]),e._v(" "),a("li",[a("code",[e._v("source")]),e._v(" (TEXT): Output data source.")]),e._v(" "),a("li",[a("code",[e._v("year_type")]),e._v(" (TEXT): Type of year: Calandar or Fiscal; included in the metadata.")]),e._v(" "),a("li",[a("code",[e._v("year_min")]),e._v(" (REAL): Minimum year value (for the earliest records); included in the metadata.")]),e._v(" "),a("li",[a("code",[e._v("year_max")]),e._v(" (REAL): Maximum year value (for the latest records); included in the metadata.")]),e._v(" "),a("li",[a("code",[e._v("description")]),e._v(" (TEXT): Description of each output; included in the metadata.")]),e._v(" "),a("li",[a("code",[e._v("notes")]),e._v(" (TEXT): Notes for each output; included in the metadata file.")]),e._v(" "),a("li",[a("code",[e._v("column_name")]),e._v(" (TEXT): A list of column names; included in the metadata.")]),e._v(" "),a("li",[a("code",[e._v("column_info")]),e._v(" (TEXT): A list of column descriptions; included in the metadata.")])]),e._v(" "),a("h2",{attrs:{id:"typerate"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#typerate"}},[e._v("#")]),e._v(" TypeRate")]),e._v(" "),a("p",[e._v('The "TypeRate" table is a simple lookup table for bases to calculate rate.')]),e._v(" "),a("p",[e._v('The "TypeRate" table has the following columns:')]),e._v(" "),a("ul",[a("li",[a("code",[e._v("id")]),e._v(" (INTEGER): Unique identifier for each rate base.")]),e._v(" "),a("li",[a("code",[e._v("description")]),e._v(" (TEXT): Description of each rate base.")])]),e._v(" "),a("h2",{attrs:{id:"typepop"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#typepop"}},[e._v("#")]),e._v(" TypePop")]),e._v(" "),a("p",[e._v('The "TypePop" table is a simple lookup table for age groups for aggregating population counts.')]),e._v(" "),a("p",[e._v('The "TypePop" table has the following columns:')]),e._v(" "),a("ul",[a("li",[a("code",[e._v("id")]),e._v(" (INTEGER): Unique indentifier for each age group.")]),e._v(" "),a("li",[a("code",[e._v("description")]),e._v(" (TEXT): Description of each age group.")])]),e._v(" "),a("h2",{attrs:{id:"typeunit"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#typeunit"}},[e._v("#")]),e._v(" TypeUnit")]),e._v(" "),a("p",[e._v('The "TypeUnit" table is a simple lookup table for geographcal units.')]),e._v(" "),a("p",[e._v('The "TypeUnit" table has the following columns:')]),e._v(" "),a("ul",[a("li",[a("code",[e._v("id")]),e._v(" (INTEGER): Unique indentifier for each geography unit.")]),e._v(" "),a("li",[a("code",[e._v("description")]),e._v(" (TEXT): Description of each geography unit.")])]),e._v(" "),a("h2",{attrs:{id:"variable"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#variable"}},[e._v("#")]),e._v(" Variable")]),e._v(" "),a("p",[e._v('The "Variable" table contains information about each "variable", whose records are collected by the ICJIA and incoporated into its published datasets.')]),e._v(" "),a("p",[e._v('Each variable is given a unique idenetifier. For instance, the indicator number of 10000 corresponds to "count" variable in the Orders of Protection table in the Administration Office of the Illinois Courts\' Annual Report of the Illinois Courts.')]),e._v(" "),a("div",{staticClass:"custom-block warning"},[a("p",{staticClass:"custom-block-title"},[e._v("NOTE")]),e._v(" "),a("p",[e._v("See "),a("RouterLink",{attrs:{to:"/dev-guide/sources.html"}},[e._v('the "Data Sources" page')]),e._v(" in the Guide for the link between variables and their sources.")],1)]),e._v(" "),a("p",[e._v('The "Variable" table has the following columns:')]),e._v(" "),a("ul",[a("li",[a("code",[e._v("id")]),e._v(" (INTEGER): Unique identifier for each variable.")]),e._v(" "),a("li",[a("code",[e._v("name")]),e._v(" (TEXT): Variable name")]),e._v(" "),a("li",[a("code",[e._v("definition")]),e._v(" (TEXT): Brief definition of each variable.")]),e._v(" "),a("li",[a("code",[e._v("fk_variable_dataset")]),e._v(' (INTEGER): A foreign key to the "Dataset" table.')]),e._v(" "),a("li",[a("code",[e._v("fk_variable_typepop")]),e._v(' (TEXT): A foreign key to the "TypePop" table.')]),e._v(" "),a("li",[a("code",[e._v("fk_variable_typerate")]),e._v(' (INTEGER): A foreign key to the "TypeRate" table.')])])])}),[],!1,null,null,null);t.default=i.exports}}]);