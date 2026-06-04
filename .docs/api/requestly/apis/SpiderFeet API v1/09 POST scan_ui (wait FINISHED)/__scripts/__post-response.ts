pm.test('status 200', function () { pm.response.to.have.status(200); });
var j = pm.response.json();
pm.test('FINISHED', function () { pm.expect(j.scan_record.status).to.eql('FINISHED'); });
pm.test('produced nuggets', function () { pm.expect(j.produced.length).to.be.above(0); });
pm.test('service', function () { pm.expect(j.scan_record.service.module_id).to.eql('sfp_dnsresolve'); });