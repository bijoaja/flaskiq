from flask import jsonify, make_response, Response as FlaskResponse, stream_with_context

class Response:
    def __init__(self, stream_mode=False):
        self.stream_mode = stream_mode

    def success(self, is_success: bool=False, chunks: str=None, content_type="text/plain", values: dict=None, directStreamData=None, message: str=None, code=200) -> FlaskResponse:
        
        if self.stream_mode and chunks:
            def generate():
                try:
                    if directStreamData:
                        yield f"{directStreamData}|||||"
                    for chunk in chunks:
                        yield chunk
                except Exception as e:
                    yield jsonify({"error": str(e)})
            
            return FlaskResponse(
                stream_with_context(generate()),
                content_type=content_type,
                headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no"
                }
            )
        
        # Non-streaming response
        res = {"success": is_success,"data": values, "message": message}
        return make_response(jsonify(res), code)

    @staticmethod
    def invalid(is_success: bool=False, values: dict=None, message: str=None, code=400) -> FlaskResponse:
        res = {"success":is_success,"data": values, "message": message}
        return make_response(jsonify(res), code)
