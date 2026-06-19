# xcresult

A Python library and CLI tool for parsing Xcode's `.xcresult` bundles. It wraps `xcresulttool` and deserializes the output into typed Python objects, so you can inspect build issues, extract test results, export attachments, and generate JUnit XML reports.

## Installation

```
pip install xcresult
```

Requires Python 3.10+ and Xcode's `xcresulttool` (ships with Xcode).

## Library Usage

```python
import xcresult

bundle = xcresult.Xcresults("/path/to/MyApp.xcresult")

# Access the invocation record
record = bundle.actions_invocation_record

# Check for errors
if record.issues.errorSummaries:
    for error in record.issues.errorSummaries:
        print(error.message)

# Export test attachments (screenshots, etc.)
bundle.export_test_attachments("/path/to/output/")

# Write JUnit XML
bundle.write_junit("/path/to/results.junit")
```

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

## License

MIT
