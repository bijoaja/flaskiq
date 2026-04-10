class DocsApiService:
    SWAGGER_URL = "/api/v1/docs"
    API_URL     = "/static/swagger.yaml"

    @classmethod
    def get_info(cls) -> dict:
        return {"docs_url": cls.SWAGGER_URL, "swagger_spec": cls.API_URL}
