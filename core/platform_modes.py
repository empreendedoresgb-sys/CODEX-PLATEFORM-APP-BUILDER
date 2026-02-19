from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlatformMode:
    name: str
    description: str
    modules: tuple[str, ...]


PLATFORM_MODES: dict[str, PlatformMode] = {
    "developer": PlatformMode(
        name="developer",
        description="Code-first workspace with architecture and export controls.",
        modules=(
            "project_manager",
            "code_editor",
            "architecture_graph",
            "cli_console",
            "live_preview",
        ),
    ),
    "nocode": PlatformMode(
        name="nocode",
        description="Visual-first builder for non-technical creators.",
        modules=(
            "project_manager",
            "visual_canvas",
            "workflow_editor",
            "data_connectors",
            "template_marketplace",
        ),
    ),
    "hybrid": PlatformMode(
        name="hybrid",
        description="Two-way synchronized visual and code builder.",
        modules=(
            "project_manager",
            "visual_canvas",
            "code_editor",
            "sync_inspector",
            "live_preview",
            "deployment_center",
        ),
    ),
}


def get_mode(name: str) -> PlatformMode:
    normalized = name.lower().strip()
    if normalized not in PLATFORM_MODES:
        supported = ", ".join(sorted(PLATFORM_MODES))
        raise ValueError(f"Unsupported mode '{name}'. Supported modes: {supported}.")
    return PLATFORM_MODES[normalized]
