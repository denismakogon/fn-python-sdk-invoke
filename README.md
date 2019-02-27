# Invoke Oracle Functions using the OCI Python SDK

## Pre-requisites

1. Install/update the Fn CLI

   `curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install |
   sh`

2. Create a function to invoke

   Create a function using [Go Hello World
   Function](https://github.com/abhirockzz/oracle-functions-hello-worlds/blob/master/golang-hello-world.md)

### Install preview OCI Python SDK

1. Download and unzip the preview SDK

   `unzip oci-python-sdk-2.2.1+preview.1.712.zip`

2. Change into the correct directory

   `cd oci-python-sdk-2.2.1+preview.1.712`

3. Virtualenv

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install oci-2.2.1+preview.1.712-py2.py3-none-any.whl
   ```

4. Clone this repository in a separate directory 

   `git clone https://github.com/denismakogon/fn-python-sdk-invoke.git`

5. Change to the correct directory where you cloned the example: 

   `cd fn-python-sdk-invoke` 



### Authentication

This example assumes the OCI config file is available on the machine where this client code will run. You can override the config defaults using the following environment variables:

 - `OCI_CONFIG_PATH` for the OCI config file (default value: `~/.oci/config`)
 - `OCI_CONFIG_PROFILE` stands from the OCI config profile (default value: `DEFAULT`)


## You can now invoke your function!

```bash
python invoke_function.py <compartment-name> <app-name> <function-name> <request payload>
```

### Enable debug mode

Set environment variable:

```bash
export DEBUG=1
python invoke_function.py <compartment-name> <app-name> <function-name> <request payload>
```
or

```bash
DEBUG=1 python invoke_function.py <compartment-name> <app-name> <function-name> <request payload>
```

### Example of invoking a function

1) Using and "DEFAULT" oci config profile:

```bash
python invoke_function.py workshop helloworld-app helloworld-func-go '{"name":"foobar"}'
{"message":"Hello foobar"}
```

2) Using a non-DEFAULT profile name in oci config:

a) with payload:

```bash
OCI_CONFIG_PROFILE=workshop-devrel-profile python invoke_function.py workshop helloworld-app helloworld-func-go '{"name":"foobar"}'
```

b) without payload:

```bash
OCI_CONFIG_PROFILE=workshop-devrel-profile python invoke_function.py workshop helloworld-app helloworld-func-go '{}'
```

3) Invoking a Function inside a nested compartment:

a) with payload:

```bash
python invoke_function.py nested-ws nest-app go-fn {"name":"EMEA"}
```

b) without payload:

```bash
python invoke_function.py nested-ws nest-app go-fn '{}'
```

## What if my function needs input in binary form?

You can use this Tensorflow based function as an example to explore the
possibility of invoking a function using binary content -
https://github.com/abhirockzz/fn-hello-tensorflow. This function expects the
image data (in binary form) as an input and returns what object that image
resembles along with the percentage accuracy.

If you were to deploy the Tensorflow function, the command to invoke it using Fn
CLI would be something like this - `cat /home/foo/cat.jpeg | fn invoke
fn-tensorflow-app classify`. In this case, the `cat.jpeg` image is being passed
as an input to the function. 

The programmatic (using python SDK) equivalent of
this would look something like [invoke_function_tf.py](invoke_function_tf.py)

### Example of invoking a function with binary input

```bash
python invoke_function_tf.py <compartment-name> <app-name> <function-name> <image-file-path>
```

```bash
python invoke_function_tf.py workshop demo-app classify test-som-1.jpeg
This is a 'sombrero' Accuracy - 94%
```
