from __future__ import annotations

import html
import json


def render_html_report(report: dict) -> str:
    finding = html.escape(str(report.get("finding", "unverified")))
    outcome = html.escape(str(report.get("outcome", "incomplete")))
    camera = html.escape(str(report.get("camera_id", "unknown")))
    categories = ", ".join(html.escape(str(x)) for x in report.get("evidence_classes", [])) or "UNVERIFIED"
    regions = report.get("regions") or []
    region_rows = "".join(
        f"<tr><th>{html.escape(str(region.get('region_id')))}</th><td>{html.escape(str(region.get('visual_cue')))}</td>"
        f"<td>{html.escape(str(region.get('bbox')))}</td><td>{region.get('pixel_area', 0)}</td></tr>"
        for region in regions
    ) or '<tr><td colspan="4">No qualifying candidate region</td></tr>'
    steps = "".join(
        f"<li><strong>{html.escape(str(step.get('selected_action')))}</strong> — "
        f"{html.escape(json.dumps(step.get('result', {}), ensure_ascii=False, sort_keys=True))}</li>"
        for step in report.get("trace", [])
    )
    hashes = "".join(f"<li><code>{html.escape(key)}: {html.escape(value)}</code></li>"
                      for key, value in (report.get("sha256") or {}).items())
    demo = '<p class="notice">Synthetic test fixture. Not real facility footage or validation.</p>' if report.get("synthetic_demo") else ''
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Incident evidence report</title><style>body{{font:16px/1.55 system-ui,sans-serif;max-width:960px;margin:36px auto;padding:0 18px;color:#211d27}}h1,h2{{line-height:1.2}}.notice{{background:#f5efff;padding:12px;border-left:4px solid #7152c7}}table{{border-collapse:collapse;width:100%}}th,td{{text-align:left;padding:8px;border-bottom:1px solid #ddd}}code{{overflow-wrap:anywhere;font-size:12px}}li{{margin:8px 0}}</style></head><body>
<header><p>FORTIFIERS INCIDENT MEMORY · EVIDENCE REPORT</p><h1>{finding}</h1><p>Outcome: <strong>{outcome}</strong> · Camera: {camera}</p>{demo}</header>
<section><h2>Evidence classifications</h2><p>{categories}</p><p>A visual appearance does not establish physical water presence or incident cause. Human review is required before consequential action.</p></section>
<section><h2>Candidate visual regions</h2><table><thead><tr><th>Region</th><th>Visual cue</th><th>Pixel box</th><th>Pixels</th></tr></thead><tbody>{region_rows}</tbody></table></section>
<section><h2>Agent investigation trace</h2><ol>{steps}</ol></section><section><h2>SHA-256 evidence hashes</h2><ul>{hashes}</ul></section>
<footer><p>Generated at {html.escape(str(report.get('created_at', 'unknown')))} · This is decision support, not a certified life-safety system.</p></footer></body></html>"""
