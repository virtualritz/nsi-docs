# Parameter Names by API Call

This table lists all optional parameters for each C API function. Parameters marked with (!) have a proposed new name for future consistency.

## NSIBegin

| Current Name            | Type    | Default | Proposed Name (!)     |
| ----------------------- | ------- | ------- | --------------------- |
| `type`                  | string  | render  |                       |
| `streamfilename`        | string  |         | `stream.filename`     |
| `streamformat`          | string  |         | `stream.format`       |
| `streamcompression`     | string  |         | `stream.compression`  |
| `streampathreplacement` | int     |         | `stream.path.replace` |
| `separateprocess`       | int     |         |                       |
| `errorhandler`          | pointer |         |                       |
| `errorhandler.data`     | pointer |         |                       |
| `executeprocedurals`    | string  |         | `evaluate.replace`    |

## NSICreate

No optional parameters defined.

## NSIDelete

| Current Name | Type | Default | Proposed Name (!) |
| ------------ | ---- | ------- | ----------------- |
| `recursive`  | int  | 0       |                   |

## NSISetAttribute / NSISetAttributeAtTime

These functions accept node attributes as their optional arguments. See [Attribute Names by Node](attribute-names.md) for a complete list.

## NSIDeleteAttribute

No optional parameters (takes a single `name` argument directly).

## NSIConnect

| Current Name | Type | Default | Proposed Name (!) |
| ------------ | ---- | ------- | ----------------- |
| `value`      |      |         |                   |
| `priority`   |      |         |                   |
| `strength`   | int  | 0       |                   |

## NSIDisconnect

No optional parameters.

## NSIEvaluate

| Current Name     | Type    | Default | Proposed Name (!) |
| ---------------- | ------- | ------- | ----------------- |
| `type`           | string  |         |                   |
| `filename`       | string  |         | `stream.filename` |
| `script`         | string  |         |                   |
| `buffer`         | pointer |         |                   |
| `size`           | int     |         |                   |
| `backgroundload` | int     |         |                   |

## NSIRenderControl

| Current Name          | Type    | Default | Proposed Name (!) |
| --------------------- | ------- | ------- | ----------------- |
| `action`              | string  |         |                   |
| `progressive`         | integer |         |                   |
| `interactive`         | integer |         |                   |
| `frame`               |         |         |                   |
| `stoppedcallback`     | pointer |         | `callback`        |
| `stoppedcallbackdata` | pointer |         | `callback.data`   |
