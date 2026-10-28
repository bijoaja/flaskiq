from app.routes import landing_bp, auth_view_bp, cms_bp, api_v1_bp


def test_blueprints_registered(app):
    expected_blueprints = [landing_bp.name, auth_view_bp.name, cms_bp.name, api_v1_bp.name]
    for bp_name in expected_blueprints:
        assert bp_name in app.blueprints
