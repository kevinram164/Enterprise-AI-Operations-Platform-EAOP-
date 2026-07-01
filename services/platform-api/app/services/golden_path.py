from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.config import get_settings

settings = get_settings()
TEMPLATES_ROOT = settings.golden_path_templates_dir


def build_context(
    *,
    app_name: str,
    display_name: str,
    team: str,
    namespace: str,
    template: str,
    ocp_base_domain: str,
    description: str | None = None,
) -> dict:
    db_name = f"{team}_{app_name}".replace("-", "_")
    return {
        "app_name": app_name,
        "display_name": display_name,
        "team": team,
        "namespace": namespace,
        "template": template,
        "description": description or "",
        "ocp_base_domain": ocp_base_domain,
        "route_host": f"{app_name}-{team}.apps.{ocp_base_domain}",
        "kafka_topic": f"phoenix.{team}.{app_name}.events",
        "postgres_db": db_name,
        "postgres_user": db_name,
        "redis_key_prefix": f"{team}:{app_name}",
        "otel_service_name": app_name,
    }


class GoldenPathEngine:
    def __init__(self, templates_root: Path = TEMPLATES_ROOT) -> None:
        self.templates_root = templates_root

    def render(self, template_name: str, context: dict) -> dict[str, str]:
        template_dir = self.templates_root / template_name
        if not template_dir.is_dir():
            raise ValueError(f"Golden Path template '{template_name}' not found")

        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(disabled_extensions=("j2",)),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        artifacts: dict[str, str] = {}
        for path in sorted(template_dir.glob("*.j2")):
            rendered = env.get_template(path.name).render(**context)
            artifacts[path.stem] = rendered

        if not artifacts:
            raise ValueError(f"No templates found in '{template_name}'")

        return artifacts
