# Versioning

!!! danger "Pre-release phase"

    `mkdocstrings-python-betterrefs` is currently in the pre-release phase (pre v1.0.0). During this phase, these
    guarantees will NOT be followed! This means that **breaking changes can occur in minor version bumps**. That said,
    micro version bumps are still strictly for bugfixes, and will not include any features or breaking changes.

This library follows [semantic versioning model][semver], which means the major version is updated every time
there is an incompatible (breaking) change made to the public API.

In our case, the public API refers to the cross-reference syntax. A major version bump would therefore mean a
potentially breaking update, requiring you to modify the cross references to be compatible with the new version.

## Examples of Breaking level change (major bump: `vX.0.0`)

We try to avoid breaking changes as much as we can, but it might sometimes be beneficial, especially if it's to resolve
a problem, that people might technically be relying on.

Here are some examples of what constitutes a breaking change:

- Dropping support for the `(m)` syntax, resolving to the current module
- Changing the behavior of a trailing `.` (previously just appending the title text) to now first clean up any markup
  from the title (like bold/italic or code markup)
- Using stricter validation of cross-references (breaking, as new warnings will be produced on xrefs that were
  considered as valid before and didn't produce warnings)
- Dropping support for `?` prefixing references to avoid cross-ref validation, as it's no longer necessary (validation
  now always works, ignoring it should never be needed)
- Removing or renaming a [configuration option][config-option] for the handler (like `check_crossrefs`)
- Changing the default value for a configuration option

## Examples of a Feature level Change (minor bump: `v1.X.0`)

- Dropping support of an old `mkdocstrings-python` version
- Introducing support of a new `mkdocstrings-python` version
- Introducing new cross-reference syntax that doesn't interfere with the existing one
- Adding a configuration option for the handler (like `check_crossrefs`), assuming it doesn't affect the default
  behavior in a breaking way, at least not by default.
- Adding support for validating more cross-references (not breaking, as people will have these marked as ignored, this
  just allows to no longer ignore these xrefs from validation)

## Examples of a Patch level change (patch bump: `v1.0.X`)

- Adding unit-tests
- Adding CI workflows
- Changing the documentation
- **Changing the internal code in any way**

Relying on the handler class, or any other code components from this library is not supported. **All code for this
library is considered a part of the private API** and is subject to any changes without backwards compatibility in mind.

We usually make these updates with the goal of improving the code readability or efficiency.

[semver]: https://semver.org
[config-option]: ../config.md
