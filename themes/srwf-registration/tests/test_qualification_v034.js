'use strict';
const assert = require('assert');
const api = require('../diagnostic/assets/srwf-v1-qualification.js');

function classes(names) {
    const list = names.slice();
    list.contains = (name) => list.includes(name);
    return list;
}

function element(tag, classNames, box, computed) {
    const node = {
        tagName: tag.toUpperCase(),
        classList: classes(classNames || []),
        children: [],
        previousElementSibling: null,
        scrollWidth: box ? box.width : 0,
        clientWidth: box ? box.width : 0,
        getBoundingClientRect: () => box || ({ x: 0, y: 0, width: 0, height: 0 }),
        getAttribute: () => null,
        querySelector: () => null,
        querySelectorAll: () => [],
        _computed: computed || {}
    };
    Object.defineProperty(node, 'value', { get() { throw new Error('private value accessed'); } });
    Object.defineProperty(node, 'textContent', { get() { throw new Error('text content accessed'); } });
    Object.defineProperty(node, 'innerText', { get() { throw new Error('inner text accessed'); } });
    return node;
}

const title = element('h2', ['gform_title'], { x: 32, y: 24, width: 300, height: 39 }, {
    fontFamily: 'Vazirmatn', fontSize: '26px', fontWeight: '700', lineHeight: '39px', color: 'rgb(23, 32, 51)'
});
const helper = element('div', ['gfield_description'], { x: 32, y: 120, width: 400, height: 21 }, {
    fontFamily: 'Vazirmatn', fontSize: '14px', fontWeight: '400', lineHeight: '21px', color: 'rgb(102, 112, 133)'
});
const error = element('div', ['gfield_validation_message'], { x: 32, y: 150, width: 400, height: 21 }, {
    fontFamily: 'Vazirmatn', fontSize: '14px', fontWeight: '600', lineHeight: '21px', color: 'rgb(180, 35, 24)'
});
const ordinaryA = element('div', ['gfield'], { x: 32, y: 200, width: 400, height: 52 }, {});
const ordinaryB = element('div', ['gfield'], { x: 32, y: 276, width: 400, height: 52 }, {});
const sectionTitle = element('h3', ['gsection_title'], { x: 32, y: 368, width: 400, height: 40 }, {
    fontFamily: 'Vazirmatn', fontSize: '18px', fontWeight: '700', lineHeight: '27px', color: 'rgb(23, 32, 51)',
    width: '40px', height: '40px', borderRadius: '10px', backgroundColor: 'rgb(237, 241, 252)', backgroundSize: '20px 20px'
});
const section = element('div', ['gfield', 'gfield--type-section', 'srwf-role-section-identity'], { x: 32, y: 360, width: 400, height: 64 }, {});
section.previousElementSibling = ordinaryB;
section.querySelector = (selector) => selector === '.gsection_title' ? sectionTitle : null;

const gpfup = element('div', ['gpfup', 'gpfup--strict'], { x: 32, y: 460, width: 400, height: 96 }, {});
const drop = element('div', ['gpfup__droparea'], { x: 32, y: 460, width: 400, height: 96 }, {
    minHeight: '96px', paddingTop: '16px', paddingRight: '16px', paddingBottom: '16px', paddingLeft: '16px',
    borderTopWidth: '1.5px', borderTopStyle: 'dashed', borderTopColor: 'rgb(134, 144, 161)', borderRadius: '12px'
});
const report = element('div', ['gfield', 'srwf-role-report-card-upload'], { x: 32, y: 450, width: 400, height: 120 }, {});
report.querySelector = (selector) => selector === '.gpfup' ? gpfup : (selector === '.gpfup__droparea' ? drop : null);

const focus = element('input', ['gform-text-input-reset'], { x: 32, y: 600, width: 400, height: 52 }, {
    outlineWidth: '2px', outlineStyle: 'solid', outlineColor: 'rgb(29, 78, 216)', outlineOffset: '2px', boxShadow: 'none'
});
const tsControl = element('div', ['ts-control'], { x: 32, y: 680, width: 400, height: 52 }, {
    minHeight: '52px', outlineWidth: '0px', outlineStyle: 'none', outlineColor: 'rgb(0, 0, 0)', outlineOffset: '0px'
});

const wrapper = element('div', ['gform-theme--framework', 'srwf-registration-theme_wrapper'], { x: 20, y: 0, width: 904, height: 900 }, {
    paddingLeft: '32px', paddingRight: '32px', maxInlineSize: '904px', maxWidth: '904px',
    backgroundColor: 'rgb(255, 255, 255)', borderRadius: '16px', boxShadow: 'none', boxSizing: 'border-box'
});
wrapper.contains = (node) => node === focus;
wrapper.querySelector = (selector) => {
    if (selector === '.gform_title') return title;
    if (selector === '.gfield_description') return helper;
    if (selector === '.gfield_validation_message') return error;
    if (selector === '.gfield--type-section.srwf-role-section-identity') return section;
    if (selector === '.gfield.srwf-role-report-card-upload') return report;
    if (selector === '.ts-wrapper > .ts-control') return tsControl;
    return null;
};
wrapper.querySelectorAll = (selector) => selector === '.gform_fields > .gfield:not(.gfield--type-section)' ? [ordinaryA, ordinaryB] : [];

const documentObject = {
    activeElement: focus,
    querySelector(selector) {
        assert.strictEqual(selector, api.TARGET_SELECTOR, 'collector escaped SRWF target scope');
        return wrapper;
    }
};
const view = {
    innerWidth: 1024,
    GTB_SRWF_RUNTIME_FORM_LAYOUT_READINESS: {
        state: 'READY',
        conflictingFieldOverrideCount: 0
    },
    getComputedStyle(node, pseudo) {
        if (pseudo === '::before' && node === sectionTitle) {
            return sectionTitle._computed;
        }
        return node && node._computed ? node._computed : {};
    }
};

const reportData = api.collect(documentObject, view);
assert.strictEqual(reportData.diagnosticVersion, '0.3.4');
assert.strictEqual(reportData.targetFound, true);
assert.strictEqual(reportData.viewportCssWidth, 1024);
assert.strictEqual(reportData.shell.rect.width, 904);
assert.strictEqual(reportData.shell.computed.paddingLeft, '32px');
assert.strictEqual(reportData.shell.computed.borderRadius, '16px');
assert.strictEqual(reportData.shell.computed.boxShadow, 'none');
assert.strictEqual(reportData.shell.horizontalOverflow, false);
assert.strictEqual(reportData.typography.formTitle.computed.fontSize, '26px');
assert.strictEqual(reportData.typography.helper.computed.fontWeight, '400');
assert.strictEqual(reportData.typography.fieldError.computed.fontWeight, '600');
assert.deepStrictEqual(reportData.rhythm.ordinary.gapsPx, [24]);
assert.strictEqual(reportData.rhythm.section.gapFromPreviousPx, 32);
assert.strictEqual(reportData.focusedConsumer.computed.outlineWidth, '2px');
assert.strictEqual(reportData.focusedConsumer.computed.outlineOffset, '2px');
assert.strictEqual(reportData.sectionIcons[0].role, 'srwf-role-section-identity');
assert.strictEqual(reportData.sectionIcons[0].tile.width, '40px');
assert.strictEqual(reportData.reportCard.hasFiles, false);
assert.strictEqual(reportData.reportCard.dropArea.computed.minHeight, '96px');
assert.strictEqual(reportData.gpas.consumer, 'runtime-proven-ts-wrapper-direct-control');
assert.strictEqual(reportData.studentPhoto.status, 'NOT_PROVEN');
assert.strictEqual(reportData.persianGravity.status, 'OWNER_RUNTIME_REQUIRED');
assert.strictEqual(reportData.formLayoutReadiness.state, 'READY');

const missing = api.collect({ querySelector: () => null }, { innerWidth: 320 });
assert.strictEqual(missing.targetFound, false);
assert.strictEqual(missing.viewportCssWidth, 320);

console.log('PASS: SRWF v1 qualification diagnostic is bounded and privacy-safe');
