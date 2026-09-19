'use strict';

const assert = require('assert');
const api = require('../diagnostic/assets/visual-repair-qualification.js');

function classList(names) {
    const list = names.slice();
    list.contains = (name) => list.includes(name);
    return list;
}

function node(tag, names, box) {
    return {
        tagName: String(tag || 'div').toUpperCase(),
        classList: classList(names || []),
        children: [],
        parentElement: null,
        getBoundingClientRect: () => box || ({ x: 0, y: 0, width: 0, height: 0 }),
        querySelector: () => null,
        querySelectorAll: () => []
    };
}

const wrapper = node('div', ['gform-theme--framework', 'srwf-registration-theme_wrapper'], { x: 0, y: 0, width: 320, height: 900 });
const fieldA = node('div', ['gfield'], { x: 16, y: 100, width: 136, height: 52 });
const fieldB = node('div', ['gfield'], { x: 168, y: 100, width: 136, height: 52 });
const fieldC = node('div', ['gfield'], { x: 16, y: 176, width: 288, height: 52 });
const visibleConsumer = node('input', [], { x: 16, y: 240, width: 288, height: 52 });
const hiddenOffscreen = node('select', [], { x: 500, y: 240, width: 200, height: 52 });
hiddenOffscreen._hidden = true;

const reportField = node('div', ['gfield', 'gfield--type-fileupload', 'srwf-role-report-card-upload'], { x: 16, y: 320, width: 288, height: 120 });
const reportRoot = node('div', ['gpfup'], { x: 16, y: 320, width: 288, height: 96 });
const reportDrop = node('div', ['gpfup__droparea'], { x: 16, y: 320, width: 288, height: 96 });
const reportButton = node('button', ['gpfup__select-files'], { x: 72, y: 340, width: 90, height: 24 });
const reportRules = node('div', ['gform_fileupload_rules'], { x: 72, y: 370, width: 180, height: 21 });
reportDrop.children = [reportButton, reportRules];
reportField.querySelector = (selector) => {
    if (selector === '.gpfup') return reportRoot;
    if (selector === '.gpfup__droparea') return reportDrop;
    if (selector === '.gpfup__select-files') return reportButton;
    if (selector === '.gform_fileupload_rules') return reportRules;
    return null;
};

const photoField = node('div', ['gfield', 'gfield--type-fileupload'], { x: 16, y: 470, width: 288, height: 120 });
const photoRoot = node('div', ['gpfup', 'gpfup--images-only'], { x: 16, y: 470, width: 288, height: 96 });
const photoDrop = node('div', ['gpfup__droparea'], { x: 16, y: 470, width: 288, height: 96 });
const photoButton = node('button', ['gpfup__select-files'], { x: 72, y: 490, width: 90, height: 24 });
const photoRules = node('div', ['gform_fileupload_rules'], { x: 72, y: 520, width: 180, height: 21 });
photoDrop.children = [photoButton, photoRules];
photoRoot.closest = (selector) => selector === '.gfield--type-fileupload' ? photoField : null;
photoField.querySelector = (selector) => {
    if (selector === '.gpfup') return photoRoot;
    if (selector === '.gpfup__droparea') return photoDrop;
    if (selector === '.gpfup__select-files') return photoButton;
    if (selector === '.gform_fileupload_rules') return photoRules;
    return null;
};

const rowFields = [fieldA, fieldB, fieldC];
const overflowCandidates = [visibleConsumer, hiddenOffscreen];
wrapper.querySelectorAll = (selector) => {
    if (selector === '.gform_fields > .gfield') return rowFields;
    if (selector === '.gform_fields > .gfield:not(.gfield--type-section)') return rowFields;
    if (selector === '.gfield:not(.gfield--type-section) .gfield_label') return [];
    if (selector.startsWith('input, select, textarea')) return overflowCandidates;
    return [];
};
wrapper.querySelector = (selector) => {
    if (selector === '.gfield.srwf-role-report-card-upload') return reportField;
    if (selector === '.gfield--type-fileupload .gpfup.gpfup--images-only') return photoRoot;
    return null;
};

const documentObject = {
    querySelectorAll(selector) {
        assert.strictEqual(selector, api.TARGET_SELECTOR);
        return [wrapper];
    }
};

const view = {
    getComputedStyle(element, pseudo) {
        if (pseudo === '::before') {
            return new Proxy({
                width: '24px', height: '24px', backgroundSize: '24px 24px',
                backgroundImage: 'url("report-card-file.svg")', borderRadius: '10px'
            }, { get(target, key) { return key in target ? target[key] : ''; } });
        }
        const hidden = Boolean(element && element._hidden);
        return new Proxy({
            display: hidden ? 'none' : 'block', visibility: 'visible', opacity: '1',
            minHeight: '96px', paddingTop: '16px', paddingRight: '16px', paddingBottom: '16px', paddingLeft: '16px',
            borderTopWidth: '1px', borderTopStyle: 'dashed', borderTopColor: 'rgb(134, 144, 161)', borderRadius: '12px',
            backgroundColor: 'rgb(250, 251, 252)', fontFamily: 'Vazirmatn', fontSize: '14px', fontWeight: '400', lineHeight: '21px',
            columnGap: '12px', rowGap: '4px'
        }, { get(target, key) { return key in target ? target[key] : ''; } });
    }
};

let report = api.collect(documentObject, view);
assert.strictEqual(report.diagnosticVersion, '0.3.5');
assert.strictEqual(report.targetCount, 1);
assert.strictEqual(report.targets[0].rowRhythm.rowCount, 2, 'same-row paired fields must collapse to one visual row');
assert.deepStrictEqual(report.targets[0].rowRhythm.gapsPx, [24], 'row-normalized rhythm must measure row-to-row gap, not paired DOM siblings');
assert.strictEqual(report.targets[0].shell.horizontalOverflow.detected, false, 'hidden offscreen consumer created a false overflow failure');
assert.strictEqual(report.targets[0].shell.horizontalOverflow.sampledVisibleConsumers, 1);
assert.strictEqual(report.targets[0].uploads.reportCard.dropArea.computed.borderTopWidth, '1px');
assert.strictEqual(report.targets[0].uploads.reportCard.dropArea.pseudoBefore.width, '24px');
assert.strictEqual(report.targets[0].uploads.studentPhoto.status, 'HOST_CONFIG_ADMITTED');
assert.strictEqual(report.targets[0].uploads.studentPhoto.admission, 'gpfup--images-only');
assert.strictEqual(report.targets[0].uploads.studentPhoto.snapshot.hasFiles, false);
assert.strictEqual(report.targets[0].runtimeOnlyStates.validation, 'OBSERVE_IF_AUTHENTIC_INVALID_STATE');
assert.strictEqual(report.targets[0].runtimeOnlyStates.postUpload, 'OBSERVE_IF_AUTHENTIC_HAS_FILES');

const visibleOverflow = node('input', [], { x: 300, y: 250, width: 40, height: 52 });
overflowCandidates.push(visibleOverflow);
report = api.collect(documentObject, view);
assert.strictEqual(report.targets[0].shell.horizontalOverflow.detected, true, 'genuine visible overflow was incorrectly filtered');
assert.strictEqual(report.targets[0].shell.horizontalOverflow.overflowingVisibleConsumers, 1);

console.log('PASS: visual repair qualification row-normalizes rhythm, filters hidden overflow, preserves genuine overflow, and admits only authentic initial upload consumers');
