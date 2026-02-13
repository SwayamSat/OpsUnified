import httpx
import time

BASE_URL = "http://127.0.0.1:8001/api/v1"
# Assuming default demo user from create_user_demo.py
EMAIL = "demo@careops.com"
PASSWORD = "demo123"

def test_full_flow():
    print("Starting End-to-End Test Flow...")
    
    # 1. Login
    print("\n1. Logging in...")
    try:
        resp = httpx.post(f"{BASE_URL}/login/access-token", data={
            "username": EMAIL,
            "password": PASSWORD
        })
        if resp.status_code != 200:
            print(f"Login failed: {resp.status_code} {resp.text}")
            return
        try:
            token = resp.json()["access_token"]
        except:
             print(f"Login response not JSON: {resp.text}")
             return
        headers = {"Authorization": f"Bearer {token}"}
        print("Login success.")
    except Exception as e:
        print(f"Login connection failed: {e}")
        return

    # 2. Get Workspace
    print("\n2. Getting Workspace...")
    resp = httpx.get(f"{BASE_URL}/workspaces/", headers=headers, follow_redirects=True)
    if resp.status_code != 200:
        print(f"Get Workspaces failed: {resp.status_code} {resp.text}")
        return
    try:
        workspaces = resp.json()
    except Exception:
        print(f"Invalid JSON from workspaces: {resp.text}")
        return
    if not workspaces:
        print("No workspaces found.")
        return
    workspace_id = workspaces[0]["id"]
    print(f"Using Workspace ID: {workspace_id}")

    # 3. Create Inventory Item
    print("\n3. Creating Inventory Item...")
    item_payload = {"name": "Test Item", "quantity": 100, "low_stock_threshold": 10}
    resp = httpx.post(f"{BASE_URL}/workspaces/inventory/", json=item_payload, headers=headers)
    if resp.status_code != 200:
        print(f"Create Item failed: {resp.text}")
    else:
        item = resp.json()
        print(f"Item created: {item['id']} - {item['name']} (Qty: {item['quantity']})")
        item_id = item['id']

        # 4. Record Usage
        print("\n4. Recording Usage (5 units)...")
        usage_payload = {"item_id": item_id, "quantity_used": 5}
        resp = httpx.post(f"{BASE_URL}/workspaces/inventory/usage", json=usage_payload, headers=headers)
        if resp.status_code == 200:
            updated_item = resp.json()
            print(f"Usage recorded. New Qty: {updated_item['quantity']}")
            assert updated_item['quantity'] == 95
        else:
            print(f"Usage recording failed: {resp.text}")

    # 5. Create Form Template
    print("\n5. Creating Form Template...")
    form_payload = {
        "name": "Test Contact Form",
        "schema": {"fields": [{"name": "Name", "type": "text"}, {"name": "Message", "type": "text"}]}
    }
    resp = httpx.post(f"{BASE_URL}/workspaces/forms/", json=form_payload, headers=headers)
    if resp.status_code != 200:
        print(f"Create Form failed: {resp.text}")
        return
    template = resp.json()
    template_id = template["id"]
    print(f"Form Template created: {template_id} - {template['name']}")

    # 6. Create Automation Rule
    print("\n6. Creating Automation Rule...")
    rule_payload = {
        "name": "Auto Reply Email",
        "form_template_id": template_id,
        "action_type": "send_email",
        "action_config": {"recipient": "contact"},
        "is_active": 1
    }
    resp = httpx.post(f"{BASE_URL}/workspaces/automation/", json=rule_payload, headers=headers)
    if resp.status_code != 200:
        print(f"Create Rule failed: {resp.text}")
    else:
        print("Automation Rule created.")

    # 7. Submit Form (Public)
    print("\n7. Submitting Form (Public)...")
    submit_payload = {
        "data": {"Name": "John Doe", "Message": "Hello World"},
        "contact_email": "john.doe@example.com"
    }
    # Public endpoint might trigger NEW_CONTACT and FORM_SUBMITTED
    resp = httpx.post(f"{BASE_URL}/public/forms/{template_id}/submit", json=submit_payload)
    if resp.status_code != 200:
        print(f"Form Submission failed: {resp.text}")
    else:
        submission = resp.json()
        print(f"Form Submitted: ID {submission['id']}")
        
        # Verify Submission in Dashboard
        print("\n8. Verifying Submission in Dashboard...")
        resp = httpx.get(f"{BASE_URL}/workspaces/forms/submissions?template_id={template_id}", headers=headers)
        submissions = resp.json()
        found = any(s['id'] == submission['id'] for s in submissions)
        if found:
            print("Submission found in dashboard list.")
        else:
            print("Submission NOT found in dashboard list.")

    print("\nTest Flow Complete.")

if __name__ == "__main__":
    test_full_flow()
