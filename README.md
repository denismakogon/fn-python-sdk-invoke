# Calling a function using OCI SDK

## Requirements

 - OCI SDK preview `2.2.1+preview.1.712` or greater

## Virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install oci-2.2.1+preview.1.712-py2.py3-none-any.whl
```

## CLI helper

```bash
python invoke_function.py <compartment-name> <app-name> <function-name> <request payload>
```

## OCI config file and auth profile

The [invoke_function.py](invoke_function.py) allows to configure OCI config file and the config profile via environment variables:

 - `OCI_CONFIG_PATH` - stands for the OCI config (default is `~/.oci/config`)
 - `OCI_CONFIG_PROFILE` - stands from the OCI config profile (default is `default`)


## Enable debug mode

Set environment variable:
```bash
export DEBUG=1
python invoke_function.py <compartment-name> <app-name> <function-name> <request payload>
```
or
```bash
DEBUG=1 python invoke_function.py <compartment-name> <app-name> <function-name> <request payload>
```

## Calling function

```bash
python invoke_function.py functions-test demo-app go-fn '{"name":"denis"}'
{"message":"Hello denis"}
```

## OCI config profile configuration
```bash
$ OCI_CONFIG_PROFILE=workshop-devrel-profile python invoke_function.py workshop helloworld-app helloworld-func-go '{"name":"EMEA"}'
$ OCI_CONFIG_PROFILE=workshop-devrel-profile python invoke_function.py workshop helloworld-app helloworld-func-go '{}'
$ OCI_CONFIG_PROFILE=workshop-devrel-profile python invoke_function.py workshop demo-app node-fn {"name":"EMEA"}
$ OCI_CONFIG_PROFILE=workshop-devrel-profile python invoke_function.py workshop demo-app node-fn '{}'
$ OCI_CONFIG_PROFILE=workshop-devrel-profile python invoke_function.py workshop demo-app go-fn '{"name":"EMEA"}'
$ OCI_CONFIG_PROFILE=workshop-devrel-profile python invoke_function.py workshop demo-app go-fn '{}'

## Nested Compartment
$ OCI_CONFIG_PROFILE=workshop-devrel-profile python invoke_function.py nested-ws nest-app go-fn {"name":"EMEA"}
$ OCI_CONFIG_PROFILE=workshop-devrel-profile python invoke_function.py nested-ws nest-app go-fn '{}'
```

## TensorFlow

```bash
python invoke_function_tf.py <compartment-name> <app-name> <function-name> <image-file-path>
```

```bash
$ OCI_CONFIG_PROFILE=workshop-devrel-profile python invoke_function_tf.py workshop demo-app classify test-som-1.jpeg
This is a 'sombrero' Accuracy - 94%

$ OCI_CONFIG_PROFILE=workshop-devrel-profile python invoke_function_tf.py workshop demo-app classify /Users/sachinpikle/doag/fn-python-sdk-invoke/test-som-1.jpeg
This is a 'sombrero' Accuracy - 94%
```
