from model.ResponseAttribute import ResponseAttribute
from model.ResponseBody import ResponseBody


def __get_response_body(content_type:str, body_content: dict, body_components: dict) -> ResponseBody:
    response_properties = []
    
    for property, property_content in body_content['schema']['properties'].items():
        ra = ResponseAttribute(property)
        ra.description = (property_content['description']).replace('\n', '<br />')
        ra.type = property_content['type']
        ra.example = property_content['example'] if 'example' in property_content else ''
        response_properties.append(ra)
        
    return ResponseBody(content_type, response_properties)

def get_response_bodies(response_content: dict, components: dict) -> list[ResponseBody]:
    bodies_content = response_content['content']
    bodies = []
    for body, body_content in bodies_content.items():
        bodies.append(__get_response_body(body, body_content, None))
    return bodies


        