
import base64
import requests
from kairosNoCheckin import app_id, app_key


base_url = 'https://api.kairos.com/'
_enroll_base_url = base_url + 'enroll'

def enroll_face(subject_id, gallery_name, base64_image_contents=None):

    auth_headers = {
        'app_id': app_id,
        'app_key': app_key
    }

    payload = _build_payload(subject_id, gallery_name, url, file,
                             base64_image_contents, multiple_faces, additional_arguments)

    response = requests.post(_enroll_base_url, json=payload, headers=auth_headers)
    json_response = response.json()
    if response.status_code != 200 or 'Errors' in json_response:
        raise exceptions.ServiceRequestError(response.status_code, json_response, payload)

    return json_response


def buildPayload(subjectId, galleryName, imageFile):
    image = _extract_base64_contents(imageFile)
    required_fields = {'image': image, 'subject_id': subjectId,
                       'gallery_name': galleryName}

    return required_fields


def _extract_base64_contents(file):
    with open(file, 'rb') as fp:
        image = base64.b64encode(fp.read()).decode('ascii')
    return image


if __name__ == '__main__':
    print('enroll picture to Kairos')
   
