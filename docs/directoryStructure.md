# Directory Structure

Here we aim to describe the directory structure and the rationale behind it in hopes that it will make navigating through the code base easier.

```text
    - docs/                         -- Contains separate docs detailing different things
        - directoryStructure.md     -- Explains the directory structure of the project
        - flipLang.md               -- Explains the design of the Flip language
    - examples/                     -- Contains example programs written in Flip
        - newton.flip               -- An example program showing an apple projectile hitting newton
        - newtonFlip.pdf            -- Compiled output of newton.flip
        ...
    - fc/                           -- This directory contains the source code of fc
        - __main__.py               -- Specifies what to call when running fc as a script. Calls cli.main
        - ast.py                    -- Contains classes to represent the AST
        - cli.py                    -- Entry point into execution. Parsers args, then calls functions to parse and output.
        - config.py                 -- Constants are put here instead of littering them across files where they are used.
        - flip.lark                 -- Grammar for Flip written for Lark parser. Rules are in EBNF, so should be easy to
                                    -- switch to another parser if needed
        - parser.py                 -- Given a program, contains code to parse it into the AST
        - pdf/                      -- Separate directory for code specific to outputting flipbook in PDF format
                                    -- An outputter for GIF would be put in a gif/ directory.
            - config.py             -- Defines the Config object which is used to configure different parts of the PDF output
                                    -- Separate object makes it easy to pass all the info so everyone can use what they need.
            - frame.py              -- Contains code to convert the AST into a list of frames
            - outputter.py          -- Interface used by the outer world. Takes in the AST, makes frames and then renders them.
    - .gitignore
    - README.md
    - problem-stmt.pdf
    - requirements.txt
```
