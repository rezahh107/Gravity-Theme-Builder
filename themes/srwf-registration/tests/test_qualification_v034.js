'use strict';
const assert = require('assert');
const api = require('../diagnostic/assets/srwf-v1-qualification.js');

function classes(names) {
    const list = names.slice();
    list.contains = (name) => list.includes(name);
    return list;
}

function element(tag, classNames, box, computed, id) {
    const node = {
        id: id || '',
        tagName: tag.toUpperCase(),
        classList: classes(classNames || []),
        previousElementSibling: null,
        parentElement: null,
        scrollWidth: box ? box.width : 0,
        clientWidth: box ? box.width : 0,
        getBoundingClientRect: () => box || ({ x: 0, y: 0, width: 0, height: 0 }),
        getAttribute: () => null,
        querySelector: () => null,
        querySelectorAll: () => [],
        _computed: computed || {}
    };
    Object.defineProperty(node, 'value', { get() { throw new Error('private value accessed'); } });
    Object.defineProperty(node, 'textContent', { get() { throw new Error('arbitrary text accessed'); } });
    Object.defineProperty(node, 'innerText', { get() { throw new Error('arbitrary text accessed'); } });
    Object.defineProperty(node, 'files', { get() { throw new Error('filenames accessed'); } });
    Object.defineProperty(node, 'options', { get() { throw new Error('option contents accessed'); } });
    Object.defineProperty(node, 'href', { get() { throw new Error('urls accessed'); } });
    return node;
}

function linkSiblings(fields) {
    const parent = {};
    fields.forEach((field, index) => {
        field.parentElement = parent;
        field.previousElementSibling = index ? fields[index - 1] : null;
    });
}

function makeSection(role, y) {
    const title = element('h3', ['gsection_title'], { x: 32, y: y + 8, width: 400, height: 40 }, {
        fontFamily: 'Vazirmatn', fontSize: '18px', fontWeight: '700', lineHeight: '27px', color: 'rgb(23, 32, 51)',
        width: '40px', height: '40px', borderRadius: '10px', backgroundColor: 'rgb(237, 241, 252)', backgroundSize: '20px 20px'
    });
    const section = element('div', ['gfield', 'gfield--type-section', role], { x: 32, y, width: 400, height: 64 }, {});
    section.querySelector = (selector) => selector === '.gsection_title' ? title : null;
    return { section, title };
}

function makeWrapper(id, layoutKind) {
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
    const education = makeSection('srwf-role-section-education', 360);
    const ordinaryC = element('div', ['gfield'], { x: 32, y: 448, width: 400, height: 52 }, {});
    const identity = makeSection('srwf-role-section-identity', 532);
    const fields = layoutKind === 'section-between'
        ? [ordinaryA, education.section, ordinaryB, identity.section]
        : [ordinaryA, ordinaryB, education.section, ordinaryC, identity.section];
    linkSiblings(fields);

    const gpfup = element('div', ['gpfup', 'gpfup--strict'], { x: 32, y: 596, width: 400, height: 96 }, {});
    const drop = element('div', ['gpfup__droparea'], { x: 32, y: 596, width: 400, height: 96 }, {
        minHeight: '96px', paddingTop: '16px', paddingRight: '16px', paddingBottom: '16px', paddingLeft: '16px',
        borderTopWidth: '1.5px', borderTopStyle: 'dashed', borderTopColor: 'rgb(134, 144, 161)', borderRadius: '12px'
    });
    const report = element('div', ['gfield', 'srwf-role-report-card-upload'], { x: 32, y: 586, width: 400, height: 120 }, {});
    report.querySelector = (selector) => selector === '.gpfup' ? gpfup : (selector === '.gpfup__droparea' ? drop : null);
    const tsControl = element('div', ['ts-control'], { x: 32, y: 716, width: 400, height: 52 }, {
        minHeight: '52px', outlineWidth: '0px', outlineStyle: 'none', outlineColor: 'rgb(0, 0, 0)', outlineOffset: '0px'
    });
    const focus = element('input', ['gform-text-input-reset'], { x: 32, y: 780, width: 400, height: 52 }, {
        outlineWidth: '2px', outlineStyle: 'solid', outlineColor: 'rgb(29, 78, 216)', outlineOffset: '2px', boxShadow: 'none'
    });
    const wrapper = element('div', ['gform-theme--framework', 'srwf-registration-theme_wrapper'], { x: 20, y: 0, width: 904, height: 900 }, {
        paddingLeft: '32px', paddingRight: '32px', maxInlineSize: '904px', maxWidth: '904px',
        backgroundColor: 'rgb(255, 255, 255)', borderRadius: '16px', boxShadow: 'none', boxSizing: 'border-box'
    }, id);
    wrapper.contains = (node) => node === focus;
    wrapper.querySelector = (selector) => {
        if (selector === '.gform_title') return title;
        if (selector === '.gfield_description') return helper;
        if (selector === '.gfield_validation_message') return error;
        if (selector === '.gfield--type-section.srwf-role-section-education') return education.section;
        if (selector === '.gfield--type-section.srwf-role-section-identity') return identity.section;
        if (selector === '.gfield.srwf-role-report-card-upload') return report;
        if (selector === '.ts-wrapper > .ts-control') return tsControl;
        return null;
    };
    wrapper.querySelectorAll = (selector) => {
        if (selector === '.gform_fields > .gfield') return fields;
        if (selector === '.gform_fields > .gfield.gfield--type-section') return fields.filter((field) => field.classList.contains('gfield--type-section'));
        return [];
    };
    return { wrapper, focus, fields };
}

const first = makeWrapper('gform_wrapper_11', 'normal');
const second = makeWrapper('gform_wrapper_12', 'section-between');
const documentObject = {
    activeElement: first.focus,
    querySelectorAll(selector) {
        assert.strictEqual(selector, api.TARGET_SELECTOR, 'collector escaped SRWF target scope');
        return [first.wrapper, second.wrapper];
    }
};
const view = {
    innerWidth: 1024,
    GTB_SRWF_RUNTIME_FORM_LAYOUT_READINESS_BY_FORM_ID: {
        '11': { state: 'READY', conflictingFieldOverrideCount: 0 },
        '12': { state: 'NEEDS ATTENTION', conflictingFieldOverrideCount: 2 }
    },
    getComputedStyle(node, pseudo) {
        if (pseudo === '::before') return node && node._computed ? node._computed : {};
        return node && node._computed ? node._computed : {};
    }
};

const report = api.collect(documentObject, view);
assert.strictEqual(report.diagnosticVersion, '0.3.4');
assert.strictEqual(report.targetFound, true);
assert.strictEqual(report.targetCount, 2);
assert.strictEqual(report.targets.length, 2);
assert.strictEqual(report.targets[0].targetIndex, 0);
assert.strictEqual(report.targets[1].targetIndex, 1);
assert.strictEqual(report.targets[0].formLayoutReadiness.state, 'READY');
assert.strictEqual(report.targets[1].formLayoutReadiness.state, 'NEEDS ATTENTION');
assert.strictEqual(report.targets[0].formLayoutReadiness.conflictingFieldOverrideCount, 0);
assert.strictEqual(report.targets[1].formLayoutReadiness.conflictingFieldOverrideCount, 2);

assert.strictEqual(report.targets[0].rhythm.section.role, 'srwf-role-section-education');
assert.strictEqual(report.targets[0].rhythm.section.gapFromPreviousPx, 32);
assert.deepStrictEqual(report.targets[0].rhythm.ordinary.gapsPx, [24]);
assert.deepStrictEqual(report.targets[1].rhythm.ordinary.gapsPx, []);
assert.strictEqual(report.targets[1].rhythm.ordinary.sampleCount, 0);
assert.strictEqual(report.targets[1].rhythm.section.role, 'srwf-role-section-education');
assert.strictEqual(report.targets[1].rhythm.section.gapFromPreviousPx, 108);

const crossContainer = makeWrapper('gform_wrapper_13', 'normal');
crossContainer.fields[1].parentElement = {};
crossContainer.fields[1].previousElementSibling = null;
const crossContainerReport = api.collect({ activeElement: null, querySelectorAll: () => [crossContainer.wrapper] }, {
    innerWidth: 1024,
    GTB_SRWF_RUNTIME_FORM_LAYOUT_READINESS_BY_FORM_ID: { '13': { state: 'READY', conflictingFieldOverrideCount: 0 } },
    getComputedStyle: view.getComputedStyle
});
assert.deepStrictEqual(crossContainerReport.targets[0].rhythm.ordinary.gapsPx, []);

assert.strictEqual(report.targets[0].focusedConsumer.computed.outlineWidth, '2px');
assert.strictEqual(report.targets[0].sectionIcons[0].role, 'srwf-role-section-identity');
assert.strictEqual(report.targets[0].sectionIcons[0].tile.width, '40px');
assert.strictEqual(report.targets[0].reportCard.hasFiles, false);
assert.strictEqual(report.targets[0].reportCard.dropArea.computed.minHeight, '96px');
assert.strictEqual(report.targets[0].gpas.consumer, 'runtime-proven-ts-wrapper-direct-control');
assert.strictEqual(report.targets[0].studentPhoto.status, 'NOT_PROVEN');
assert.strictEqual(report.targets[0].persianGravity.status, 'OWNER_RUNTIME_REQUIRED');

const single = api.collect({ activeElement: first.focus, querySelectorAll: () => [first.wrapper] }, view);
assert.strictEqual(single.targetCount, 1);
assert.strictEqual(single.targets[0].formLayoutReadiness.state, 'READY');
assert.strictEqual(single.targets[0].shell.rect.width, 904);

const missing = api.collect({ querySelectorAll: () => [] }, { innerWidth: 320 });
assert.strictEqual(missing.targetFound, false);
assert.strictEqual(missing.targetCount, 0);
assert.deepStrictEqual(missing.targets, []);
assert.strictEqual(missing.viewportCssWidth, 320);

const many = api.collect({ querySelectorAll: () => [first.wrapper, second.wrapper, first.wrapper, second.wrapper, first.wrapper] }, view);
assert.strictEqual(api.MAX_TARGETS, 4);
assert.strictEqual(many.targetCount, 4);
assert.strictEqual(many.targetsTruncated, true);

const serialized = JSON.stringify(report);
for (const forbidden of ['private value', 'arbitrary text', 'filename', 'https://upload.example', 'option-secret']) {
    assert.strictEqual(serialized.includes(forbidden), false, 'privacy leak: ' + forbidden);
}

console.log('PASS: SRWF v0.3.4 qualification evidence is per-target, adjacency-bound, bounded, and privacy-safe');
