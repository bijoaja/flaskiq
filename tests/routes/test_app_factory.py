from app.routes import api_v1_bp, auth_view_bp, cms_bp, landing_bp


def test_blueprints_registered(app):
    expected_blueprints = [landing_bp.name, auth_view_bp.name, cms_bp.name, api_v1_bp.name]
    for bp_name in expected_blueprints:
        assert bp_name in app.blueprints
