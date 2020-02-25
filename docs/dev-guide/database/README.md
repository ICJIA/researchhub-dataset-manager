# Database Overview

Research Hub Dataset Manager relies on data stored in `/database/database.db` created via SQLite.

## SQLite

![SQLite logo](https://upload.wikimedia.org/wikipedia/commons/3/38/SQLite370.svg)

> _"SQLite is an in-process library that implements a self-contained, serverless, zero-configuration, transactional SQL database engine. [...] SQLite is the most widely deployed database in the world with more applications than we can count, including several high-profile projects."_

The Web Dataset Maintenance Tool uses SQLite as its database engine. SQLite is freely available at [the official SQLite website](https://www.sqlite.org/index.html).

## DB Browser for SQLite

<img :src="$withBase('/assets/img/sqlitebrowser_logo.png')" alt="DB Browser for SQLite logo">

Although a SQLite database file can be accessed and modified programmatically, it is still conveninent to use a graphical tool to browse the database file and make minor changes if needed.

For that, the current documentation recommends DB Browser for SQLite, previously known as SQLite Browser, for a graphical user interface software tool providing a to SQLite database files. It is freely downloadable from [its official website](https://sqlitebrowser.org/), which introduces DB Browser for SQLite as follows:

> _"DB Browser for SQLite is a high quality, visual, open source tool to create, design, and edit database files compatible with SQLite."_

Once DB Browser is downloaded and installed, you can use it to open SQLite database file (`.db`). The following screenshot image shows the graphical user interface to a `.db` file:

<img :src="$withBase('/assets/img/database_1.png')" alt="Screenshot of DB for SQLite GUI">

::: tip TIP
To find more about using the DB Browser for SQLite, visit [its official documentation Wiki pages on GitHub](https://github.com/sqlitebrowser/sqlitebrowser/wiki).
:::
