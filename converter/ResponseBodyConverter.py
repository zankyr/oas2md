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


def __get_response_body(content_type: str, body_content: dict, body_components: dict) -> Content:
    response_properties = []

    required_properties = body_content['schema']['required'] if 'required' in body_content['schema'] else []

    for property_name, property_content in body_content['schema']['properties'].items():
        if 'object' == property_content['type']:
            attribute = Attribute(property_name)
            attribute.type = property_content['type']
            response_properties.append(attribute)
            response_properties.extend(__get_nested_properties(property_name, property_content))
            continue

        attribute = Attribute(property_name)
        attribute.description = (property_content['description']).replace('\n', '<br />')
        attribute.type = property_content['type']
        attribute.example = str(property_content['example']) if 'example' in property_content else ''
        response_properties.append(attribute)

    return Content(content_type, response_properties)


def get_response_content(response_content: dict, components: dict) -> list[Content]:
    bodies = []
    for body, body_content in response_content['content'].items():
        bodies.append(__get_response_body(body, body_content, None))
    return bodies
