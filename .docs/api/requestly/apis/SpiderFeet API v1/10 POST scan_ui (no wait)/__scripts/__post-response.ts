pm.test('status 200', function () { pm.response.to.have.status(200); });
pm.test('STARTING', function () { pm.expect(pm.response.json().scan_record.status).to.eql('STARTING'); });