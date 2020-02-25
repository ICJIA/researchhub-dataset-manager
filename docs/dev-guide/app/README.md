# App Overview

The key component of Research Hub Dataset Manager is a Python command-line app using a custom package written specifically for fuctionalities required by the Dataset Manager.

All Python scripts are located at the subdirectory `/python/`, and the file structure looks like the followiing:

```
/python/
├─ __main__.py
└─ util/
    ├─ __init__.py
    ├─ data/
    ├─ database/
    ├─ dataset/
    ├─ fs/
    └─ ui/
```

- `__main__.py` is the entrypoint for the app.
- `util` is a custom utility package providing supporting functionalities for the app.

::: danger WARNING
Be careful when editing the program files for any reasons, including fixing bugs or adding new datasets. If necessary, first consult the Dataset Manager's original author ([Bobae.Kang@illinois.gov](mailto:Bobae.Kang@illinois.gov)) before implementing any changes.

For experimentation, it is recommended to clone the repository and copy over the `/database/database.db` from its public location at `P:\DATA\`.
:::
