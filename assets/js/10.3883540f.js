(window.webpackJsonp=window.webpackJsonp||[]).push([[10],{254:function(t,s,a){"use strict";a.r(s);var e=a(28),n=Object(e.a)({},(function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("ContentSlotsDistributor",{attrs:{"slot-key":t.$parent.slotKey}},[a("h1",{attrs:{id:"main-py"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#main-py"}},[t._v("#")]),t._v(" "),a("code",[t._v("__main__.py")])]),t._v(" "),a("p",[a("code",[t._v("__main__.py")]),t._v(" is the entrypoint script for the Python app. It defines and runs the "),a("code",[t._v("main()")]),t._v(" function which contains the core business logic of Research Hub Dataset Manager.")]),t._v(" "),a("h2",{attrs:{id:"main"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#main"}},[t._v("#")]),t._v(" "),a("code",[t._v("main()")])]),t._v(" "),a("p",[t._v("The body of "),a("code",[t._v("main()")]),t._v(" looks like the following:")]),t._v(" "),a("div",{staticClass:"language-python extra-class"},[a("pre",{pre:!0,attrs:{class:"language-python"}},[a("code",[a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("def")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token function"}},[t._v("main")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v("\n    reset_env"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("exit"),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),a("span",{pre:!0,attrs:{class:"token boolean"}},[t._v("False")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n\n    welcome_msg "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"\\n### WELCOME TO ICJIA WEB DATASET MAINTENANCE TOOL ###"')]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("+")]),t._v("\\\n        "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v("\"\\n\\nYou can safely exit this program by typing 'q' and\"")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("+")]),t._v("\\\n        "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"  press Enter whenever asked for your input."')]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("+")]),t._v("\\\n        "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"\\n***WARNING: Trying to forcibly quit the program might cause"')]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("+")]),t._v("\\\n        "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('" unexpected problems.***"')]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("+")]),t._v("\\\n        "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"\\n"')]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("print")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("welcome_msg"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n\n    "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("while")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token boolean"}},[t._v("True")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v("\n        task_code "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" prompt_for_task_input"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n\n        "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("if")]),t._v(" task_code "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("==")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v("'1'")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v("\n            taks_result "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" task_data"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n        "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("elif")]),t._v(" task_code "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("==")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v("'2'")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v("\n            taks_result "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" task_population"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n        "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("elif")]),t._v(" task_code "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("==")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v("'3'")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v("\n            taks_result "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" task_dataset"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n\n        handle_task_result"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("taks_result"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n")])])]),a("h2",{attrs:{id:"imported-util-functions"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#imported-util-functions"}},[t._v("#")]),t._v(" Imported "),a("code",[t._v("util")]),t._v(" functions")]),t._v(" "),a("p",[a("code",[t._v("__main__.py")]),t._v(" also imports the following functions from the "),a("code",[t._v("util")]),t._v(" package:")]),t._v(" "),a("div",{staticClass:"language-python extra-class"},[a("pre",{pre:!0,attrs:{class:"language-python"}},[a("code",[a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("from")]),t._v(" util "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("import")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("\n  handle_task_result"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n  prompt_for_task_input"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n  reset_env"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n  task_data"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n  task_dataset"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n  task_population\n"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n")])])]),a("ul",[a("li",[a("code",[t._v("handle_task_result")]),t._v(" "),a("ul",[a("li",[t._v("Receive the task result and take appropriate actions based on the result (e.g. if success, print success message and ask whether to continue working on a new task).")]),t._v(" "),a("li",[t._v("Defined in "),a("code",[t._v("util.ui.main")]),t._v(".")])])]),t._v(" "),a("li",[a("code",[t._v("prompt_for_task_input")]),t._v(" "),a("ul",[a("li",[t._v("Prompt the user to provide input specifying which task to carry out. Possible inputs include "),a("code",[t._v("1")]),t._v(' for updating "Data", '),a("code",[t._v("2")]),t._v(' for updating "BridgePop", '),a("code",[t._v("3")]),t._v(" for generating datasets, and "),a("code",[t._v("q")]),t._v(" for exiting the program.")]),t._v(" "),a("li",[t._v("Defined in "),a("code",[t._v("util.ui.prompt")]),t._v(".")])])]),t._v(" "),a("li",[a("code",[t._v("reset_env")]),t._v(" "),a("ul",[a("li",[t._v("Reset the environment by cleaning out all temporary outputs. If the "),a("code",[t._v("exit")]),t._v(" input is "),a("code",[t._v("True")]),t._v(", an exit message will be printed out at the end.")]),t._v(" "),a("li",[t._v("Defined in "),a("code",[t._v("util.ui.main")]),t._v(".")])])]),t._v(" "),a("li",[a("code",[t._v("task_data")]),t._v(" "),a("ul",[a("li",[t._v('Implement business logic for updating the "Data" table in the database. Return '),a("code",[t._v("True")]),t._v(" if the task is successfully carried out, return "),a("code",[t._v("False")]),t._v(" otherwise.")]),t._v(" "),a("li",[t._v("Defined in "),a("code",[t._v("util.ui.main")]),t._v(".")])])]),t._v(" "),a("li",[a("code",[t._v("task_dataset")]),t._v(" "),a("ul",[a("li",[t._v("Implement business logic for generating packaged dataset products using data stored in the database. Return "),a("code",[t._v("True")]),t._v(" if the task is successfully carried out, return "),a("code",[t._v("False")]),t._v(" otherwise.")]),t._v(" "),a("li",[t._v("Defined in "),a("code",[t._v("util.ui.main")]),t._v(".")])])]),t._v(" "),a("li",[a("code",[t._v("task_population")]),t._v(" "),a("ul",[a("li",[t._v('Implement business logic for updating the "BridgePop" table in the database. Return '),a("code",[t._v("True")]),t._v(" if the task is successfully carried out, return "),a("code",[t._v("False")]),t._v(" otherwise.")]),t._v(" "),a("li",[t._v("Defined in "),a("code",[t._v("util.ui.main")]),t._v(".")])])])])])}),[],!1,null,null,null);s.default=n.exports}}]);