# Quick Start

The program is AIAA Client easy sample by refer [ai-assisted-annotation-client/py-client](https://github.com/NVIDIA/ai-assisted-annotation-client/tree/master/py-client)

- Start AIAA Server
- Start AIAA Client

## Start AIAA server

`python3 test_aiaa_server.py --test_config {configuration file}`

- Configuration file
  - aas_tests_fixpolygon.json
  - aas_tests_mask2polygon.json 

```
python test_aiaa_server.py --test_config aas_tests.json
```

test_aiaa_server.py gives method to test the API under configurations specified by aas_tests.json:

server information: IP, port, version

test-specific information: test name disable flag for running / skipping a particular test api name for selecting different methods test-dependent parameters: input/output file path, other parameters


## Start AIAA Client

```
python3 aiaa_client.py
```
