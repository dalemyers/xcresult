# xcresult

A Python library and CLI tool for reading Xcode's `.xcresult` bundles. It uses
xcresulttool's modern JSON reports and generated Python dataclasses to inspect
build issues, extract test results, export attachments, and generate JUnit XML.
Neither generation nor runtime access uses the deprecated legacy object API.

## Installation

```
pip install xcresult
```

Requires Python 3.10+ and Xcode 27's `xcresulttool` (schema version 0.4.0).
Select the Xcode installation using `xcode-select` or `DEVELOPER_DIR`. Older
Xcode schema versions are not currently a supported compatibility target.

## Library Usage

```python
import xcresult

bundle = xcresult.Xcresults("/path/to/MyApp.xcresult")

# Check build issues
for error in bundle.build_results.errors:
    print(error.message, error.sourceURL)

# Decode an issue's source URL into a file path and one-based coordinates
for warning in bundle.build_results.warnings:
    location = xcresult.parse_source_url(warning.sourceURL)
    if location is None:
        continue
    print(location.path, location.starting_line_number, location.starting_column_number)
    print(f"{location} -> {warning.message}")

# Check availability before requesting test reports from build-only bundles
if bundle.content_availability.hasTestResults:
    print(bundle.test_summary.failedTests)
    for node in bundle.tests.testNodes:
        print(node.name, node.result)

# Read a specific test's individual runs or activity trees
details = bundle.test_details("MyTests/testExample()")
activities = bundle.test_activities("MyTests/testExample()")

# Export test attachments (screenshots, etc.)
manifest = bundle.export_test_attachments("/path/to/output/")

# Write JUnit XML
bundle.write_junit("/path/to/results.junit")
```

`build_results`, `content_availability`, `test_summary`, and `tests` are loaded
lazily and cached for the lifetime of the `Xcresults` instance. Test identifiers
can be identifier strings or identifier URLs; prefer URLs when targets contain
identically named tests. Apple field names retain their camelCase spelling.

### Source locations

Modern reports give each `Issue` a `sourceURL` string rather than a legacy
location object, for example
`file:///path/to/File.swift#StartingLineNumber=328&StartingColumnNumber=35`.
`parse_source_url` decodes one into a frozen `source_url.SourceLocation`,
returning `None` when the URL is absent, empty, or has no file path:

| Attribute | Description |
| --- | --- |
| `path` | The percent-decoded file path |
| `starting_line_number` | One-based line, or `None` if absent or unusable |
| `starting_column_number` | One-based column, or `None` if absent or unusable |

The coordinates in the URL fragment are zero based; they are converted to the
one-based values editors and build logs report. Blank, negative, and
non-integer values decode as `None` rather than raising. Converting a
`SourceLocation` to a string appends whichever coordinates are available,
stopping at the first missing one, giving `path`, `path:line`, or
`path:line:column`. This is the format the `check-issues` subcommand prints.

Note that `xcresult.SourceLocation` is a different, generated type: it is
Apple's wire model for `TestNode.sourceLocation` (`filePath` and `lineNumber`).
Import the decoded issue location from its module to keep the two apart:

```python
from xcresult.source_url import SourceLocation, parse_source_url
```

Attachments use xcresulttool's export layout: files and `manifest.json` in the
output directory. The returned manifest identifies each test's files through
`attachment.exportedFileName`. To export only one test or suite, pass
`test_id="MyTests/testExample()"`.

Use a fresh output directory for each export: xcresulttool refuses to overwrite
an existing `manifest.json`. The JUnit `export_attachments_path` option performs
its own export, so it also needs a directory without an existing manifest.

### JUnit options

```python
bundle.write_junit(
    "/path/to/results.junit",
    export_attachments_path="/path/to/attachments",
    test_class_prefix="MyApp",
    test_class_suffix="UI",
    collapse_retries=True,
    test_filter=lambda test: not test.name.startswith("disabled"),
)
```

By default, each individual run becomes a testcase, rather than reporting only
the aggregate result. Retry collapsing prefers a passing attempt and keeps
different devices, configurations, and arguments separate. Expected failures
are treated as successful outcomes; skipped tests become `<skipped>` elements.
Unknown outcomes are not treated as passes. The filter receives a modern
`TestNode`; excluded tests do not contribute to XML counts or leave empty suites.
Suite names follow the modern bundle/suite hierarchy, with configuration and
device recorded as properties. Attachment links come from the export manifest.
Build-only bundles produce an empty JUnit report.

## CLI Usage

The package installs an `xcresult` command with three subcommands:

### Export test attachments

```
xcresult -b /path/to/MyApp.xcresult export -o /path/to/output/
```

### Generate JUnit XML

```
xcresult -b /path/to/MyApp.xcresult junit -o /path/to/results.junit
```

Optionally export attachments alongside the JUnit file:

```
xcresult -b /path/to/MyApp.xcresult junit -o /path/to/results.junit --export-attachments-path /path/to/attachments/
```

Collapse retry attempts:

```
xcresult -b /path/to/MyApp.xcresult junit -o /path/to/results.junit --collapse-retries
```

### Check for issues

```
xcresult -b /path/to/MyApp.xcresult check-issues
```

Filter by issue type with `--issue-types`:

```
xcresult -b /path/to/MyApp.xcresult check-issues --issue-types error warning
```

Available issue types: `error`, `warning`, `analyzer-warning`, `test-failure`, `test-warning`.

Returns exit code 1 if any matching issues are found.

## Migrating from the legacy API

This is a **breaking library API change**. The command-line subcommands remain
available, but the underlying models, attachment layout, and JUnit suite
hierarchy now follow the modern reports.

| Legacy API | Modern API |
| --- | --- |
| `actions_invocation_record.issues` | `build_results.errors`, `.warnings`, `.analyzerWarnings`, plus `test_summary.testFailures` and `.runtimeWarnings` |
| `actions_invocation_record.actions` and `testsRef` traversal | `tests.testNodes` and `test_details(test_id).testRuns` |
| `get(object_id)` and summary references | `test_details(test_id)` or `test_activities(test_id)` |
| `export_attachment(payload_id, type, path)` | `export_test_attachments(directory, test_id=...)` and its returned manifest |
| `ActionTestMetadata` in test filters | `TestNode` (`name`, `nodeIdentifier`, `nodeIdentifierURL`, `result`) |
| `deserialize(legacy_typed_json)` | `Tests.from_dict(json_data)` or `deserialize(json_data, Tests)` |
| `issue.documentLocationInCreatingWorkspace` | `issue.sourceURL`, decoded with `parse_source_url` |

Legacy `Action*`, `Reference`, and other internal object-graph models are no
longer exported. Modern models are dataclasses with required constructor
arguments and optional fields defaulting to `None`. Missing required data and
invalid field types raise errors; unrecognized properties are logged and
ignored to accommodate additive tool changes. Decoding does not mutate input.
Test results use modern values such as `Passed`, `Failed`, `Skipped`, and
`Expected Failure`, rather than legacy `testStatus` values. Timestamp fields
are UNIX seconds, not `datetime` objects. Models use normal mutable dataclass
equality and are not hashable.

## Development

Dependencies are managed with Poetry. Regenerate the models from the selected
Xcode installation's endpoint schemas, then format them:

```
python -m generator
python -m black --line-length 100 xcresult/model.py
```

The generator reads the schemas for test summaries, test trees, test details,
activities, build results, content availability, and attachment manifests. It
reconciles shared types and keeps distinct activity/export attachment models.
Two known schema cardinality errors are corrected to match report output:
`Summary.devicesAndConfigurations` and `Activities.testRuns` are arrays.
Generated models are checked in; using the package does not run the generator.

```
python -m pytest tests
XCRESULT_RUN_INTEGRATION=1 python -m pytest tests/test_modern_integration.py
```

Tests cover ordinary JSON decoding, command routing, issue reporting, retries,
filtering, report counts, and manifest-based attachment links. Xcode integration
checks use disposable fixture copies because xcresulttool may update a bundle's
database while reading it. The live test-report, activity, and export checks are
opt-in and require a working local Xcode test-report cache; command failures
are surfaced rather than silently falling back to the legacy API.

## License

MIT
