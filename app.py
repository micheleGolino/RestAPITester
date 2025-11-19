import json
from typing import Dict, List, Optional

import requests
import streamlit as st
from pydantic import BaseModel, HttpUrl, ValidationError
import curlify

# Constant MIME types
APPLICATION_JSON = "application/json"

# ------------------------------
# Validation models (simple)
# ------------------------------
class RequestPreset(BaseModel):
    name: str
    method: str
    url: str  # use str for flexibility, validate at runtime
    headers: Dict[str, str] = {}
    params: Dict[str, str] = {}
    auth_type: str = "None"  # None | Bearer | Basic
    bearer_token: Optional[str] = None
    basic_user: Optional[str] = None
    basic_pass: Optional[str] = None
    body_mode: Optional[str] = None  # None | json | raw
    body_raw: str = ""
    timeout_s: float = 20.0
    verify_ssl: bool = True

# ------------------------------
# Utils
# ------------------------------

def kv_rows_to_dict(rows: List[Dict[str, str]]) -> Dict[str, str]:
    """Convert key/value rows to dict, ignoring empty keys."""
    out = {}
    for r in rows:
        k = (r.get("key") or "").strip()
        v = (r.get("value") or "").strip()
        if k:
            out[k] = v
    return out


def build_auth(auth_type: str, bearer: Optional[str], user: Optional[str], pwd: Optional[str]):
    """Return tuple (headers_add, requests_auth) based on auth type."""
    if auth_type == "Bearer" and bearer:
        return ({"Authorization": f"Bearer {bearer}"}, None)
    if auth_type == "Basic" and user is not None:
        return ({}, (user, pwd or ""))
    return ({}, None)


def try_parse_json(s: str):
    """Try to parse JSON; if it fails, return None."""
    try:
        return json.loads(s)
    except Exception:
        return None


# ------------------------------
# UI
# ------------------------------
st.set_page_config(page_title="REST API Tester", layout="wide")
st.title("🧪 REST API Tester")
st.caption("Send HTTP requests and read responses easily.")

# Initialize session state for presets and tables
if "presets" not in st.session_state:
    st.session_state.presets = [] 

# Sidebar: Preset manager
with st.sidebar:
    st.header("Presets")
    preset_names = [p.name for p in st.session_state.presets]
    selected_name = st.selectbox("Load preset", ["—"] + preset_names)
    col_sp = st.columns(2)
    with col_sp[0]:
        new_name = st.text_input("New preset name")
    with col_sp[1]:
        save_clicked = st.button("Save preset", use_container_width=True)

# Main form
with st.form("request_form", clear_on_submit=False):
    top_cols = st.columns([1, 5, 1, 1])
    method = top_cols[0].selectbox("Method", ["GET", "POST", "PUT", "PATCH", "DELETE"])
    url = top_cols[1].text_input("URL", placeholder="https://api.example.com/v1/resource")
    timeout_s = top_cols[2].number_input("Timeout (s)", min_value=1.0, max_value=120.0, value=20.0, step=1.0)
    verify_ssl = top_cols[3].checkbox("Verify SSL", value=True)

    # Tabs to organize input
    t_params, t_headers, t_body, t_auth = st.tabs(["Query Params", "Headers", "Body", "Auth"])

    with t_params:
        st.write("Add query string as key/value rows.")
        params_rows = st.data_editor(
            [{"key": "", "value": ""}],
            num_rows="dynamic",
            use_container_width=True,
        )
    with t_headers:
        st.write("Set custom headers.")
        headers_rows = st.data_editor(
            [{"key": "Accept", "value": APPLICATION_JSON}],
            num_rows="dynamic",
            use_container_width=True,
            key="headers_editor",
        )

    with t_body:
        if method == "GET":
            st.info("GET requests typically do not include a body. Switch to POST, PUT, PATCH, or DELETE to send data.")
            body_mode = None
            body_raw = ""
        else:
            mode_selection = st.radio("Body mode", ["none", "json", "raw"], horizontal=True)
            body_mode = mode_selection if mode_selection != "none" else None
            body_raw = ""
            if body_mode == "json":
                st.caption("Send HTTP requests and read responses easily.")
                body_raw = st.text_area("JSON body", value="{\n  \"example\": true\n}", height=180)
            elif body_mode == "raw":
                st.caption("Raw text. We don't force Content-Type.")
                body_raw = st.text_area("Raw body", value="", height=180)

    with t_auth:
        auth_type = st.radio("Auth type", ["None", "Bearer", "Basic"], horizontal=True)
        bearer_token = basic_user = basic_pass = None
        if auth_type == "Bearer":
            bearer_token = st.text_input("Bearer token", type="password")
        elif auth_type == "Basic":
            basic_user = st.text_input("Username")
            basic_pass = st.text_input("Password", type="password")

    submitted = st.form_submit_button("Send request", use_container_width=True)

# Load preset
if selected_name != "—":
    # Find preset and populate fields (simple: show info in center)
    sel = next((p for p in st.session_state.presets if p.name == selected_name), None)
    if sel:
        st.info(f"Preset selected: {sel.name}")

# Save preset
if save_clicked:
    try:
        preset = RequestPreset(
            name=new_name.strip() or "Preset",
            method=method,
            url=url,
            headers=kv_rows_to_dict(headers_rows),
            params=kv_rows_to_dict(params_rows),
            auth_type=auth_type,
            bearer_token=bearer_token,
            basic_user=basic_user,
            basic_pass=basic_pass,
            body_mode=body_mode,
            body_raw=body_raw,
            timeout_s=timeout_s,
            verify_ssl=verify_ssl,
        )
        # replace if name exists
        st.session_state.presets = [p for p in st.session_state.presets if p.name != preset.name]
        st.session_state.presets.append(preset)
        st.success(f"Saved preset: {preset.name}")
    except ValidationError as e:
        st.error(str(e))

# Caricamento preset
if selected_name != "—":
    # Trova preset e riempi i campi (semplice: mostriamo info al centro)
    sel = next((p for p in st.session_state.presets if p.name == selected_name), None)
    if sel:
        st.info(f"Preset selected: {sel.name}")

# Salvataggio preset
if save_clicked:
    try:
        preset = RequestPreset(
            name=new_name.strip() or "Preset",
            method=method,
            url=url,
            headers=kv_rows_to_dict(headers_rows),
            params=kv_rows_to_dict(params_rows),
            auth_type=auth_type,
            bearer_token=bearer_token,
            basic_user=basic_user,
            basic_pass=basic_pass,
            body_mode=body_mode,
            body_raw=body_raw,
            timeout_s=timeout_s,
            verify_ssl=verify_ssl,
        )
        # sostituisci se nome esiste
        st.session_state.presets = [p for p in st.session_state.presets if p.name != preset.name]
        st.session_state.presets.append(preset)
        st.success(f"Saved preset: {preset.name}")
    except ValidationError as e:
        st.error(str(e))

# Send request
if submitted:
    # validate URL minimum
    if not url.strip().startswith("http"):
        st.error("Invalid URL. Must start with http or https.")
    else:
        headers = kv_rows_to_dict(headers_rows)
        params = kv_rows_to_dict(params_rows)

        # auth
        auth_headers, requests_auth = build_auth(auth_type, bearer_token, basic_user, basic_pass)
        headers.update(auth_headers)

        data = None
        json_payload = None
        if body_mode == "json" and body_raw.strip():
            parsed = try_parse_json(body_raw)
            json_payload = parsed
            headers.setdefault("Content-Type", APPLICATION_JSON)
        elif body_mode == "raw":
            data = body_raw
            headers.setdefault("Content-Type", "application/json")

        try:
            with st.spinner("Sending..."):
                resp = requests.request(
                    method=method,
                    url=url,
                    params=params or None,
                    headers=headers or None,
                    data=data,
                    json=json_payload,
                    auth=requests_auth,
                    timeout=timeout_s,
                    verify=verify_ssl,
                )
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
            st.stop()

        # Response panel
        st.subheader("Response")
        m_cols = st.columns([1, 1, 2])
        with m_cols[0]:
            st.metric("Status", f"{resp.status_code}")
        with m_cols[1]:
            st.metric("Elapsed", f"{resp.elapsed.total_seconds():.3f}s")
        with m_cols[2]:
            st.text("Final URL")
            st.code(resp.url, language="text")

        # Headers
        with st.expander("Response headers"):
            st.json(dict(resp.headers))

        # Body viewer
        content_type = resp.headers.get("Content-Type", "")
        show_as_json = "application/json" in content_type
        if show_as_json:
            try:
                st.json(resp.json())
            except Exception:
                st.text(resp.text)
        else:
            # try JSON even if header doesn't declare it
            parsed = try_parse_json(resp.text)
            if parsed is not None:
                st.json(parsed)
            else:
                st.text_area("Body", value=resp.text, height=300)

        # Download response
        st.download_button(
            label="Download response as file",
            data=resp.content,
            file_name="response.bin",
        )

        # Show curl
        try:
            prepared = requests.Request(
                method=method,
                url=url,
                params=params or None,
                headers=headers or None,
                data=data,
                json=json_payload,
            ).prepare()
            curl_cmd = curlify.to_curl(prepared)
            st.subheader("cURL preview")
            st.code(curl_cmd, language="bash")
        except Exception:
            pass

    # Footer / Help
    with st.expander("ℹ️ Help and notes"):
        st.markdown(
            """
            - **Timeout**: Avoid blocking calls.
            - **Verify SSL**: Disable only in test environments.
            - **Body JSON**: Must be valid JSON.
            - **Auth**: Bearer adds the `Authorization` header.
            - **Presets**: Save recurring combinations.
            """
        )
        st.metric("Status", f"{resp.status_code}")
    with m_cols[1]:
        st.metric("Elapsed", f"{resp.elapsed.total_seconds():.3f}s")
    with m_cols[2]:
        st.text("Final URL")
        st.code(resp.url, language="text")

    # Headers
    with st.expander("Response headers"):
        st.json(dict(resp.headers))

    # Body viewer
    content_type = resp.headers.get("Content-Type", "")
    show_as_json = "application/json" in content_type
    if show_as_json:
        try:
            st.json(resp.json())
        except Exception:
            st.text(resp.text)
    else:
        # try JSON even if header doesn't declare it
        parsed = try_parse_json(resp.text)
        if parsed is not None:
            st.json(parsed)
        else:
            st.text_area("Body", value=resp.text, height=300)

    # Unique key for download button to avoid Streamlit warning
    download_key = f"download_response_{resp.status_code}_{resp.elapsed.total_seconds()}_{resp.headers.get('Content-Length', 'unknown')}"

    # Download response
    st.download_button(
        label="Download response as file",
        data=resp.content,
        file_name="response.bin",
        key=download_key,
    )

    # Show curl
    try:
        prepared = requests.Request(
            method=method,
            url=url,
            params=params or None,
            headers=headers or None,
            data=data,
            json=json_payload,
        ).prepare()
        curl_cmd = curlify.to_curl(prepared)
        st.subheader("cURL preview")
        st.code(curl_cmd, language="bash")
    except Exception:
        pass

# Footer / Help
with st.expander("ℹ️ Help and notes"):
    st.markdown(
        """
        - **Timeout**: Avoid blocking calls.
        - **Verify SSL**: Disable only in test environments.
        - **Body JSON**: Must be valid JSON.
        - **Auth**: Bearer adds the `Authorization` header.
        - **Presets**: Save recurring combinations.
        """
    )
    
