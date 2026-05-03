#!/usr/bin/env python3
"""
Convert confirmed architecture JSON and optional flow JSON into Draw.io.

Usage:
    python scripts/export_to_xml.py .xml/project_architecture.json
    python scripts/export_to_xml.py .xml/project_architecture.json .xml/project_architecture.drawio
    python scripts/export_to_xml.py .xml/project_architecture.json --flows .xml/project_flows.json
    python scripts/export_to_xml.py .xml/project_architecture.json .xml/final.drawio --flows .xml/project_flows.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Any
from xml.dom import minidom

PAGE_MARGIN = 32
MIN_LAYER_WIDTH = 900
LAYER_HEADER_HEIGHT = 34
LAYER_PADDING = 14
LAYER_GAP = 28
FEATURE_WIDTH = 220
FEATURE_HEADER_HEIGHT = 28
FEATURE_GAP = 18
COMPONENT_HEIGHT = 48
COMPONENT_GAP = 10
COMPONENT_PADDING = 10
DRAWIO_VERSION = "22.1.0"
FIXED_MODIFIED = "1970-01-01T00:00:00Z"

ARCHITECTURE_ALLOWED_KEYS = {"layers"}
LAYER_ALLOWED_KEYS = {"label", "child"}
COMPONENT_ALLOWED_KEYS = {"label", "feature"}
FLOWS_ALLOWED_KEYS = {"flows"}
FLOW_ALLOWED_KEYS = {"feature", "label", "exposed_interface", "nodes", "edges"}
REF_ALLOWED_KEYS = {"layer", "label", "feature"}
NODE_ALLOWED_KEYS = {"id", "ref"}
EDGE_ALLOWED_KEYS = {"from", "to", "label", "step"}

LAYER_PALETTES = [
    ("#EAF5FF", "#4A90C2", "#D8ECFF", "#1F4E79"),
    ("#FFF3E8", "#E58A2A", "#FFE1C4", "#7A3E00"),
    ("#F1EAFE", "#8B5BC7", "#E2D3FA", "#4C1D95"),
    ("#EAF7EA", "#58A55C", "#D8F0D8", "#1F5E25"),
    ("#FFF8DF", "#C99A22", "#FFF0B8", "#7A5600"),
    ("#FFEDEF", "#D45A6A", "#FFD6DD", "#8A1F2D"),
    ("#EAF7F7", "#3A9A9A", "#D5F0F0", "#145E5E"),
    ("#F0EEFF", "#7266C9", "#DDD8FF", "#312A80"),
]

NAMED_LAYER_PALETTES = {
    "用户层": ("#EAF5FF", "#4A90C2", "#D8ECFF", "#1F4E79"),
    "前端": ("#FFF3E8", "#E58A2A", "#FFE1C4", "#7A3E00"),
    "接入层": ("#F1EAFE", "#8B5BC7", "#E2D3FA", "#4C1D95"),
    "网关层": ("#F1EAFE", "#8B5BC7", "#E2D3FA", "#4C1D95"),
    "网关与接入层": ("#F1EAFE", "#8B5BC7", "#E2D3FA", "#4C1D95"),
    "前端服务层": ("#EAF7EA", "#58A55C", "#D8F0D8", "#1F5E25"),
    "对外接口层": ("#EAF7EA", "#58A55C", "#D8F0D8", "#1F5E25"),
    "DTO层": ("#EAF7EA", "#58A55C", "#D8F0D8", "#1F5E25"),
    "服务层": ("#FFF8DF", "#C99A22", "#FFF0B8", "#7A5600"),
    "核心业务服务层": ("#FFF8DF", "#C99A22", "#FFF0B8", "#7A5600"),
    "核心业务服务层（微服务）": ("#FFF8DF", "#C99A22", "#FFF0B8", "#7A5600"),
    "中间件层": ("#FFEDEF", "#D45A6A", "#FFD6DD", "#8A1F2D"),
    "Repository层": ("#FFEDEF", "#D45A6A", "#FFD6DD", "#8A1F2D"),
    "数据存储层": ("#FFEDEF", "#D45A6A", "#FFD6DD", "#8A1F2D"),
    "基础设施层": ("#F0EEFF", "#7266C9", "#DDD8FF", "#312A80"),
    "部署层": ("#F0EEFF", "#7266C9", "#DDD8FF", "#312A80"),
    "运维监控层": ("#F0EEFF", "#7266C9", "#DDD8FF", "#312A80"),
}


def stable_id(*parts: object) -> str:
    text = "|".join(str(part) for part in parts)
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
    return f"id_{digest}"


def require_keys(value: dict[str, Any], allowed: set[str], context: str) -> None:
    extra = set(value) - allowed
    missing = allowed - set(value)
    if extra:
        raise ValueError(f"{context} contains unsupported field(s): {', '.join(sorted(extra))}.")
    if missing:
        raise ValueError(f"{context} is missing required field(s): {', '.join(sorted(missing))}.")


def require_non_empty_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context} must be a non-empty string.")
    return value


def ref_key(ref: dict[str, Any]) -> tuple[str, str, str]:
    return (
        require_non_empty_string(ref.get("layer"), "ref.layer"),
        require_non_empty_string(ref.get("label"), "ref.label"),
        require_non_empty_string(ref.get("feature"), "ref.feature"),
    )


def component_key(layer_label: str, component: dict[str, Any]) -> tuple[str, str, str]:
    return (
        layer_label,
        require_non_empty_string(component.get("label"), "component.label"),
        require_non_empty_string(component.get("feature"), "component.feature"),
    )


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return data


def validate_architecture(data: dict[str, Any]) -> tuple[list[dict[str, Any]], set[tuple[str, str, str]]]:
    require_keys(data, ARCHITECTURE_ALLOWED_KEYS, "Top-level architecture JSON")
    layers = data["layers"]
    if not isinstance(layers, list) or not layers:
        raise ValueError("'layers' must be a non-empty array.")

    registry: set[tuple[str, str, str]] = set()
    seen_layers: set[str] = set()

    for layer_index, layer in enumerate(layers):
        if not isinstance(layer, dict):
            raise ValueError(f"Layer at index {layer_index} must be an object.")
        require_keys(layer, LAYER_ALLOWED_KEYS, f"Layer at index {layer_index}")

        layer_label = require_non_empty_string(layer["label"], f"Layer at index {layer_index} label")
        if layer_label in seen_layers:
            raise ValueError(f"Layer label '{layer_label}' is duplicated.")
        seen_layers.add(layer_label)

        children = layer["child"]
        if not isinstance(children, list):
            raise ValueError(f"Layer '{layer_label}' child must be an array.")

        seen_components_in_layer: set[tuple[str, str]] = set()
        for component_index, component in enumerate(children):
            if not isinstance(component, dict):
                raise ValueError(f"Component at layer '{layer_label}' index {component_index} must be an object.")
            require_keys(component, COMPONENT_ALLOWED_KEYS, f"Component at layer '{layer_label}' index {component_index}")

            label = require_non_empty_string(component["label"], f"Component at layer '{layer_label}' label")
            feature = require_non_empty_string(component["feature"], f"Component '{label}' feature")
            local_key = (label, feature)
            if local_key in seen_components_in_layer:
                raise ValueError(f"Component '{label}' with feature '{feature}' is duplicated in layer '{layer_label}'.")
            seen_components_in_layer.add(local_key)
            registry.add((layer_label, label, feature))

    return layers, registry


def validate_ref(ref: Any, registry: set[tuple[str, str, str]], context: str) -> dict[str, str]:
    if not isinstance(ref, dict):
        raise ValueError(f"{context} must be an object.")
    require_keys(ref, REF_ALLOWED_KEYS, context)
    key = ref_key(ref)
    if key not in registry:
        raise ValueError(
            f"{context} references unknown architecture component: "
            f"layer='{key[0]}', label='{key[1]}', feature='{key[2]}'."
        )
    return {"layer": key[0], "label": key[1], "feature": key[2]}


def validate_flows(data: dict[str, Any], registry: set[tuple[str, str, str]]) -> list[dict[str, Any]]:
    require_keys(data, FLOWS_ALLOWED_KEYS, "Top-level flow JSON")
    flows = data["flows"]
    if not isinstance(flows, list) or not flows:
        raise ValueError("'flows' must be a non-empty array.")

    validated: list[dict[str, Any]] = []
    for flow_index, flow in enumerate(flows):
        if not isinstance(flow, dict):
            raise ValueError(f"Flow at index {flow_index} must be an object.")
        require_keys(flow, FLOW_ALLOWED_KEYS, f"Flow at index {flow_index}")

        label = require_non_empty_string(flow["label"], f"Flow at index {flow_index} label")
        feature = require_non_empty_string(flow["feature"], f"Flow '{label}' feature")
        exposed_interface = validate_ref(flow["exposed_interface"], registry, f"Flow '{label}' exposed_interface")

        nodes = flow["nodes"]
        if not isinstance(nodes, list) or not nodes:
            raise ValueError(f"Flow '{label}' nodes must be a non-empty array.")
        node_by_id: dict[str, dict[str, Any]] = {}
        for node_index, node in enumerate(nodes):
            if not isinstance(node, dict):
                raise ValueError(f"Flow '{label}' node at index {node_index} must be an object.")
            require_keys(node, NODE_ALLOWED_KEYS, f"Flow '{label}' node at index {node_index}")
            node_id = require_non_empty_string(node["id"], f"Flow '{label}' node id")
            if node_id in node_by_id:
                raise ValueError(f"Flow '{label}' contains duplicate node id '{node_id}'.")
            node_by_id[node_id] = {
                "id": node_id,
                "ref": validate_ref(node["ref"], registry, f"Flow '{label}' node '{node_id}' ref"),
            }

        edges = flow["edges"]
        if not isinstance(edges, list) or not edges:
            raise ValueError(f"Flow '{label}' edges must be a non-empty array.")
        validated_edges: list[dict[str, str]] = []
        for edge_index, edge in enumerate(edges):
            if not isinstance(edge, dict):
                raise ValueError(f"Flow '{label}' edge at index {edge_index} must be an object.")
            require_keys(edge, EDGE_ALLOWED_KEYS, f"Flow '{label}' edge at index {edge_index}")
            source = require_non_empty_string(edge["from"], f"Flow '{label}' edge from")
            target = require_non_empty_string(edge["to"], f"Flow '{label}' edge to")
            if source not in node_by_id:
                raise ValueError(f"Flow '{label}' edge references unknown source node '{source}'.")
            if target not in node_by_id:
                raise ValueError(f"Flow '{label}' edge references unknown target node '{target}'.")
            validated_edges.append(
                {
                    "from": source,
                    "to": target,
                    "label": require_non_empty_string(edge["label"], f"Flow '{label}' edge label"),
                    "step": require_non_empty_string(edge["step"], f"Flow '{label}' edge step"),
                }
            )

        validated.append(
            {
                "feature": feature,
                "label": label,
                "exposed_interface": exposed_interface,
                "nodes": list(node_by_id.values()),
                "edges": validated_edges,
            }
        )

    return validated


def layer_palette(layer_label: str, index: int) -> tuple[str, str, str, str]:
    return NAMED_LAYER_PALETTES.get(layer_label, LAYER_PALETTES[index % len(LAYER_PALETTES)])


def collect_feature_order(layers: list[dict[str, Any]]) -> list[str]:
    order: list[str] = []
    seen: set[str] = set()
    for layer in layers:
        for component in layer["child"]:
            feature = str(component["feature"])
            if feature not in seen:
                seen.add(feature)
                order.append(feature)
    return order or ["default"]


def group_components_by_feature(layer: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for component in layer["child"]:
        grouped[str(component["feature"])].append(component)
    return grouped


def compute_layout(layers: list[dict[str, Any]]) -> dict[str, Any]:
    features = collect_feature_order(layers)
    feature_x = {feature: LAYER_PADDING + index * (FEATURE_WIDTH + FEATURE_GAP) for index, feature in enumerate(features)}
    layer_width = max(
        MIN_LAYER_WIDTH,
        2 * LAYER_PADDING + len(features) * FEATURE_WIDTH + max(0, len(features) - 1) * FEATURE_GAP,
    )

    layer_layouts: list[dict[str, Any]] = []
    current_y = PAGE_MARGIN
    for index, layer in enumerate(layers):
        grouped = group_components_by_feature(layer)
        max_count = max([len(items) for items in grouped.values()] or [1])
        feature_height = (
            FEATURE_HEADER_HEIGHT
            + COMPONENT_PADDING
            + max_count * COMPONENT_HEIGHT
            + max(0, max_count - 1) * COMPONENT_GAP
            + COMPONENT_PADDING
        )
        layer_height = LAYER_HEADER_HEIGHT + LAYER_PADDING + feature_height + LAYER_PADDING
        layer_layouts.append(
            {
                "layer": layer,
                "index": index,
                "x": PAGE_MARGIN,
                "y": current_y,
                "width": layer_width,
                "height": layer_height,
                "feature_height": feature_height,
                "grouped": grouped,
                "palette": layer_palette(str(layer["label"]), index),
            }
        )
        current_y += layer_height + LAYER_GAP

    return {
        "features": features,
        "feature_x": feature_x,
        "layers": layer_layouts,
        "page_width": layer_width + 2 * PAGE_MARGIN,
        "page_height": max(current_y - LAYER_GAP + PAGE_MARGIN, 720),
    }


def add_geometry(node: ET.Element, x: int, y: int, width: int, height: int) -> None:
    ET.SubElement(
        node,
        "mxGeometry",
        x=str(x),
        y=str(y),
        width=str(width),
        height=str(height),
        **{"as": "geometry"},
    )


def add_edge_geometry(node: ET.Element) -> None:
    ET.SubElement(node, "mxGeometry", relative="1", **{"as": "geometry"})


def layer_style(fill: str, stroke: str, font_color: str) -> str:
    return (
        "swimlane;whiteSpace=wrap;html=1;rounded=0;collapsible=0;"
        f"startSize={LAYER_HEADER_HEIGHT};fillColor={fill};strokeColor={stroke};"
        f"fontStyle=1;fontColor={font_color};strokeWidth=1.5;"
    )


def feature_style(fill: str, stroke: str, font_color: str, muted: bool = False) -> str:
    opacity = "opacity=35;textOpacity=55;" if muted else ""
    return (
        "swimlane;whiteSpace=wrap;html=1;rounded=1;arcSize=6;collapsible=0;"
        f"startSize={FEATURE_HEADER_HEIGHT};fillColor=#FFFFFF;gradientColor={fill};"
        f"strokeColor={stroke};fontStyle=1;fontColor={font_color};{opacity}"
    )


def component_style(fill: str, stroke: str, font_color: str, active: bool, muted: bool) -> str:
    if active:
        return (
            "rounded=1;whiteSpace=wrap;html=1;arcSize=8;spacing=8;"
            "fillColor=#FFF7ED;strokeColor=#EA580C;fontColor=#111827;"
            "strokeWidth=2;"
        )
    if muted:
        return (
            "rounded=1;whiteSpace=wrap;html=1;arcSize=8;spacing=8;"
            f"fillColor={fill};strokeColor={stroke};fontColor={font_color};"
            "opacity=12;textOpacity=20;"
        )
    return (
        "rounded=1;whiteSpace=wrap;html=1;arcSize=8;spacing=8;"
        f"fillColor={fill};strokeColor={stroke};fontColor={font_color};strokeWidth=1;"
    )


def placeholder_style() -> str:
    return "rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;fontColor=#64748B;dashed=1;"


def structural_edge_style() -> str:
    return "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;strokeColor=#94A3B8;strokeWidth=1;dashed=1;"


def flow_edge_style() -> str:
    return "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;strokeColor=#2563EB;fontColor=#1D4ED8;strokeWidth=2;"


def component_cell_id(page_slug: str, key: tuple[str, str, str]) -> str:
    return stable_id(page_slug, "component", key[0], key[1], key[2])


def draw_architecture_cells(
    root: ET.Element,
    layout: dict[str, Any],
    page_slug: str,
    active_refs: set[tuple[str, str, str]] | None = None,
) -> tuple[dict[tuple[str, str, str], str], list[str]]:
    component_ids: dict[tuple[str, str, str], str] = {}
    layer_ids: list[str] = []
    flow_mode = active_refs is not None
    active_refs = active_refs or set()

    for layer_layout in layout["layers"]:
        layer = layer_layout["layer"]
        layer_label = str(layer["label"])
        fill, stroke, component_fill, font_color = layer_layout["palette"]
        layer_id = stable_id(page_slug, "layer", layer_layout["index"], layer_label)
        layer_ids.append(layer_id)

        layer_cell = ET.SubElement(
            root,
            "mxCell",
            id=layer_id,
            value=layer_label,
            style=layer_style(fill, stroke, font_color),
            vertex="1",
            parent="1",
        )
        add_geometry(layer_cell, layer_layout["x"], layer_layout["y"], layer_layout["width"], layer_layout["height"])

        grouped = layer_layout["grouped"]
        if not grouped:
            placeholder = ET.SubElement(
                root,
                "mxCell",
                id=stable_id(page_slug, "placeholder", layer_label),
                value="无组件",
                style=placeholder_style(),
                vertex="1",
                parent=layer_id,
            )
            add_geometry(
                placeholder,
                LAYER_PADDING,
                LAYER_HEADER_HEIGHT + LAYER_PADDING,
                FEATURE_WIDTH,
                COMPONENT_HEIGHT,
            )
            continue

        for feature in layout["features"]:
            components = grouped.get(feature)
            if not components:
                continue

            group_key_refs = {component_key(layer_label, component) for component in components}
            group_muted = flow_mode and active_refs.isdisjoint(group_key_refs)
            group_id = stable_id(page_slug, "feature", layer_label, feature)
            group_cell = ET.SubElement(
                root,
                "mxCell",
                id=group_id,
                value=feature,
                style=feature_style(fill, stroke, font_color, group_muted),
                vertex="1",
                parent=layer_id,
            )
            add_geometry(
                group_cell,
                layout["feature_x"][feature],
                LAYER_HEADER_HEIGHT + LAYER_PADDING,
                FEATURE_WIDTH,
                layer_layout["feature_height"],
            )

            component_y = FEATURE_HEADER_HEIGHT + COMPONENT_PADDING
            for component in components:
                key = component_key(layer_label, component)
                active = flow_mode and key in active_refs
                muted = flow_mode and key not in active_refs
                cell_id = component_cell_id(page_slug, key)
                component_ids[key] = cell_id
                cell = ET.SubElement(
                    root,
                    "mxCell",
                    id=cell_id,
                    value=str(component["label"]),
                    style=component_style(component_fill, stroke, font_color, active, muted),
                    vertex="1",
                    parent=group_id,
                    layer=layer_label,
                    feature=str(component["feature"]),
                )
                add_geometry(
                    cell,
                    COMPONENT_PADDING,
                    component_y,
                    FEATURE_WIDTH - 2 * COMPONENT_PADDING,
                    COMPONENT_HEIGHT,
                )
                component_y += COMPONENT_HEIGHT + COMPONENT_GAP

    return component_ids, layer_ids


def add_structural_edges(root: ET.Element, page_slug: str, layer_ids: list[str]) -> None:
    for index, (source, target) in enumerate(zip(layer_ids, layer_ids[1:])):
        edge = ET.SubElement(
            root,
            "mxCell",
            id=stable_id(page_slug, "structural-edge", index, source, target),
            value="",
            style=structural_edge_style(),
            edge="1",
            parent="1",
            source=source,
            target=target,
        )
        add_edge_geometry(edge)


def add_flow_edges(
    root: ET.Element,
    page_slug: str,
    flow: dict[str, Any],
    component_ids: dict[tuple[str, str, str], str],
) -> None:
    node_refs = {node["id"]: ref_key(node["ref"]) for node in flow["nodes"]}
    for index, edge_data in enumerate(flow["edges"]):
        source_key = node_refs[edge_data["from"]]
        target_key = node_refs[edge_data["to"]]
        edge = ET.SubElement(
            root,
            "mxCell",
            id=stable_id(page_slug, "flow-edge", index, edge_data["from"], edge_data["to"], edge_data["label"]),
            value=f"{edge_data['step']}\n{edge_data['label']}",
            style=flow_edge_style(),
            edge="1",
            parent="1",
            source=component_ids[source_key],
            target=component_ids[target_key],
        )
        add_edge_geometry(edge)


def create_graph_model(root: ET.Element, layout: dict[str, Any]) -> ET.Element:
    model = ET.Element(
        "mxGraphModel",
        dx="1422",
        dy="794",
        grid="1",
        gridSize="10",
        guides="1",
        tooltips="1",
        connect="1",
        arrows="1",
        fold="1",
        page="1",
        pageScale="1",
        pageWidth=str(layout["page_width"]),
        pageHeight=str(layout["page_height"]),
        math="0",
        shadow="0",
    )
    model.append(root)
    return model


def create_root() -> ET.Element:
    root = ET.Element("root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")
    return root


def build_architecture_diagram(layout: dict[str, Any]) -> ET.Element:
    page_slug = "architecture"
    root = create_root()
    _, layer_ids = draw_architecture_cells(root, layout, page_slug)
    add_structural_edges(root, page_slug, layer_ids)

    diagram = ET.Element("diagram", id=stable_id(page_slug, "diagram"), name="架构图")
    diagram.append(create_graph_model(root, layout))
    return diagram


def build_flow_diagram(layout: dict[str, Any], flow: dict[str, Any], index: int) -> ET.Element:
    page_slug = f"flow-{index}-{flow['label']}"
    active_refs = {ref_key(node["ref"]) for node in flow["nodes"]}
    active_refs.add(ref_key(flow["exposed_interface"]))

    root = create_root()
    component_ids, _ = draw_architecture_cells(root, layout, page_slug, active_refs)
    add_flow_edges(root, page_slug, flow, component_ids)

    diagram = ET.Element("diagram", id=stable_id(page_slug, "diagram"), name=str(flow["label"]))
    diagram.append(create_graph_model(root, layout))
    return diagram


def build_drawio(layers: list[dict[str, Any]], flows: list[dict[str, Any]] | None = None) -> ET.Element:
    layout = compute_layout(layers)
    mxfile = ET.Element(
        "mxfile",
        host="app.diagrams.net",
        modified=FIXED_MODIFIED,
        agent="xml-architecture-designer",
        version=DRAWIO_VERSION,
        type="device",
    )
    mxfile.append(build_architecture_diagram(layout))
    for index, flow in enumerate(flows or [], start=1):
        mxfile.append(build_flow_diagram(layout, flow, index))
    return mxfile


def prettify_xml(element: ET.Element) -> str:
    rough = ET.tostring(element, encoding="utf-8")
    parsed = minidom.parseString(rough)
    return parsed.toprettyxml(indent="  ")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export architecture and optional flow JSON to Draw.io.")
    parser.add_argument("architecture_json", help="Path to architecture JSON.")
    parser.add_argument("output_drawio", nargs="?", help="Optional output .drawio path.")
    parser.add_argument("--flows", help="Optional flow JSON path for multi-page flow diagrams.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    architecture_path = Path(args.architecture_json)
    output_path = Path(args.output_drawio) if args.output_drawio else architecture_path.with_suffix(".drawio")

    try:
        architecture_data = load_json(architecture_path)
        layers, registry = validate_architecture(architecture_data)

        flows = None
        if args.flows:
            flow_data = load_json(Path(args.flows))
            flows = validate_flows(flow_data, registry)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(prettify_xml(build_drawio(layers, flows)), encoding="utf-8")
    except Exception as exc:  # noqa: BLE001 - CLI should return a readable validation failure.
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    page_count = 1 + (len(flows) if flows else 0)
    print(f"Successfully generated {output_path} ({page_count} page{'s' if page_count != 1 else ''})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
