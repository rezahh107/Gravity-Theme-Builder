'use strict';
const assert = require('assert');
const api = require('../diagnostic/assets/admission-diagnostic.js');

const admitted = api.safeDecision({
    formIdentityMatched: true,
    presentationAdmitted: true,
    renderingContext: 'registration',
    contextEvidence: 'registration_default',
    exclusionReason: null,
    privateExtra: 'discard-me'
});
assert.deepStrictEqual(admitted, {
    formIdentityMatched: true,
    presentationAdmitted: true,
    renderingContext: 'registration',
    contextEvidence: 'registration_default',
    exclusionReason: null
});

const excluded = api.safeDecision({
    formIdentityMatched: true,
    presentationAdmitted: false,
    renderingContext: 'gravity_flow_entry_detail',
    contextEvidence: 'gravity_flow_early_enqueue',
    exclusionReason: 'gravity_flow_entry_detail'
});
assert.strictEqual(excluded.presentationAdmitted, false);
assert.strictEqual(excluded.contextEvidence, 'gravity_flow_early_enqueue');

const unknown = api.safeDecision({ renderingContext: 'invented', contextEvidence: 'invented', exclusionReason: 'invented' });
assert.strictEqual(unknown.renderingContext, 'unknown');
assert.strictEqual(unknown.contextEvidence, 'unknown');
assert.strictEqual(unknown.exclusionReason, null);

const styleDoc = { getElementById: (id) => id === 'srwf-registration-theme-css' ? {} : null };
const cleanDoc = { getElementById: () => null };
assert.strictEqual(api.stylesheetPresent(styleDoc), true);
assert.strictEqual(api.stylesheetPresent(cleanDoc), false);

const report = api.buildReport(Array.from({ length: 10 }, () => excluded), cleanDoc);
assert.strictEqual(report.admissionDecisions.length, 8, 'admission decision budget changed');
assert.strictEqual(report.truncated, true, 'truncation evidence missing');
assert.strictEqual(report.srwfStylesheetPresent, false, 'stylesheet absence observation missing');
assert.strictEqual(report.diagnosticVersion, '0.3.2');
assert.strictEqual(report.schemaVersion, 'v0.2');

const presentReport = api.buildReport([admitted], styleDoc);
assert.strictEqual(presentReport.srwfStylesheetPresent, true, 'stylesheet presence observation missing');

console.log('PASS: admission diagnostic v0.3.2 earliest-context/style-presence fixture');
