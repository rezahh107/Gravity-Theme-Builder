(function (root, factory) {
    'use strict';

    var api = factory();
    if (typeof module === 'object' && module.exports) {
        module.exports = api;
    }

    function installBrowserCollector() {
        if (!root || !root.document) {
            return;
        }
        var documentObject = root.document;
        var button = documentObject.getElementById('gtb-srwf-download-report');

        function collectNow() {
            var report = root.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03;
            if (report && typeof report === 'object' && Object.prototype.hasOwnProperty.call(report, 'srwfV1Qualification')) {
                delete report.srwfV1Qualification;
            }
            root.GTB_SRWF_V1_QUALIFICATION_V034 = null;

            var result = api.collect(documentObject, root);
            root.GTB_SRWF_V1_QUALIFICATION_V034 = result;
            if (report && typeof report === 'object') {
                report.srwfV1Qualification = result;
            }
            return result;
        }

        root.GTB_SRWF_COLLECT_V1_QUALIFICATION_V034 = collectNow;

        try {
            collectNow();
        } catch (error) {
            root.GTB_SRWF_V1_QUALIFICATION_V034 = null;
        }

        if (button && typeof button.addEventListener === 'function') {
            button.addEventListener('pointerdown', function () {
                try {
                    collectNow();
                } catch (error) {
                    root.GTB_SRWF_V1_QUALIFICATION_V034 = null;
                }
            });
        }
    }

    if (root && root.document) {
        if (root.document.readyState === 'loading') {
            root.document.addEventListener('DOMContentLoaded', installBrowserCollector, { once: true });
        } else {
            installBrowserCollector();
        }
    }
}(typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : this), function () {
    'use strict';

    var VERSION = '0.3.4';
    var TARGET_SELECTOR = '.gform-theme--framework.srwf-registration-theme_wrapper';
    var MAX_TARGETS = 4;
    var MAX_RHYTHM_FIELDS = 12;
    var MAX_ORDINARY_GAPS = 3;
    var MAX_SECTIONS = 8;
    var SECTION_ROLES = Object.freeze([
        'srwf-role-section-identity',
        'srwf-role-section-contact',
        'srwf-role-section-education',
        'srwf-role-section-school-documents',
        'srwf-role-section-student-photo'
    ]);

    function bounded(items, limit) {
        return Array.prototype.slice.call(items || [], 0, limit);
    }

    function rect(element) {
        if (!element || typeof element.getBoundingClientRect !== 'function') {
            return null;
        }
        var value = element.getBoundingClientRect();
        return {
            x: Number(value.x || 0),
            y: Number(value.y || 0),
            width: Number(value.width || 0),
            height: Number(value.height || 0)
        };
    }

    function style(element, view, pseudo) {
        if (!element || !view || typeof view.getComputedStyle !== 'function') {
            return null;
        }
        return view.getComputedStyle(element, pseudo || null);
    }

    function styleSnapshot(element, view, properties, pseudo) {
        var computed = style(element, view, pseudo);
        var output = {};
        if (!computed) {
            return output;
        }
        for (var i = 0; i < properties.length; i += 1) {
            var property = properties[i];
            output[property] = String(computed[property] || '');
        }
        return output;
    }

    function shellSnapshot(wrapper, view) {
        var computed = styleSnapshot(wrapper, view, [
            'paddingLeft', 'paddingRight', 'maxInlineSize', 'maxWidth',
            'backgroundColor', 'borderRadius', 'boxShadow', 'boxSizing'
        ]);
        return {
            rect: rect(wrapper),
            computed: computed,
            horizontalOverflow: Boolean(wrapper && Number(wrapper.scrollWidth || 0) > Number(wrapper.clientWidth || 0))
        };
    }

    function typographySnapshot(element, view) {
        if (!element) {
            return null;
        }
        return {
            rect: rect(element),
            computed: styleSnapshot(element, view, [
                'fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'color'
            ])
        };
    }

    function hasClass(element, className) {
        return Boolean(element && element.classList && typeof element.classList.contains === 'function' && element.classList.contains(className));
    }

    function explicitSectionRole(field) {
        if (!field) {
            return null;
        }
        for (var i = 0; i < SECTION_ROLES.length; i += 1) {
            if (hasClass(field, SECTION_ROLES[i])) {
                return SECTION_ROLES[i];
            }
        }
        return null;
    }

    function firstExplicitSection(wrapper) {
        if (!wrapper || typeof wrapper.querySelectorAll !== 'function') {
            return null;
        }
        var sections = bounded(wrapper.querySelectorAll('.gform_fields > .gfield.gfield--type-section'), MAX_SECTIONS);
        for (var i = 0; i < sections.length; i += 1) {
            var role = explicitSectionRole(sections[i]);
            if (role) {
                return { role: role, field: sections[i] };
            }
        }
        return null;
    }

    function ordinaryRhythm(wrapper) {
        if (!wrapper || typeof wrapper.querySelectorAll !== 'function') {
            return { sampleCount: 0, gapsPx: [] };
        }
        var fields = bounded(wrapper.querySelectorAll('.gform_fields > .gfield'), MAX_RHYTHM_FIELDS);
        var gaps = [];
        for (var i = 1; i < fields.length && gaps.length < MAX_ORDINARY_GAPS; i += 1) {
            var previousField = fields[i - 1];
            var currentField = fields[i];
            var adjacentSiblings = currentField && currentField.previousElementSibling === previousField
                && currentField.parentElement && previousField.parentElement === currentField.parentElement;
            if (!adjacentSiblings || hasClass(previousField, 'gfield--type-section') || hasClass(currentField, 'gfield--type-section')) {
                continue;
            }
            var before = rect(previousField);
            var after = rect(currentField);
            if (before && after) {
                gaps.push(Number(after.y - (before.y + before.height)));
            }
        }
        return { sampleCount: gaps.length, gapsPx: gaps };
    }

    function sectionRhythm(wrapper) {
        var section = firstExplicitSection(wrapper);
        if (!section || !section.field) {
            return { role: null, gapFromPreviousPx: null };
        }
        var previous = section.field.previousElementSibling;
        var sameParent = previous && section.field.parentElement && previous.parentElement === section.field.parentElement;
        if (!sameParent || !hasClass(previous, 'gfield')) {
            return { role: section.role, gapFromPreviousPx: null };
        }
        var currentRect = rect(section.field);
        var previousRect = rect(previous);
        return {
            role: section.role,
            gapFromPreviousPx: previousRect && currentRect ? Number(currentRect.y - (previousRect.y + previousRect.height)) : null
        };
    }

    function focusSnapshot(wrapper, documentObject, view) {
        var active = documentObject && documentObject.activeElement ? documentObject.activeElement : null;
        if (!active || !wrapper || typeof wrapper.contains !== 'function' || !wrapper.contains(active)) {
            return null;
        }
        var classes = bounded(active.classList || [], 24).map(String).filter(function (name) {
            return /^gform-|^gfield-|^ginput_|^ts-/.test(name);
        });
        var role = active && typeof active.getAttribute === 'function' ? active.getAttribute('role') : null;
        return {
            tag: active.tagName ? String(active.tagName).toLowerCase() : '',
            role: role ? String(role) : null,
            classes: classes,
            computed: styleSnapshot(active, view, [
                'outlineWidth', 'outlineStyle', 'outlineColor', 'outlineOffset', 'boxShadow'
            ])
        };
    }

    function sectionIconSnapshots(wrapper, view) {
        var output = [];
        if (!wrapper || typeof wrapper.querySelector !== 'function') {
            return output;
        }
        for (var i = 0; i < SECTION_ROLES.length; i += 1) {
            var role = SECTION_ROLES[i];
            var field = wrapper.querySelector('.gfield--type-section.' + role);
            var title = field && typeof field.querySelector === 'function' ? field.querySelector('.gsection_title') : null;
            if (!title) {
                continue;
            }
            output.push({
                role: role,
                tile: styleSnapshot(title, view, [
                    'width', 'height', 'borderRadius', 'backgroundColor', 'backgroundSize'
                ], '::before')
            });
        }
        return output;
    }

    function reportCardSnapshot(wrapper, view) {
        if (!wrapper || typeof wrapper.querySelector !== 'function') {
            return null;
        }
        var field = wrapper.querySelector('.gfield.srwf-role-report-card-upload');
        var root = field && typeof field.querySelector === 'function' ? field.querySelector('.gpfup') : null;
        var drop = field && typeof field.querySelector === 'function' ? field.querySelector('.gpfup__droparea') : null;
        if (!field || !root) {
            return null;
        }
        var classes = bounded(root.classList || [], 32).map(String);
        return {
            hasFiles: classes.indexOf('gpfup--has-files') !== -1,
            dropArea: drop ? {
                rect: rect(drop),
                computed: styleSnapshot(drop, view, [
                    'minHeight', 'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
                    'borderTopWidth', 'borderTopStyle', 'borderTopColor', 'borderRadius'
                ])
            } : null
        };
    }

    function gpasSnapshot(wrapper, view) {
        if (!wrapper || typeof wrapper.querySelector !== 'function') {
            return null;
        }
        var control = wrapper.querySelector('.ts-wrapper > .ts-control');
        if (!control) {
            return null;
        }
        return {
            consumer: 'runtime-proven-ts-wrapper-direct-control',
            rect: rect(control),
            computed: styleSnapshot(control, view, ['minHeight', 'outlineWidth', 'outlineStyle', 'outlineColor', 'outlineOffset'])
        };
    }

    function formIdFromWrapper(wrapper) {
        var id = wrapper && wrapper.id ? String(wrapper.id) : '';
        var match = /^gform_wrapper_(\d+)$/.exec(id);
        return match ? match[1] : null;
    }

    function formLayoutReadiness(wrapper, view) {
        var formId = formIdFromWrapper(wrapper);
        var map = view && view.GTB_SRWF_RUNTIME_FORM_LAYOUT_READINESS_BY_FORM_ID;
        if (!formId || !map || typeof map !== 'object') {
            return null;
        }
        return Object.prototype.hasOwnProperty.call(map, formId) ? map[formId] : null;
    }

    function collectTarget(wrapper, targetIndex, documentObject, view) {
        var section = firstExplicitSection(wrapper);
        var title = wrapper.querySelector('.gform_title');
        var helper = wrapper.querySelector('.gfield_description');
        var error = wrapper.querySelector('.gfield_validation_message');
        var sectionTitle = section && section.field ? section.field.querySelector('.gsection_title') : null;

        return {
            targetIndex: targetIndex,
            shell: shellSnapshot(wrapper, view),
            typography: {
                formTitle: typographySnapshot(title, view),
                sectionTitle: sectionTitle ? { role: section.role, snapshot: typographySnapshot(sectionTitle, view) } : null,
                helper: typographySnapshot(helper, view),
                fieldError: typographySnapshot(error, view)
            },
            rhythm: {
                ordinary: ordinaryRhythm(wrapper),
                section: sectionRhythm(wrapper)
            },
            focusedConsumer: focusSnapshot(wrapper, documentObject, view),
            sectionIcons: sectionIconSnapshots(wrapper, view),
            reportCard: reportCardSnapshot(wrapper, view),
            gpas: gpasSnapshot(wrapper, view),
            studentPhoto: {
                status: 'NOT_PROVEN',
                reason: 'no-explicit-student-photo-upload-consumer-admitted'
            },
            persianGravity: {
                status: 'OWNER_RUNTIME_REQUIRED',
                reason: 'no-authentic-persiangravity-presentation-consumer-admitted'
            },
            formLayoutReadiness: formLayoutReadiness(wrapper, view)
        };
    }

    function collect(documentObject, view) {
        var allWrappers = documentObject && typeof documentObject.querySelectorAll === 'function'
            ? documentObject.querySelectorAll(TARGET_SELECTOR)
            : [];
        var wrappers = bounded(allWrappers, MAX_TARGETS);
        return {
            diagnosticVersion: VERSION,
            targetFound: wrappers.length > 0,
            targetCount: wrappers.length,
            targetsTruncated: Number(allWrappers.length || 0) > MAX_TARGETS,
            viewportCssWidth: view ? Number(view.innerWidth || 0) : 0,
            targets: wrappers.map(function (wrapper, index) {
                return collectTarget(wrapper, index, documentObject, view);
            })
        };
    }

    return {
        VERSION: VERSION,
        TARGET_SELECTOR: TARGET_SELECTOR,
        MAX_TARGETS: MAX_TARGETS,
        collect: collect
    };
}));
