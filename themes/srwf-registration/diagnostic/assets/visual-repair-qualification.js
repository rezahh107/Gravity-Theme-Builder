(function (root, factory) {
    'use strict';

    var api = factory();
    if (typeof module === 'object' && module.exports) {
        module.exports = api;
    }

    function install() {
        if (!root || !root.document) {
            return;
        }
        var button = root.document.getElementById('gtb-srwf-download-report');

        function collectNow() {
            var value = api.collect(root.document, root);
            root.GTB_SRWF_VISUAL_REPAIR_QUALIFICATION_V036 = value;
            root.GTB_SRWF_VISUAL_REPAIR_QUALIFICATION_V035 = value;
            var report = root.GTB_SRWF_RUNTIME_DIAGNOSTIC_V03;
            if (report && typeof report === 'object') {
                report.visualRepairQualification = value;
            }
            return value;
        }

        root.GTB_SRWF_COLLECT_VISUAL_REPAIR_QUALIFICATION_V036 = collectNow;
        root.GTB_SRWF_COLLECT_VISUAL_REPAIR_QUALIFICATION_V035 = collectNow;
        collectNow();

        if (button && typeof button.addEventListener === 'function') {
            button.addEventListener('pointerdown', collectNow);
            button.addEventListener('click', collectNow, true);
        }
    }

    if (root && root.document) {
        if (root.document.readyState === 'loading') {
            root.document.addEventListener('DOMContentLoaded', install, { once: true });
        } else {
            install();
        }
    }
}(typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : this), function () {
    'use strict';

    var VERSION = '0.3.6';
    var TARGET_SELECTOR = '.gform-theme--framework.srwf-registration-theme_wrapper';
    var MAX_TARGETS = 4;
    var MAX_FIELDS = 48;
    var MAX_SCROLL_ANCESTORS = 12;
    var MAX_WIDTH_ANCESTORS = 12;
    var MAX_CLASSES = 32;
    var SECTION_ROLES = [
        'srwf-role-section-identity',
        'srwf-role-section-contact',
        'srwf-role-section-education',
        'srwf-role-section-school-documents',
        'srwf-role-section-student-photo'
    ];

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

    function computed(element, view, pseudo) {
        if (!element || !view || typeof view.getComputedStyle !== 'function') {
            return null;
        }
        return view.getComputedStyle(element, pseudo || null);
    }

    function styleSnapshot(element, view, properties, pseudo) {
        var style = computed(element, view, pseudo);
        var result = {};
        if (!style) {
            return result;
        }
        properties.forEach(function (property) {
            result[property] = String(style[property] || '');
        });
        return result;
    }

    function safeStructuralId(element) {
        var id = element && typeof element.id === 'string' ? element.id : '';
        return /^(?:gform_wrapper_\d+|gform_\d+|field_\d+_\d+|input_\d+_\d+(?:_\d+)?)$/.test(id) ? id : null;
    }

    function widthSnapshot(element, view, kind) {
        if (!element) {
            return null;
        }
        return {
            kind: kind,
            tag: String(element.tagName || '').toLowerCase(),
            structuralId: safeStructuralId(element),
            classes: bounded(element.classList || [], MAX_CLASSES).map(String),
            rect: rect(element),
            computed: styleSnapshot(element, view, [
                'display', 'boxSizing', 'width', 'inlineSize', 'minWidth', 'minInlineSize', 'maxWidth', 'maxInlineSize',
                'paddingLeft', 'paddingRight', 'marginLeft', 'marginRight', 'overflowX'
            ])
        };
    }

    function firstVisible(wrapper, selector, view) {
        if (!wrapper || typeof wrapper.querySelectorAll !== 'function') {
            return null;
        }
        var candidates = bounded(wrapper.querySelectorAll(selector), MAX_FIELDS);
        for (var i = 0; i < candidates.length; i += 1) {
            if (visible(candidates[i], view)) {
                return candidates[i];
            }
        }
        return null;
    }

    function widthChain(wrapper, view) {
        var gravityForm = wrapper && typeof wrapper.querySelector === 'function' ? wrapper.querySelector('form') : null;
        var formBody = wrapper && typeof wrapper.querySelector === 'function' ? wrapper.querySelector('.gform-body, .gform_body') : null;
        var fields = wrapper && typeof wrapper.querySelector === 'function' ? wrapper.querySelector('.gform_fields') : null;
        var textControl = firstVisible(
            wrapper,
            'input[type="text"], input[type="email"], input[type="tel"], input[type="url"], input[type="number"], input:not([type]), textarea',
            view
        );
        var radioGroup = firstVisible(wrapper, '.gfield.gfield--type-radio .gfield_radio', view);
        var initialDroparea = firstVisible(wrapper, '.gpfup:not(.gpfup--has-files) .gpfup__droparea', view);
        var submit = firstVisible(wrapper, '.gform-footer .gform_button, .gform_footer .gform_button', view);
        var ancestors = [];
        var current = wrapper ? wrapper.parentElement : null;
        var depth = 0;
        while (current && depth < MAX_WIDTH_ANCESTORS) {
            ancestors.push(widthSnapshot(current, view, depth === 0 ? 'immediate-parent' : 'ancestor'));
            if (String(current.tagName || '').toLowerCase() === 'body') {
                break;
            }
            current = current.parentElement || null;
            depth += 1;
        }

        return {
            wrapper: widthSnapshot(wrapper, view, 'srwf-theme-wrapper'),
            gravityFormsContainers: [
                widthSnapshot(gravityForm, view, 'gravity-forms-form'),
                widthSnapshot(formBody, view, 'gravity-forms-body'),
                widthSnapshot(fields, view, 'gravity-forms-fields')
            ].filter(Boolean),
            ancestors: ancestors.filter(Boolean),
            representativeTextControl: widthSnapshot(textControl, view, 'representative-text-control'),
            representativeRadioGroup: widthSnapshot(radioGroup, view, 'representative-radio-group'),
            representativeInitialUpload: widthSnapshot(initialDroparea, view, 'representative-initial-gpfup-droparea'),
            submit: widthSnapshot(submit, view, 'submit')
        };
    }

    function visible(element, view) {
        var value = rect(element);
        var style = computed(element, view);
        return Boolean(value && value.width > 0 && value.height > 0 && style && style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0');
    }

    function typography(element, view) {
        if (!element) {
            return null;
        }
        return {
            rect: rect(element),
            computed: styleSnapshot(element, view, ['fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'color'])
        };
    }

    function numericDimension(element, property) {
        var value = element && Number(element[property]);
        return Number.isFinite(value) ? value : null;
    }

    function scrollSurfaceSnapshot(element, view, kind) {
        if (!element) {
            return null;
        }
        var clientWidth = numericDimension(element, 'clientWidth');
        var scrollWidth = numericDimension(element, 'scrollWidth');
        return {
            kind: kind,
            rect: rect(element),
            overflowX: styleSnapshot(element, view, ['overflowX']).overflowX || '',
            clientWidth: clientWidth,
            scrollWidth: scrollWidth,
            horizontalScrollOverflow: clientWidth !== null && scrollWidth !== null ? scrollWidth > clientWidth + 1 : null
        };
    }

    function actualHorizontalScrollSurface(wrapper, view, documentObject) {
        var current = wrapper;
        var depth = 0;
        while (current && depth < MAX_SCROLL_ANCESTORS) {
            var style = computed(current, view);
            var overflowX = String(style && style.overflowX || '');
            if (/^(auto|scroll)$/.test(overflowX)) {
                return scrollSurfaceSnapshot(current, view, current === wrapper ? 'theme-wrapper' : 'scroll-ancestor');
            }
            current = current.parentElement || null;
            depth += 1;
        }

        var scrolling = documentObject && (documentObject.scrollingElement || documentObject.documentElement || documentObject.body);
        return scrollSurfaceSnapshot(scrolling || wrapper, view, scrolling ? 'document-scrolling-element' : 'theme-wrapper-fallback');
    }

    function visibleOverflow(wrapper, view, documentObject) {
        var wrapperRect = rect(wrapper);
        var surface = actualHorizontalScrollSurface(wrapper, view, documentObject);
        if (!wrapperRect || !wrapper || typeof wrapper.querySelectorAll !== 'function') {
            return {
                detected: false,
                visibleConsumerOverflowDetected: false,
                sampledVisibleConsumers: 0,
                overflowingVisibleConsumers: 0,
                scrollingSurface: surface
            };
        }
        var candidates = bounded(wrapper.querySelectorAll('input, select, textarea, button, .ts-control, .gfield, .gpfup__droparea, .gchoice > label'), 160);
        var sampled = 0;
        var overflowing = 0;
        candidates.forEach(function (candidate) {
            if (!visible(candidate, view)) {
                return;
            }
            var value = rect(candidate);
            sampled += 1;
            if (value.x < wrapperRect.x - 1 || value.x + value.width > wrapperRect.x + wrapperRect.width + 1) {
                overflowing += 1;
            }
        });
        var scrollOverflow = Boolean(surface && surface.horizontalScrollOverflow === true);
        return {
            detected: overflowing > 0 || scrollOverflow,
            visibleConsumerOverflowDetected: overflowing > 0,
            sampledVisibleConsumers: sampled,
            overflowingVisibleConsumers: overflowing,
            scrollingSurface: surface
        };
    }

    function rowRhythm(wrapper, view) {
        var fields = bounded(wrapper.querySelectorAll('.gform_fields > .gfield'), MAX_FIELDS).filter(function (field) {
            return visible(field, view) && !(field.classList && field.classList.contains('gfield--type-section'));
        });
        var rows = [];
        fields.forEach(function (field) {
            var value = rect(field);
            var row = rows.length ? rows[rows.length - 1] : null;
            if (row && Math.abs(value.y - row.top) <= 2) {
                row.bottom = Math.max(row.bottom, value.y + value.height);
                return;
            }
            rows.push({ top: value.y, bottom: value.y + value.height });
        });
        return {
            rowCount: rows.length,
            gapsPx: rows.slice(1, 5).map(function (row, index) { return Number(row.top - rows[index].bottom); })
        };
    }

    function sectionSnapshots(wrapper, view) {
        var result = [];
        SECTION_ROLES.forEach(function (role) {
            var field = wrapper.querySelector('.gfield--type-section.' + role);
            var title = field && field.querySelector('.gsection_title');
            if (!field || !title) {
                return;
            }
            result.push({
                role: role,
                heading: typography(title, view),
                headingGap: styleSnapshot(title, view, ['gap', 'columnGap']),
                divider: styleSnapshot(field, view, ['borderBottomWidth', 'borderBottomStyle', 'borderBottomColor']),
                icon: styleSnapshot(title, view, ['width', 'height', 'borderRadius', 'backgroundSize'], '::before')
            });
        });
        return result;
    }

    function representativeLabel(wrapper, view) {
        var labels = bounded(wrapper.querySelectorAll('.gfield:not(.gfield--type-section) .gfield_label'), MAX_FIELDS);
        for (var i = 0; i < labels.length; i += 1) {
            if (visible(labels[i], view)) {
                return typography(labels[i], view);
            }
        }
        return null;
    }

    function orderedGapChain(parts) {
        var visibleParts = parts.filter(function (part) { return part.rect; });
        visibleParts.sort(function (a, b) {
            if (Math.abs(a.rect.y - b.rect.y) <= 1) {
                return a.order - b.order;
            }
            return a.rect.y - b.rect.y;
        });
        return visibleParts.map(function (part, index) {
            var next = index + 1 < visibleParts.length ? visibleParts[index + 1] : null;
            return {
                kind: part.kind,
                rect: part.rect,
                gapToNextPx: next ? Number(next.rect.y - (part.rect.y + part.rect.height)) : null,
                nextKind: next ? next.kind : null
            };
        });
    }

    function labelControlChain(wrapper, view) {
        var fields = bounded(wrapper.querySelectorAll('.gform_fields > .gfield:not(.gfield--type-section)'), MAX_FIELDS);
        for (var i = 0; i < fields.length; i += 1) {
            var field = fields[i];
            if (!visible(field, view)) {
                continue;
            }
            var label = field.querySelector('.gfield_label');
            var helper = field.querySelector('.gfield_description:not(.gform_fileupload_rules)');
            var error = field.querySelector('.gfield_validation_message');
            var control = field.querySelector('.ts-wrapper > .ts-control, input:not([type="hidden"]):not([type="radio"]):not([type="checkbox"]), select, textarea');
            if (!label || !control || !visible(label, view) || !visible(control, view)) {
                continue;
            }
            var labelRect = rect(label);
            var helperRect = helper && visible(helper, view) ? rect(helper) : null;
            var errorRect = error && visible(error, view) ? rect(error) : null;
            var controlRect = rect(control);
            var chain = orderedGapChain([
                { kind: 'label', rect: labelRect, order: 0 },
                { kind: 'helper', rect: helperRect, order: 1 },
                { kind: 'error', rect: errorRect, order: 2 },
                { kind: 'control', rect: controlRect, order: 3 }
            ]);
            var predecessor = errorRect || helperRect || labelRect;
            return {
                label: typography(label, view),
                helper: helperRect ? typography(helper, view) : null,
                error: errorRect ? typography(error, view) : null,
                control: typography(control, view),
                gapChain: chain,
                finalTextToControlGapPx: predecessor && controlRect ? Number(controlRect.y - (predecessor.y + predecessor.height)) : null
            };
        }
        return null;
    }

    function uploadSnapshot(field, view) {
        if (!field) {
            return null;
        }
        var root = field.querySelector('.gpfup');
        var drop = field.querySelector('.gpfup__droparea');
        if (!root || !drop) {
            return null;
        }
        var classes = bounded(root.classList || [], 24).map(String);
        var selectFiles = field.querySelector('.gpfup__select-files');
        var rules = field.querySelector('.gform_fileupload_rules');
        return {
            hasFiles: classes.indexOf('gpfup--has-files') !== -1,
            rootClasses: classes.filter(function (value) { return /^gpfup/.test(value); }),
            dropArea: {
                rect: rect(drop),
                computed: styleSnapshot(drop, view, ['minHeight', 'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft', 'borderTopWidth', 'borderTopStyle', 'borderTopColor', 'borderRadius', 'backgroundColor', 'fontSize', 'fontWeight', 'lineHeight', 'columnGap', 'rowGap']),
                pseudoBefore: styleSnapshot(drop, view, ['width', 'height', 'backgroundSize', 'backgroundImage', 'borderRadius'], '::before'),
                childStructure: bounded(drop.children || [], 12).map(function (child) {
                    return { tag: String(child.tagName || '').toLowerCase(), classes: bounded(child.classList || [], 12).map(String) };
                })
            },
            selectFiles: typography(selectFiles, view),
            fileRules: typography(rules, view)
        };
    }

    function uploads(wrapper, view) {
        var reportField = wrapper.querySelector('.gfield.srwf-role-report-card-upload');
        var imageRoot = wrapper.querySelector('.gfield--type-fileupload .gpfup.gpfup--images-only');
        var imageField = imageRoot && typeof imageRoot.closest === 'function' ? imageRoot.closest('.gfield--type-fileupload') : null;
        return {
            reportCard: uploadSnapshot(reportField, view),
            studentPhoto: imageField ? {
                status: 'HOST_CONFIG_ADMITTED',
                admission: 'gpfup--images-only',
                snapshot: uploadSnapshot(imageField, view)
            } : {
                status: 'NOT_PROVEN',
                reason: 'no-authentic-images-only-gpfup-consumer-admitted'
            }
        };
    }

    function gpas(wrapper, view) {
        if (!wrapper || typeof wrapper.querySelector !== 'function') {
            return null;
        }
        var control = wrapper.querySelector('.ts-wrapper > .ts-control');
        if (!control) {
            return null;
        }
        var parent = control.parentElement;
        return {
            consumer: 'ts-wrapper-direct-control',
            snapshot: typography(control, view),
            computed: styleSnapshot(control, view, ['minHeight', 'outlineWidth', 'outlineStyle', 'outlineColor', 'outlineOffset']),
            dynamicState: parent && parent.classList && parent.classList.contains('dropdown-active') ? 'OPEN_RUNTIME_OBSERVED' : 'NOT_PROVEN_CLOSED'
        };
    }

    function primaryAction(wrapper, view) {
        if (!wrapper || typeof wrapper.querySelector !== 'function') {
            return null;
        }
        var button = wrapper.querySelector('.gform-footer .gform_button, .gform_footer .gform_button');
        return button ? typography(button, view) : null;
    }

    function targetSnapshot(wrapper, view, documentObject) {
        return {
            shell: { rect: rect(wrapper), horizontalOverflow: visibleOverflow(wrapper, view, documentObject) },
            widthChain: widthChain(wrapper, view),
            rowRhythm: rowRhythm(wrapper, view),
            representativeFieldLabel: representativeLabel(wrapper, view),
            labelControlChain: labelControlChain(wrapper, view),
            sections: sectionSnapshots(wrapper, view),
            uploads: uploads(wrapper, view),
            gpas: gpas(wrapper, view),
            primaryAction: primaryAction(wrapper, view),
            runtimeOnlyStates: {
                selectedRadio: 'OBSERVE_IF_CHECKED',
                keyboardFocus: 'OBSERVE_IF_FOCUSED',
                validation: 'OBSERVE_IF_AUTHENTIC_INVALID_STATE',
                gpasDynamic: 'OBSERVE_IF_AUTHENTIC_OPEN_OR_ERROR_STATE',
                postUpload: 'OBSERVE_IF_AUTHENTIC_HAS_FILES'
            }
        };
    }

    function collect(documentObject, view) {
        var wrappers = documentObject && typeof documentObject.querySelectorAll === 'function' ? bounded(documentObject.querySelectorAll(TARGET_SELECTOR), MAX_TARGETS) : [];
        return {
            diagnosticVersion: VERSION,
            viewportCssWidth: view ? Number(view.innerWidth || 0) : 0,
            devicePixelRatio: view && Number.isFinite(Number(view.devicePixelRatio)) ? Number(view.devicePixelRatio) : null,
            targetCount: wrappers.length,
            targets: wrappers.map(function (wrapper) { return targetSnapshot(wrapper, view, documentObject); })
        };
    }

    return {
        VERSION: VERSION,
        TARGET_SELECTOR: TARGET_SELECTOR,
        MAX_WIDTH_ANCESTORS: MAX_WIDTH_ANCESTORS,
        collect: collect
    };
}));
