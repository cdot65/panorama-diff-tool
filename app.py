# standard library imports
import logging
import argparse

# third party imports
from lxml import etree
import difflib
import requests


def fetch_config(url, headers, config_params):
    """
    Fetch configuration from Panorama. Parses the response as XML.
    """
    logging.info(
        f"Fetching configuration from Panorama with parameters: {config_params}"
    )
    try:
        response = requests.get(
            f"https://{url}/api", headers=headers, params=config_params, timeout=10
        )
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

    logging.debug(
        f"Response Status: {response.status_code}, Response Body: {response.text[:100]}..."
    )
    return etree.fromstring(response.content)


def find_element_by_xpath(xml_obj, xpath):
    """
    Find an element in an XML object using an XPath.

    :param xml_obj: XML object to search in.
    :param xpath: XPath string to locate the desired element.
    :return: Element at the specified XPath or None if not found.
    """
    try:
        element = xml_obj.xpath(xpath)
        if element:
            logging.debug(f"Element found for XPath: {xpath}")
            return element[0]  # Return the first matched element
        else:
            logging.debug(f"Element not found for XPath: {xpath}")
            return None
    except Exception as e:
        logging.error(f"Error finding element: {e}")
        return None


def filter_xml_by_xpath(xml_obj, xpath):
    """
    Filter an XML object to include only elements at a specific XPath.
    """
    element = find_element_by_xpath(xml_obj, xpath)
    if element is None:
        logging.warning(f"No matching elements found for XPath: {xpath}")
        return None

    # Use lxml to create a new XML element for filtered results
    filtered_xml = etree.Element("FilteredResult")
    filtered_xml.append(element)

    logging.debug(
        f"Filtered XML: {etree.tostring(filtered_xml, pretty_print=True, encoding='unicode')}"
    )
    return filtered_xml


def generate_diff_string(xml1, xml2):
    """
    Generate a unified diff string between two XML objects.
    """
    # Convert XML objects to string representations
    xml1_string = etree.tostring(xml1, pretty_print=True, encoding="unicode")
    xml2_string = etree.tostring(xml2, pretty_print=True, encoding="unicode")

    # Generating the unified diff
    diff = difflib.unified_diff(
        xml1_string.splitlines(), xml2_string.splitlines(), lineterm=""
    )
    return "\n".join(diff)


def main():
    # Initialize logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    parser = argparse.ArgumentParser(description="Panorama Configuration Diff Tool")

    # Add an argument for logging level
    parser.add_argument("--debug", help="Enable debug logging", action="store_true")

    # Panorama Information
    parser.add_argument("--url", required=True, help="URL of the Panorama API endpoint")
    parser.add_argument(
        "--api-key",
        help="API key for authentication (required)",
    )

    # XPath Parameters
    parser.add_argument(
        "--device-group", help="Device group to filter the XML configuration"
    )
    parser.add_argument("--template", help="Template to filter the XML configuration")
    parser.add_argument(
        "--template-stack", help="Template stack to filter the XML configuration"
    )

    args = parser.parse_args()

    # Adjust logging level based on the debug flag
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Start of script processing
    logging.info("Starting Panorama Configuration Diff Tool")

    # Argument validation for api-key
    if not args.api_key:
        parser.error("You must provide an --api-key")

    # Ensure at least one of the XPath parameters is provided
    if not (args.device_group or args.template or args.template_stack):
        parser.error(
            "At least one XPath parameter (device-group, template, template-stack) must be provided"
        )

    # Form the XPath based on the provided argument
    if args.device_group:
        xpath_to_filter = f'/response/result/config/devices/entry/device-group/entry[@name="{args.device_group}"]'
    elif args.template:
        xpath_to_filter = f'/response/result/config/devices/entry/template/entry[@name="{args.template}"]'
    elif args.template_stack:
        xpath_to_filter = f'/response/result/config/devices/entry/template-stack/entry[@name="{args.template_stack}"]'

    headers = {}
    if args.api_key:
        headers["X-PAN-KEY"] = args.api_key
    elif args.username and args.password:
        # TODO
        pass

    url = args.url
    candidate_config_params = {
        "type": "op",
        "cmd": "<show><config><candidate/></config></show>",
    }
    running_config_params = {
        "type": "op",
        "cmd": "<show><config><running/></config></show>",
    }

    # Fetching configurations and generating diff
    candidate_config_xml = fetch_config(url, headers, candidate_config_params)
    running_config_xml = fetch_config(url, headers, running_config_params)

    if candidate_config_xml is None or running_config_xml is None:
        logging.error("Failed to fetch configurations. Exiting.")
        return

    filtered_candidate_config = filter_xml_by_xpath(
        candidate_config_xml, xpath_to_filter
    )
    filtered_running_config = filter_xml_by_xpath(running_config_xml, xpath_to_filter)

    logging.info("Generating configuration diff...")
    diff_result = generate_diff_string(
        filtered_running_config,
        filtered_candidate_config,
    )

    if diff_result:
        logging.info("Diff generated successfully.")
        print(diff_result)
    else:
        logging.info("No differences found.")


if __name__ == "__main__":
    main()
