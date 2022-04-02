from model.Attribute import Attribute
from model.Content import Content


def __get_nested_properties(parent_property: str, nested_properties: dict) -> list[Attribute]:
    attributes = []

    required_properties = nested_properties['required']
    properties = nested_properties['properties']

    for nested_property_name, nested_property in properties.items():
        attribute = Attribute(nested_property_name)
        attribute.parent_attribute = parent_property
        attribute.description = (nested_property['description']).replace('\n', '<br />')
        attribute.type = nested_property['type']
        attribute.example = str(nested_property['example']) if 'example' in nested_property else ''
        attribute.required = True if nested_property_name in required_properties else False
        attributes.append(attribute)

    return attributes


# def __get_content_from_components():


def __get_response_body(content_type: str, body_content: dict, body_components: dict) -> Content:
    if '$ref' in body_content['schema']:
        body_content_ref = body_content['schema']['$ref']
        body_content_ref_name = body_content_ref[body_content_ref.rfind('/') + 1:]
        if body_content_ref_name not in body_components:
            raise Exception(f'{body_content_ref_name} not found in the \'components/schema\' section')
        body_component = body_components[body_content_ref_name]
        body_content_properties = body_component['properties']
        required_properties = body_component['required'] if 'required' in body_component else []
    else:
        body_content_properties = body_content['schema']['properties']
        required_properties = body_content['schema']['required'] if 'required' in body_content['schema'] else []

    response_properties = []

    for property_name, property_content in body_content_properties.items():
        if 'object' == property_content['type']:
            attribute = Attribute(property_name)
            attribute.type = property_content['type']
            attribute.required = True if property_name in required_properties else False
            response_properties.append(attribute)
            response_properties.extend(__get_nested_properties(property_name, property_content))
            continue

        attribute = Attribute(property_name)
        attribute.description = (property_content['description']).replace('\n', '<br />') \
            if 'description' in property_content \
            else ''
        attribute.type = property_content['type']
        attribute.required = True if property_name in required_properties else False
        attribute.example = str(property_content['example']) if 'example' in property_content else ''
        response_properties.append(attribute)

    return Content(content_type, response_properties)


def get_response_content(response_content: dict, components: dict) -> list[Content]:
    bodies = []

    if 'content' not in response_content:
        return bodies

    body_components = components['schemas'] if 'schemas' in components else None

    for body, body_content in response_content['content'].items():
        bodies.append(__get_response_body(body, body_content, body_components))

    return bodies
