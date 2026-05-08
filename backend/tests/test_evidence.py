def test_upload_text_evidence_and_add_note(client, investigation_payload):
    create_response = client.post("/api/investigations", json=investigation_payload)
    investigation_id = create_response.json()["id"]

    upload_response = client.post(
        f"/api/investigations/{investigation_id}/upload",
        files={
            "file": (
                "delivery-warning.txt",
                b"Final warning: your package is held. Pay now at https://bit.ly/fake-parcel",
                "text/plain",
            )
        },
    )
    assert upload_response.status_code == 201
    evidence = upload_response.json()
    assert evidence["file_name"] == "delivery-warning.txt"
    assert evidence["file_size"] > 0

    note_response = client.post(
        f"/api/investigations/{investigation_id}/notes",
        json={
            "title": "Shortened payment link",
            "type": "Known scam pattern",
            "confidence": "High",
            "explanation": "The message pressures the user to pay through a shortened link.",
            "source": "Analyst note",
        },
    )
    assert note_response.status_code == 201
    assert note_response.json()["confidence"] == "High"

    analyze_response = client.post(f"/api/investigations/{investigation_id}/analyze")
    assert analyze_response.status_code == 200
    data = analyze_response.json()
    assert data["risk"]["score"] >= 50
    assert any(finding["module"] == "text_patterns" for finding in data["findings"])


def test_list_evidence(client, investigation_payload):
    investigation_id = client.post("/api/investigations", json=investigation_payload).json()["id"]
    client.post(
        f"/api/investigations/{investigation_id}/upload",
        files={"file": ("note.txt", b"Plain context note", "text/plain")},
    )

    response = client.get(f"/api/investigations/{investigation_id}/evidence")

    assert response.status_code == 200
    assert len(response.json()) == 1

