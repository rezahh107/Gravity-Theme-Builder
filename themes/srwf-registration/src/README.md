## First real implementation

The first real presentation implementation is theme-local under `src/`. It is not production-qualified until the required Gravity Forms runtime checks are completed.

### Activation

The implementation uses Gravity Forms' own supported extension points rather than registering a parallel renderer:

1. install/activate `src/srwf-registration-theme.php` with `src/srwf-registration.css` adjacent to it as one small WordPress plugin directory;
2. on the intended SRWF form only, set **Form Settings → Form Layout → CSS Class Name** to `srwf-registration-theme`;
3. keep **Description Placement** and **Validation Message Placement** below inputs and enable the authentic Gravity Forms **Validation Summary** per the approved visual contract.

For that opted-in form, the integration selects the `orbital` form theme through `gform_form_theme_slug` and enqueues the stylesheet through `gform_enqueue_scripts`. Other forms are left untouched. The CSS itself is additionally scoped to `.gform-theme--framework.srwf-registration-theme_wrapper`.

Vazirmatn delivery remains owned by the embedding SRWF environment; this package does not fetch fonts from a third-party CDN.

### Deliberately unresolved

The production breakpoint, desktop short-field pairings, desktop shadow, exact focus-ring geometry/alpha, form-title sizing/line-height, helper/error font sizes, and exact field/section rhythm remain unresolved exactly as the admitted contract requires. GP Advanced Select, PersianGravity Jalali UI, and GP File Upload Pro/crop selectors are not authored until their real runtime consumers are inspected.

Run deterministic checks with:

```bash
bash themes/srwf-registration/reference/materialize_reference.sh /tmp/OWNER_REFERENCE_new_7.html
python3 -m unittest discover -s themes/srwf-registration/tests -p 'test_*.py' -v
php -l themes/srwf-registration/src/srwf-registration-theme.php
```

These checks are repository/static evidence only. They do not qualify the theme against a real WordPress + Gravity Forms runtime.
