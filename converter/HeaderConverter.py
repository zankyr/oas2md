from model.Header import Header


def sanitize_markdown_table_cell(cell_content: str):
    """
    Replaces newline characters ("\n") and YAML-style newline characters ("\\n", which is a "\" symbol followed by a newline)
    with the HTML tag "<br />".

     This is required since the only method to create a newline inside a markdown table cell is using the HTML newline tag,
     any other syntax will result in bad formatting styles.

    :param cell_content: the YAML content to convert as a markdown cell
    :return: the string with all the specified characters replaced by the "<br />" tag
    """
    return cell_content.replace("\\\n", "<br />").replace("\n", "<br />")


def __get_header_from_components(header: str, header_content: dict, headers_components: dict) -> Header:
    h = Header(header)
    header_ref = header_content['$ref']
    header_ref_name = header_ref[header_ref.rfind('/') + 1:]
    if header_ref_name not in headers_components:
        raise Exception(f'{header_ref_name} not found in the \'components/headers\' section')
    header_component = headers_components[header_ref_name]
    h.type = header_component['schema']['type']
    h.example = header_component['schema']['example']
    h.description = sanitize_markdown_table_cell(header_component['description'])
    return h


def __get_header(header: str, header_content: dict, headers_components: dict) -> Header:
    if '$ref' in header_content:
        return __get_header_from_components(header, header_content, headers_components)

    h = Header(header)
    h.type = header_content['schema']['type']
    h.example = header_content['schema']['example']
    h.description = sanitize_markdown_table_cell(header_content['description'])
    return h


def get_headers(response_content: dict, components: dict) -> list[Header]:
    headers = []

    if 'headers' not in response_content:
        return headers

    headers_content = response_content['headers']
    headers_components = components['headers'] if 'headers' in components else None

    for header, header_content in headers_content.items():
        headers.append(__get_header(header, header_content, headers_components))

    return headers
