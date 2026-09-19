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
        id: '',
        classList: classList(classes),
        children: [],
        parentElement: null,
        clientWidth: box ? box.width : 0,
        scrollWidth: box ? box.width : 0,
        _box: box || { x: 0, y: 0, width: 0, height: 0 },
        _style: Object.assign({
            display: 'block', visibility: 'visible', opacity: '1', overflowX: 'visible',
            boxSizing: 'border-box', width: '', inlineSize: '', minWidth: '', minInlineSize: '',
            maxWidth: 'none', maxInlineSize: 'none', paddingLeft: '0px', paddingRight: '0px',
            marginLeft: '0px', marginRight: '0px'
        }, style || {}),
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

const wrapper = node('div', ['gform-theme--framework', 'srwf-registration-theme_wrapper'], { x: 80, y: 0, width: 840, height: 1200 }, {
    width: '840px', inlineSize: '840px', maxWidth: '840px', maxInlineSize: '840px', paddingLeft: '16px', paddingRight: '16px'
});
const hostMain = node('main', ['entry-content'], { x: 40, y: 0, width: 920, height: 1300 }, {
    width: '920px', maxWidth: '920px', maxInlineSize: '920px', paddingLeft: '20px', paddingRight: '20px', overflowX: 'auto'
});
const body = node('body', ['site-body'], { x: 0, y: 0, width: 1000, height: 1400 }, { width: '1000px' });
wrapper.parentElement = hostMain;
hostMain.parentElement = body;

const form = node('form', [], { x: 96, y: 20, width: 808, height: 1150 }, { width: '808px' });
const formBody = node('div', ['gform-body'], { x: 96, y: 80, width: 808, height: 980 }, { width: '808px' });
const fields = node('div', ['gform_fields'], { x: 96, y: 100, width: 808, height: 900 }, { width: '808px' });
const textControl = node('input', [], { x: 100, y: 189, width: 380, height: 52 }, { width: '380px', fontFamily: 'Vazirmatn', fontSize: '16px', fontWeight: '400', lineHeight: '24px' });
const radioGroup = node('div', ['gfield_radio'], { x: 100, y: 300, width: 808, height: 116 }, { width: '808px' });
const submit = node('button', ['gform_button'], { x: 100, y: 700, width: 800, height: 56 }, { width: '800px', fontSize: '16px', fontWeight: '700', lineHeight: '24px' });

const label = node('legend', ['gfield_label'], { x: 100, y: 100, width: 300, height: 22 }, { fontSize: '15px', fontWeight: '600', lineHeight: '22.5px' });
const helper = node('div', ['gfield_description'], { x: 100, y: 128, width: 300, height: 21 }, { fontSize: '14px', fontWeight: '400', lineHeight: '21px' });
const error = node('div', ['gfield_validation_message'], { x: 100, y: 160, width: 300, height: 21 }, { fontSize: '14px', fontWeight: '600', lineHeight: '21px' });
const fieldOne = node('div', ['gfield'], { x: 100, y: 80, width: 390, height: 120 });
fieldOne.querySelector = (selector) => {
    if (selector === '.gfield_label') return label;
    if (selector === '.gfield_description:not(.gform_fileupload_rules)') return helper;
    if (selector === '.gfield_validation_message') return error;
    if (selector.includes('input:not')) return textControl;
    return null;
};
const fieldSameRow = node('div', ['gfield'], { x: 510, y: 80, width: 390, height: 100 });
const fieldNextRow = node('div', ['gfield'], { x: 100, y: 224, width: 800, height: 100 });

function uploadField(rootClasses, reportRole) {
    const field = node('div', ['gfield', 'gfield--type-fileupload'].concat(reportRole ? ['srwf-role-report-card-upload'] : []), { x: 100, y: 440, width: 808, height: 140 });
    const root = node('div', rootClasses, { x: 100, y: 440, width: 808, height: 120 });
    const drop = node('div', ['gpfup__droparea'], { x: 100, y: 440, width: 808, height: 96 }, {
        width: '808px', minHeight: '96px', paddingTop: '16px', paddingRight: '16px', paddingBottom: '16px', paddingLeft: '16px',
        borderTopWidth: '1px', borderTopStyle: 'dashed', borderTopColor: 'rgb(134, 144, 161)', borderRadius: '12px',
        backgroundColor: 'rgb(250, 251, 252)', fontSize: '14px', fontWeight: '400', lineHeight: '21px', columnGap: '12px', rowGap: '12px'
    });
    const button = node('button', ['gpfup__select-files'], { x: 170, y: 465, width: 160, height: 24 }, { fontSize: '14px', fontWeight: '600', lineHeight: '21px' });
    const rules = node('span', ['gform_fileupload_rules'], { x: 100, y: 545, width: 400, height: 21 }, { fontSize: '14px', fontWeight: '400', lineHeight: '21px' });
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
const gpas = node('div', ['ts-control'], { x: 100, y: 600, width: 400, height: 52 }, { minHeight: '52px', fontSize: '16px', fontWeight: '400', lineHeight: '24px' });
const gpasParent = node('div', ['ts-wrapper'], { x: 100, y: 600, width: 400, height: 52 });
gpas.parentElement = gpasParent;

const visibleInside = node('input', [], { x: 100, y: 760, width: 300, height: 52 });
const hiddenOffscreen = node('input', [], { x: 2000, y: 760, width: 100, height: 52 }, { display: 'none' });
const overflowCandidates = [visibleInside, hiddenOffscreen];

wrapper.querySelector = (selector) => {
    if (selector === 'form') return form;
    if (selector === '.gform-body, .gform_body') return formBody;
    if (selector === '.gform_fields') return fields;
    if (selector.startsWith('.gfield--type-section.')) return null;
    if (selector === '.gfield.srwf-role-report-card-upload') return report.field;
    if (selector === '.gfield--type-fileupload .gpfup.gpfup--images-only') return photo.root;
    if (selector === '.ts-wrapper > .ts-control') return gpas;
    if (selector === '.gform-footer .gform_button, .gform_footer .gform_button') return submit;
    return null;
};
wrapper.querySelectorAll = (selector) => {
    if (selector === 'input, select, textarea, button, .ts-control, .gfield, .gpfup__droparea, .gchoice > label') return overflowCandidates;
    if (selector === '.gform_fields > .gfield') return [fieldOne, fieldSameRow, fieldNextRow];
    if (selector === '.gfield:not(.gfield--type-section) .gfield_label') return [label];
    if (selector === '.gform_fields > .gfield:not(.gfield--type-section)') return [fieldOne];
    if (selector.startsWith('input[type="text"]')) return [textControl];
    if (selector === '.gfield.gfield--type-radio .gfield_radio') return [radioGroup];
    if (selector === '.gpfup:not(.gpfup--has-files) .gpfup__droparea') return [report.drop];
    if (selector === '.gform-footer .gform_button, .gform_footer .gform_button') return [submit];
    return [];
};

const scrollingElement = node('html', [], { x: 0, y: 0, width: 1000, height: 1400 });
scrollingElement.clientWidth = 1000;
scrollingElement.scrollWidth = 1000;
const documentObject = {
    scrollingElement,
    documentElement: scrollingElement,
    body,
    querySelectorAll(selector) {
        assert.strictEqual(selector, api.TARGET_SELECTOR);
        return [wrapper];
    }
};

const view = {
    innerWidth: 1000,
    devicePixelRatio: 2,
    getComputedStyle(element, pseudo) {
        if (pseudo === '::before') {
            if (element === report.drop) return { width: '40px', height: '40px', backgroundSize: '24px 24px', backgroundImage: 'url("report-card-file.svg")', borderRadius: '10px' };
            if (element === photo.drop) return { width: '40px', height: '40px', backgroundSize: '24px 24px', backgroundImage: 'url("student-photo-upload.svg")', borderRadius: '10px' };
            return { width: '', height: '', backgroundSize: '', backgroundImage: '', borderRadius: '' };
        }
        return element && element._style ? element._style : { display: 'block', visibility: 'visible', opacity: '1', overflowX: 'visible' };
    }
};

const result = api.collect(documentObject, view);
assert.strictEqual(result.diagnosticVersion, '0.3.6');
assert.strictEqual(result.viewportCssWidth, 1000);
assert.strictEqual(result.devicePixelRatio, 2);
assert.strictEqual(result.targetCount, 1);

const target = result.targets[0];
assert.strictEqual(target.widthChain.wrapper.rect.width, 840);
assert.strictEqual(target.widthChain.wrapper.computed.paddingLeft, '16px');
assert.strictEqual(target.widthChain.ancestors[0].kind, 'immediate-parent');
assert.strictEqual(target.widthChain.ancestors[0].rect.width, 920);
assert.strictEqual(target.widthChain.ancestors[0].computed.maxWidth, '920px');
assert.ok(target.widthChain.ancestors.some((item) => item.tag === 'body' && item.rect.width === 1000));
assert.deepStrictEqual(target.widthChain.gravityFormsContainers.map((item) => item.rect.width), [808, 808, 808]);
assert.strictEqual(target.widthChain.representativeTextControl.rect.width, 380);
assert.strictEqual(target.widthChain.representativeRadioGroup.rect.width, 808);
assert.strictEqual(target.widthChain.representativeInitialUpload.rect.width, 808);
assert.strictEqual(target.widthChain.submit.rect.width, 800);

assert.strictEqual(target.shell.horizontalOverflow.detected, false);
assert.deepStrictEqual(target.rowRhythm.gapsPx, [24]);
assert.strictEqual(target.labelControlChain.finalTextToControlGapPx, 8);
assert.strictEqual(target.uploads.reportCard.dropArea.computed.minHeight, '96px');
assert.strictEqual(target.uploads.reportCard.dropArea.computed.rowGap, '12px');
assert.strictEqual(target.uploads.studentPhoto.status, 'HOST_CONFIG_ADMITTED');
assert.strictEqual(target.primaryAction.computed.lineHeight, '24px');

console.log('PASS: diagnostic v0.3.6 captures DPR, viewport, host/GF/wrapper width chain, representative consumer widths, and existing visual qualification evidence without reading content');
