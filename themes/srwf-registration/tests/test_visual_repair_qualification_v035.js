'use strict';

const assert = require('assert');
const api = require('../diagnostic/assets/visual-repair-qualification.js');

function classList(names) {
    const list = (names || []).slice();
    list.contains = (name) => list.includes(name);
    return list;
}

function node(tag, classes, box, style) {
    const value = {
        tagName: String(tag || 'div').toUpperCase(),
        classList: classList(classes),
        children: [],
        parentElement: null,
        clientWidth: box ? box.width : 0,
        scrollWidth: box ? box.width : 0,
        _box: box || { x: 0, y: 0, width: 0, height: 0 },
        _style: Object.assign({ display: 'block', visibility: 'visible', opacity: '1', overflowX: 'visible' }, style || {}),
        getBoundingClientRect() { return this._box; },
        querySelector() { return null; },
        querySelectorAll() { return []; },
        closest() { return null; }
    };
    Object.defineProperty(value, 'textContent', { get() { throw new Error('diagnostic read page text'); } });
    Object.defineProperty(value, 'innerText', { get() { throw new Error('diagnostic read page text'); } });
    Object.defineProperty(value, 'value', { get() { throw new Error('diagnostic read form value'); } });
    return value;
}

const wrapper = node('div', ['gform-theme--framework', 'srwf-registration-theme_wrapper'], { x: 80, y: 0, width: 840, height: 1200 });
wrapper.clientWidth = 840;
wrapper.scrollWidth = 840;

const scrollParent = node('main', [], { x: 40, y: 0, width: 920, height: 1300 }, { overflowX: 'auto' });
scrollParent.clientWidth = 920;
scrollParent.scrollWidth = 920;
wrapper.parentElement = scrollParent;

const label = node('legend', ['gfield_label'], { x: 100, y: 100, width: 300, height: 22 }, { fontFamily: 'Vazirmatn', fontSize: '15px', fontWeight: '600', lineHeight: '22.5px', color: 'rgb(23, 32, 51)' });
const helper = node('div', ['gfield_description'], { x: 100, y: 128, width: 300, height: 21 }, { fontFamily: 'Vazirmatn', fontSize: '14px', fontWeight: '400', lineHeight: '21px', color: 'rgb(102, 112, 133)' });
// The synthetic helper→error gap is observation-only; AUTHORITY_NOT_INVENTED.
const error = node('div', ['gfield_validation_message'], { x: 100, y: 160, width: 300, height: 21 }, { fontFamily: 'Vazirmatn', fontSize: '14px', fontWeight: '600', lineHeight: '21px', color: 'rgb(180, 35, 24)' });
const control = node('input', [], { x: 100, y: 189, width: 380, height: 52 }, { fontFamily: 'Vazirmatn', fontSize: '16px', fontWeight: '400', lineHeight: '24px', color: 'rgb(23, 32, 51)' });
const fieldOne = node('div', ['gfield'], { x: 100, y: 80, width: 390, height: 120 });
fieldOne.querySelector = (selector) => {
    if (selector === '.gfield_label') return label;
    if (selector === '.gfield_description:not(.gform_fileupload_rules)') return helper;
    if (selector === '.gfield_validation_message') return error;
    if (selector.includes('input:not')) return control;
    return null;
};

const fieldSameRow = node('div', ['gfield'], { x: 510, y: 80, width: 390, height: 100 });
const fieldNextRow = node('div', ['gfield'], { x: 100, y: 224, width: 800, height: 100 });

const hiddenOffscreen = node('input', [], { x: 2000, y: 300, width: 100, height: 52 }, { display: 'none' });
const visibleInside = node('input', [], { x: 100, y: 300, width: 300, height: 52 });
const overflowCandidates = [visibleInside, hiddenOffscreen];

function uploadField(rootClasses, report) {
    const field = node('div', ['gfield', 'gfield--type-fileupload'].concat(report ? ['srwf-role-report-card-upload'] : []), { x: 100, y: 400, width: 800, height: 140 });
    const root = node('div', rootClasses, { x: 100, y: 400, width: 800, height: 120 });
    const drop = node('div', ['gpfup__droparea'], { x: 100, y: 400, width: 800, height: 96 }, {
        minHeight: '96px', paddingTop: '16px', paddingRight: '16px', paddingBottom: '16px', paddingLeft: '16px',
        borderTopWidth: '1px', borderTopStyle: 'dashed', borderTopColor: 'rgb(134, 144, 161)', borderRadius: '12px',
        backgroundColor: 'rgb(250, 251, 252)', fontSize: '14px', fontWeight: '400', lineHeight: '21px', columnGap: '12px', rowGap: '4px'
    });
    const button = node('button', ['gpfup__select-files'], { x: 170, y: 425, width: 160, height: 24 }, { fontFamily: 'Vazirmatn', fontSize: '14px', fontWeight: '600', lineHeight: '21px' });
    const rules = node('span', ['gform_fileupload_rules'], { x: 100, y: 505, width: 400, height: 21 }, { fontFamily: 'Vazirmatn', fontSize: '14px', fontWeight: '400', lineHeight: '21px' });
    drop.children = [button];
    field.querySelector = (selector) => {
        if (selector === '.gpfup') return root;
        if (selector === '.gpfup__droparea') return drop;
        if (selector === '.gpfup__select-files') return button;
        if (selector === '.gform_fileupload_rules') return rules;
        return null;
    };
    root.closest = (selector) => selector === '.gfield--type-fileupload' ? field : null;
    return { field, root, drop };
}

const report = uploadField(['gpfup', 'gpfup--strict'], true);
const photo = uploadField(['gpfup', 'gpfup--strict', 'gpfup--images-only'], false);
const gpas = node('div', ['ts-control'], { x: 100, y: 600, width: 400, height: 52 }, { minHeight: '52px', fontFamily: 'Vazirmatn', fontSize: '16px', fontWeight: '400', lineHeight: '24px' });
const gpasParent = node('div', ['ts-wrapper'], { x: 100, y: 600, width: 400, height: 52 });
gpas.parentElement = gpasParent;
const submit = node('button', ['gform_button'], { x: 100, y: 700, width: 800, height: 56 }, { fontFamily: 'Vazirmatn', fontSize: '16px', fontWeight: '700', lineHeight: '24px' });

wrapper.querySelectorAll = (selector) => {
    if (selector === 'input, select, textarea, button, .ts-control, .gfield, .gpfup__droparea, .gchoice > label') return overflowCandidates;
    if (selector === '.gform_fields > .gfield') return [fieldOne, fieldSameRow, fieldNextRow];
    if (selector === '.gfield:not(.gfield--type-section) .gfield_label') return [label];
    if (selector === '.gform_fields > .gfield:not(.gfield--type-section)') return [fieldOne];
    return [];
};
wrapper.querySelector = (selector) => {
    if (selector.startsWith('.gfield--type-section.')) return null;
    if (selector === '.gfield.srwf-role-report-card-upload') return report.field;
    if (selector === '.gfield--type-fileupload .gpfup.gpfup--images-only') return photo.root;
    if (selector === '.ts-wrapper > .ts-control') return gpas;
    if (selector === '.gform-footer .gform_button, .gform_footer .gform_button') return submit;
    return null;
};

const scrollingElement = node('html', [], { x: 0, y: 0, width: 1000, height: 1400 });
scrollingElement.clientWidth = 1000;
scrollingElement.scrollWidth = 1000;
const documentObject = {
    scrollingElement,
    querySelectorAll(selector) {
        assert.strictEqual(selector, api.TARGET_SELECTOR);
        return [wrapper];
    }
};

const view = {
    getComputedStyle(element, pseudo) {
        if (pseudo === '::before') {
            if (element === report.drop) {
                return { width: '40px', height: '40px', backgroundSize: '24px 24px', backgroundImage: 'url("report-card-file.svg")', borderRadius: '10px' };
            }
            if (element === photo.drop) {
                return { width: '40px', height: '40px', backgroundSize: '24px 24px', backgroundImage: 'url("student-photo-upload.svg")', borderRadius: '10px' };
            }
            return { width: '', height: '', backgroundSize: '', backgroundImage: '', borderRadius: '' };
        }
        return element && element._style ? element._style : { display: 'block', visibility: 'visible', opacity: '1', overflowX: 'visible' };
    }
};

let result = api.collect(documentObject, view);
assert.strictEqual(result.diagnosticVersion, '0.3.5');
assert.strictEqual(result.targetCount, 1);
let target = result.targets[0];

assert.strictEqual(target.shell.horizontalOverflow.detected, false, 'hidden/offscreen content must not create a false overflow failure');
assert.strictEqual(target.shell.horizontalOverflow.sampledVisibleConsumers, 1);
assert.strictEqual(target.shell.horizontalOverflow.overflowingVisibleConsumers, 0);
assert.strictEqual(target.shell.horizontalOverflow.scrollingSurface.kind, 'scroll-ancestor');
assert.strictEqual(target.shell.horizontalOverflow.scrollingSurface.horizontalScrollOverflow, false);

assert.deepStrictEqual(target.rowRhythm.gapsPx, [24], 'same-row fields must not create negative field rhythm');
assert.deepStrictEqual(
    target.labelControlChain.gapChain.map((item) => [item.kind, item.gapToNextPx, item.nextKind]),
    [['label', 6, 'helper'], ['helper', 11, 'error'], ['error', 8, 'control'], ['control', null, null]],
    'diagnostic must preserve the observed visible chain without inventing a helper-to-error Owner constant'
);
assert.strictEqual(target.labelControlChain.finalTextToControlGapPx, 8);

assert.strictEqual(target.uploads.reportCard.dropArea.computed.minHeight, '96px');
assert.strictEqual(target.uploads.reportCard.dropArea.computed.borderTopWidth, '1px');
assert.strictEqual(target.uploads.reportCard.dropArea.pseudoBefore.width, '40px');
assert.strictEqual(target.uploads.reportCard.dropArea.pseudoBefore.height, '40px');
assert.strictEqual(target.uploads.reportCard.dropArea.pseudoBefore.backgroundSize, '24px 24px');
assert.ok(target.uploads.reportCard.dropArea.pseudoBefore.backgroundImage.includes('report-card-file.svg'));
assert.strictEqual(target.uploads.studentPhoto.status, 'HOST_CONFIG_ADMITTED');
assert.strictEqual(target.uploads.studentPhoto.admission, 'gpfup--images-only');
assert.ok(target.uploads.studentPhoto.snapshot.rootClasses.includes('gpfup--images-only'));
assert.strictEqual(target.uploads.studentPhoto.snapshot.dropArea.pseudoBefore.width, '40px');
assert.strictEqual(target.uploads.studentPhoto.snapshot.dropArea.pseudoBefore.height, '40px');
assert.strictEqual(target.uploads.studentPhoto.snapshot.dropArea.pseudoBefore.backgroundSize, '24px 24px');
assert.ok(target.uploads.studentPhoto.snapshot.dropArea.pseudoBefore.backgroundImage.includes('student-photo-upload.svg'));
assert.strictEqual(target.gpas.dynamicState, 'NOT_PROVEN_CLOSED');
assert.strictEqual(target.primaryAction.computed.lineHeight, '24px');
assert.strictEqual(target.runtimeOnlyStates.validation, 'OBSERVE_IF_AUTHENTIC_INVALID_STATE');

const visibleOverflow = node('input', [], { x: 900, y: 800, width: 80, height: 52 });
overflowCandidates.push(visibleOverflow);
result = api.collect(documentObject, view);
target = result.targets[0];
assert.strictEqual(target.shell.horizontalOverflow.visibleConsumerOverflowDetected, true, 'genuine visible theme-boundary overflow was incorrectly filtered');
assert.strictEqual(target.shell.horizontalOverflow.overflowingVisibleConsumers, 1);

scrollParent.scrollWidth = 1000;
result = api.collect(documentObject, view);
target = result.targets[0];
assert.strictEqual(target.shell.horizontalOverflow.scrollingSurface.horizontalScrollOverflow, true, 'actual scroll surface overflow was not recorded');
assert.strictEqual(target.shell.horizontalOverflow.detected, true);

console.log('PASS: visual repair qualification measures shared GPFUP icon geometry, row-normalized rhythm, observed gap chain, visible overflow, actual scroll surface, and unresolved dynamic states');
