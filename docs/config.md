# Configuration

Configuration is the same as with [mkdocstrings-python] except that the handler name should be `python_betterrefs`
instead of `python`. Because this handler extends the standard mkdocstrings-python handler, the same options are
available.

Additional options are added by this extension. Currently, there are two:

- **better_crossrefs** - If set to true enables use of better cross-reference syntax provided by this handler
  extension (setting this to false would essentially mimic the `python` handler). This is enabled by default, so you
  shouldn't need to specify it unless you want to disable this behavior.

- **check_crossrefs** - Enables early checking of all cross-references. Note that this option only takes affect if
  **better_crossrefs** is also true. This option is true by default, so you only need to specify it if you wish to
  disable this checking. Checking can also be disabled on a per-case basis by prefixing a reference with '?', e.g.
  `[something][?dontcheckme]`.

!!! Example "mkdocs.yml plugins specification using this handler"

    ```yaml
    plugins:
        - search
        - mkdocstrings:
            default_handler: python_betterrefs
            handlers:
                python_betterrefs:
                    options:
                        docstring_style: google
                        docstring_options:
                            ignore_init_summary: true
                        merge_init_into_class: true
                        better_crossrefs: true
                        check_crossrefs: false
                        separate_signature: true
                        show_source: true
                        show_root_full_path: true
                    inventories:
                        - https://docs.python.org/3/objects.inv
    ```

[mkdocstrings-python]: https://mkdocstrings.github.io/python/
