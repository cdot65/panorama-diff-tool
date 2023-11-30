# Panorama Configuration Diff Tool

This is a Python script that fetches configuration data from a Panorama API endpoint, filters the data based on provided XPath parameters, and generates a unified diff between the candidate and running configurations.

## Prerequisites

- Python 3.x
- Docker (optional)

## Usage

When running the script, from either the Docker container image or your own Python environment, you must provide the following arguments:

- `--url` - The URL of the Panorama API endpoint.
- `--api-key` - The API key used to authenticate to the Panorama API endpoint.

You are to pass one of the following arguments:

- `--device-group` - The name of the device group to fetch configuration data from.
- `--template` - The name of the template to fetch configuration data from.
- `--template-stack` - The name of the template stack to fetch configuration data from.

## Docker Workflow

1. Pull the pre-built Docker container image:

   ```shell
   docker pull ghcr.io/cdot65/panorama-diff-tool:latest
   ```

2. Run the Docker container with the necessary arguments. Replace <url>, <api-key>, and <device-group/template/template-stack> with your actual values:

   ```shell
   docker run -it --rm ghcr.io/cdot65/panorama-diff-tool:latest --url <url> --api-key <api-key> --device-group <device-group name> | --template <template name> | --template-stack <template-stack name>
   ```

### Docker Container Example

```shell
docker run -it --rm ghcr.io/cdot65/panorama-diff-tool:latest --url panorama.example.com --api-key mysecretapikey --device-group DataCenter
docker run -it --rm ghcr.io/cdot65/panorama-diff-tool:latest --url panorama.example.com --api-key mysecretapikey --template DataCenter
docker run -it --rm ghcr.io/cdot65/panorama-diff-tool:latest --url panorama.example.com --api-key mysecretapikey --template-stack DCN-PAF-001
```

## Python Workflow

1. Clone the repository:

   ````shell
   git clone https://github.com/cdot65/panorama-diff-tool.git```
   ````

2. Navigate to the cloned repository:

   ```shell
   cd panorama-diff-tool
   ```

3. Install the required Python packages:

   ```shell
   pip3 install -r requirements.txt
   ```

4. Run the script with the necessary arguments. Replace <url>, <api-key>, and <device-group/template/template-stack> with your actual values:

   ```shell
   python app.py --url <url> --api-key <api-key> --device-group <device-group name> | --template <template name> | --template-stack <template-stack name>
   ```

### Python Workflow Example

```shell
python app.py --url panorama.example.com --api-key mysecretapikey --device-group DataCenter
python app.py --url panorama.example.com --api-key mysecretapikey --template DataCenter
python app.py --url panorama.example.com --api-key mysecretapikey --template-stack DCN-PAF-001
```
