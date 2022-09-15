from src.yadisk_api.api.schema import Error

bad_request_response = {400: {"model": Error}}
not_found_response = {404: {"model": Error}}

common_responses = bad_request_response | not_found_response
