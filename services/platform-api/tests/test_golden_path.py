from app.services.golden_path import GoldenPathEngine, build_context


def test_golden_path_renders_all_artifacts():
    context = build_context(
        app_name="demo-api",
        display_name="Demo API",
        team="platform",
        namespace="team-platform-demo-api",
        template="web-api",
        ocp_base_domain="ocp1.npd.co",
    )

    engine = GoldenPathEngine()
    artifacts = engine.render("web-api", context)

    expected = {
        "namespace.yaml",
        "resourcequota.yaml",
        "helm-values.yaml",
        "argocd-application.yaml",
        "route.yaml",
        "keycloak-client.json",
        "postgres-config.yaml",
        "redis-config.yaml",
        "kafka-topic.yaml",
        "otel-config.yaml",
        "servicemonitor.yaml",
    }
    assert expected == set(artifacts.keys())
    assert "team-platform-demo-api" in artifacts["namespace.yaml"]
    assert "demo-api-platform.apps.ocp1.npd.co" in artifacts["route.yaml"]
    assert "phoenix.platform.demo-api.events" in artifacts["kafka-topic.yaml"]
