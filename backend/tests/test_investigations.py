def test_create_investigation(client, investigation_payload):
    response = client.post("/api/investigations", json=investigation_payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == investigation_payload["title"]
    assert data["risk_score"] == 0
    assert data["risk_label"] == "Low"
    assert data["evidence_items"] == []


def test_generate_markdown_report(client, investigation_payload):
    create_response = client.post("/api/investigations", json=investigation_payload)
    investigation_id = create_response.json()["id"]

    client.post(
        f"/api/investigations/{investigation_id}/notes",
        json={
            "title": "Official courier page differs",
            "type": "External reference",
            "confidence": "High",
            "explanation": "Official courier support page confirms it does not request payment by SMS.",
            "source": "https://example.invalid/courier-security",
        },
    )
    analyze_response = client.post(f"/api/investigations/{investigation_id}/analyze")
    assert analyze_response.status_code == 200

    report_response = client.get(f"/api/investigations/{investigation_id}/report.md")

    assert report_response.status_code == 200
    assert "text/markdown" in report_response.headers["content-type"]
    assert "# ProofGarden Verification Report: Suspicious delivery text" in report_response.text
    assert "Risk Score Explanation" in report_response.text
    assert "Official courier page differs" in report_response.text

