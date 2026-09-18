'use strict';

const assert = require('assert');
const api = require('../diagnostic/assets/admission-diagnostic.js');

const report = api.buildReport([
    {
        formIdentityMatched: true,
        presentationAdmitted: true,
        renderingContext: 'registration',
        exclusionReason: null,
        fieldValue: 'SHOULD_NOT_APPEAR',
        label: 'SHOULD_NOT_APPEAR'
    },
    {
        formIdentityMatched: true,
        presentationAdmitted: false,
        renderingContext: 'gravity_flow_entry_detail',
        exclusionReason: 'gravity_flow_entry_detail',
        entryValue: 'SHOULD_NOT_APPEAR'
    },
    {
        formIdentityMatched: true,
        presentationAdmitted: null,
        renderingContext: 'invented-context',
        exclusionReason: 'invented-reason'
    }
]);

assert.strictEqual(report.schemaVersion, 'v0.1');
assert.strictEqual(report.diagnosticVersion, '0.3.1');
assert.strictEqual(report.diagnosticMode, 'admin-gated-read-only-context-admission');
assert.strictEqual(report.admissionDecisions.length, 3);
assert.deepStrictEqual(report.admissionDecisions[0], {
    formIdentityMatched: true,
    presentationAdmitted: true,
    renderingContext: 'registration',
    exclusionReason: null
});
assert.deepStrictEqual(report.admissionDecisions[1], {
    formIdentityMatched: true,
    presentationAdmitted: false,
    renderingContext: 'gravity_flow_entry_detail',
    exclusionReason: 'gravity_flow_entry_detail'
});
assert.deepStrictEqual(report.admissionDecisions[2], {
    formIdentityMatched: true,
    presentationAdmitted: null,
    renderingContext: 'unknown',
    exclusionReason: null
});
assert.ok(!JSON.stringify(report).includes('SHOULD_NOT_APPEAR'), 'arbitrary/private fields leaked into admission report');

const overflow = api.buildReport(Array.from({ length: api.MAX_DECISIONS + 3 }, () => ({
    formIdentityMatched: true,
    presentationAdmitted: true,
    renderingContext: 'registration',
    exclusionReason: null
})));
assert.strictEqual(overflow.admissionDecisions.length, api.MAX_DECISIONS, 'admission decision budget not enforced');
assert.strictEqual(overflow.truncated, true, 'admission decision truncation not reported');

const appended = [];
const documentObject = {
    getElementById: () => null,
    createTextNode: (value) => ({ nodeType: 3, data: value }),
    createElement: () => ({
        style: {},
        setAttribute() {},
        appendChild(node) { this.child = node; },
        addEventListener() {},
        click() {},
        remove() {}
    }),
    body: { appendChild(node) { appended.push(node); } }
};
const button = api.ensureDownloadControl(documentObject);
assert.ok(button, 'admission download control unavailable');
assert.strictEqual(button.id, 'gtb-srwf-download-admission-report');
assert.strictEqual(appended.length, 1, 'admission download control not appended');

console.log('PASS: admission diagnostic v0.3.1 bounded/privacy-safe context fixture');
