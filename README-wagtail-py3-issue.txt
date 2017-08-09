As of 9 August 2017 there are two files in the top dir of the pyconau2017/website repo:

    struct_block.py
    test_blocks.py

These are updated versions of the same files found in the wagtail distribution pulled from 
ppi.  The contain bug fixes for an issue that prevents the site from starting in DEBUG = True
mode.  Replace the files of the same name in these dirs:

   VENVROOT/lib/python3.5/site-packages/wagtail/wagtailcore/blocks
   VENVROOT/lib/python3.5/site-packages/wagtail/wagtailcore/tests

respectively.

Once the ppi archive has been updated to include these fixes, these two files, and this README
can be removed from the repo.

Nick Seidenman <n6151h@gmail.com> 
9 August 2017

