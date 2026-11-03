import app

client = app.app.test_client()

# 1. Analyst Dashboard
res = client.get('/')
assert res.status_code == 200, f'Dashboard failed: {res.status_code}'
print('[OK] Analyst Dashboard')

# 2. Single Scan Legit
res = client.post('/api/scan', data={'domain': 'kemkes.go.id'})
assert res.status_code == 200, f'Scan failed: {res.status_code}'
data = res.get_json()
assert data['classification'] == 'Legit', f"Expected Legit, got {data['classification']}"
print(f"[OK] Single Scan Legit: {data['domain']} -> {data['classification']} ({data['confidence']}%)")

# 3. Single Scan DGA
res = client.post('/api/scan', data={'domain': 'xkq981mbpzwt74v.biz'})
assert res.status_code == 200, f'Scan failed: {res.status_code}'
data = res.get_json()
assert data['classification'] == 'DGA', f"Expected DGA, got {data['classification']}"
print(f"[OK] Single Scan DGA: {data['domain']} -> {data['classification']} ({data['confidence']}%)")

# 4. Stream Feed
res = client.get('/api/stream/feed')
assert res.status_code == 200
print(f"[OK] Stream Feed, entries: {len(res.get_json())}")

# 5. Stream Simulate
res = client.post('/api/stream/simulate')
assert res.status_code == 200
print('[OK] Stream Simulate')

# 6. Admin Model
res = client.get('/admin/model')
assert res.status_code == 200
print('[OK] Admin Model')

# 7. Admin Threshold
res = client.get('/admin/threshold')
assert res.status_code == 200
res = client.post('/admin/threshold/update', data={'threshold': '0.42'}, follow_redirects=True)
assert res.status_code == 200
print('[OK] Admin Threshold')

# 8. Admin Firewall
res = client.get('/admin/firewall')
assert res.status_code == 200
res = client.get('/admin/firewall/export/iptables')
assert res.status_code == 200 and 'iptables' in res.text
print('[OK] Admin Firewall & Export')

# 9. Admin Dataset
res = client.get('/admin/dataset')
assert res.status_code == 200
print('[OK] Admin Dataset')

# 10. Admin API
res = client.get('/admin/api')
assert res.status_code == 200
print('[OK] Admin API')

# 11. Admin Health
res = client.get('/admin/health')
assert res.status_code == 200
print('[OK] Admin Health')

# 12. Admin Users & Audit Trail
res = client.get('/admin/users')
assert res.status_code == 200
print('[OK] Admin Users & Audit Trail')

# 13. Public API
res = client.post('/api/v1/detect', json={'domain': 'necurs7723910vba.ru'})
assert res.status_code == 200
api_data = res.get_json()
assert api_data['status'] == 'success'
print(f"[OK] Public API Endpoint: {api_data['query']} -> {api_data['classification']}")

print('\n>>> ALL 13 TEST SUITES PASSED SUCCESSFULLY! <<<')

