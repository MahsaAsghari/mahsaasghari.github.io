# Delivery verification — redesigned public edition

Checked 17 November 2026.

## Scope and content

- The public research collection contains four published studies.
- OCT is limited to a short, explicitly unpublished concept-level statement. The previous technical description, measurements, setup photographs and figures are absent.
- The old unpublished-project route now displays only the same concept-level statement and a return link.
- Named legacy image files are empty one-pixel replacement images, checked programmatically. They allow a full-package upload to replace earlier public images without carrying the research content forward.
- The asset inventory and contact sheet contain only the public portrait and published-project figures.
- The downloadable PDF is a new five-page public selection. Every page was rasterized and visually reviewed. The original detailed source PDF is not bundled.
- PDF text and generated public text were checked for removed unpublished-work details.

## Static checks

- The generated page has one H1, four study disclosures, unique IDs and valid internal fragment targets.
- Styles, font subsets, interface scripts and displayed images are embedded in index.html; there are no external CSS or JavaScript dependencies.
- Every embedded publication image was decoded and verified. Captions, axes, labels and source aspect ratios are retained.
- The embedded PDF data matches the public PDF in assets/documents.
- All four compatibility routes target valid study anchors.
- JavaScript syntax checks pass.

## Browser checks

- Inspected the desktop home page, research disclosures, decorative light studies and contact layout in Chrome.
- Inspected 320, 390, 768 and 1440 CSS-pixel iframe viewports. No horizontal document overflow was observed in checked states.
- Checked the mobile menu opening and closing through navigation.
- Opened a published study, enlarged a figure, changed full-size viewing, and closed the viewer with Escape.
- Checked both research filters: two Dynamics studies and two Sensing studies.
- Checked shared motion pause/resume controls and the resulting paused state.
- Checked a JavaScript-disabled frame: navigation and all four native study disclosures remained available, and a disclosure could be opened.
- Tested a directory containing only index.html: the page had no broken embedded images, and the public PDF downloaded through its embedded data.
- Checked an existing published-project route redirecting to its open study and checked the minimal unpublished-concept route with zero images.
- Checked the email-copy success feedback.

## Limits

The browser checks used Chrome with representative CSS viewport sizes, rather than physical devices or a full cross-browser/assistive-technology audit. The native reduced-motion preference was implemented and reviewed in source; it was not independently emulated in the browser.

This package prepares the update for the existing GitHub Pages repository. No changes were pushed to that repository and no new public deployment was performed.
