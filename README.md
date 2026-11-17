# Mahsa Asghari — public research portfolio, redesigned

The complete main experience is in **index.html**: embedded styles, font subsets, imagery, optional JavaScript enhancements, decorative animation and public PDF download data. Publish it without a build step, dependencies or a backend.

For the full update of the existing repository, upload **all files and folders in this package**, preserving paths. See [README_FA.md](README_FA.md) for Persian instructions.

## Content

Four published studies are presented through native expandable sections. The unpublished OCT work is limited to a short concept-level statement. No figures, photographs, measurements or technical description of that work are included.

The public PDF is a newly designed five-page selection of the published research. The original detailed portfolio is not distributed here.

## Existing URL compatibility

- Four old published-project routes redirect to their corresponding study anchors.
- The old unpublished-project route contains only the short concept-level statement.
- Old unpublished image URLs have empty one-pixel replacement files, including their previous originals paths. These are overwrite stubs, not research figures.
- Updated project data, template, credits, contact sheet and download PDF replace their prior public paths when the full package is uploaded.

Uploading only index.html changes the main page but does not overwrite previously uploaded files at separate paths.

## Edit and regenerate

The source content is in scripts/site_content.json and scripts/templates/home.html. Shared styles and enhancements are in assets/style.css and assets/site.js.

    python scripts/generate_site.py
    python scripts/check_site.py

Only PDF regeneration requires the optional requirements.txt:

    python -m pip install -r requirements.txt
    python scripts/make_public_pdf.py
    python scripts/generate_site.py

The public source images, font subsets and their notices are included. No private source PDF is needed.

## Progressive enhancement and motion

Native details and semantic content remain usable without JavaScript. JavaScript adds filters, figure enlargement, clipboard feedback, deep-link opening, embedded PDF downloads and decorative Canvas 2D studies. The plain PDF link remains as a no-JavaScript fallback in a full upload.

Animation has shared pause controls, honors prefers-reduced-motion, pauses when the document is hidden, renders only visible scenes, and caps device pixel density. All motion studies are illustrative artwork, not experimental data.

See VALIDATION.md for completed verification and ASSET_CREDITS.md for image and font provenance.
