from collections.abc import Generator, Iterable
from typing import Any

from flask import Response as FlaskResponse
from flask import jsonify, make_response, stream_with_context


class Response:
    def __init__(self, stream_mode: bool = False) -> None:
        self.stream_mode = stream_mode

    def success(
        self,
        is_success: bool = True,
        chunks: Iterable[str] | None = None,
        content_type: str = "text/plain",
        values: Any = None,
        directStreamData: Any = None,
        message: str | None = None,
        code: int = 200,
    ) -> FlaskResponse:
        if self.stream_mode and chunks:

            def generate() -> Generator[str, None, None]:
                try:
                    if directStreamData:
                        yield f"{directStreamData}|||||"
                    yield from chunks
                except Exception as e:
                    yield str(jsonify({"error": str(e)}))

            return FlaskResponse(
                stream_with_context(generate()),
                content_type=content_type,
                headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
            )

        # Non-streaming response
        res = {"success": is_success, "data": values, "message": message}
        return make_response(jsonify(res), code)

    @staticmethod
    def invalid(
        is_success: bool = False,
        values: Any = None,
        message: str | None = None,
        code: int = 400,
    ) -> FlaskResponse:
        res = {"success": is_success, "data": values, "message": message}
        return make_response(jsonify(res), code)
