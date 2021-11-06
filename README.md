# fc: The flipbook compiler

fc is a compiler for compiling flipbook recipes (written in the flip language) into a flipbook. Currently only outputting PDF is supported but other output formats can be easily added.

## Time Taken

Overall, I've spent roughly 8-10 hours on the project, spread over many sessions due to the current festive season.

## How to run

To run, we first need to install the required packages. So create a virtual environment, activate it and then run `pip install -r requirements.txt`

Then we can give it a .flip file to compile into a PDF. Some examples are present in the `examples/` folder. For example, we can run `python -m fc examples/newton.flip -o output.pdf` to compile the recipe [examples/newton.flip](examples/newton.flip) into the flipbook PDF `output.pdf`.

## Directory Structure

See [docs/directoryStructure.md](docs/directoryStructure.md) for a detailed description on how the codebase is organised. It is recommended to go through it before diving into reading the code.

## The Flip language

We have a very bare-bones language to describe a flipbook. It currently has 3 primitives to describe what's happening: Image, Tween and Scene. An Image represents an image, a Tween describes movement of some Image/Tween/Scene object and a Scene is a collection of objects with possibly different positions and start/end frames.

For detailed description of the language, see [docs/flipLang.md](docs/flipLang.md).

### Language Support

fc supports all of the Flip language except the specification of starting and ending frames in a scene element.

## Future Scope

### Language

The language has been so designed that little change to the grammar would be required to add some feature and old programs would still work.

Some features that could be added to enhance the language:

- A header could be added that specifies paramaters to configure a specific format outputter. For example `output pdf size A4` could specify that the size of the output PDF (if generated) should be A4.
  - Some more headers could potentially be added: to specify the base directory for images, to allow importing other flip files
- Since things like a frame descriptor could be a bit confusing to read, we could add another production for `frame_desc` to have it support a syntax like `frame=5 x=0 y=10.6`
- We could also add optional size parameter for a scene_element, to allow scaling of the primitives when they are put in a scene. This would be helpful in reusing an animation or a scene in different places where different sizes of it are required.

### Compiler

Firstly, the compiler has to evolve as the language evolves. Hopefully, this is helped by how the codebase is organised. A change in the AST goes into `ast.py` and in the rules goes into `parser.py`. Any new feature that a outputter needs to support goes into it's own directory, for example `pdf/`.

Currently, starting and ending frame numbers for a scene element hasn't been implemented. It's not very hard to do but not trivial either since we'd need to take a call on how to scale something in time. A scene with 3 frames of one image and 3 frames of another could be scaled down into 5 frames by either having one image take 3 frames and the other 2 or placing both of them on the 3rd frame with transparency.

#### Support of Multiple Outputters

As we add more outputters, we'll find what commonalities they have and we can take that to implement a IR (Intermediate Representation) for a frame. The `pdf/frame.py` file's functionality can be extracted into the IR.

#### Efficiency

The current method for generating frames from the AST is not very efficient since it has to basically traverse the AST for every frame. For example if a tween is contained in a tween, what we are currently doing is for each frame of the outer tween, generate one frame for the inner tween. This could be made better if we transformed the nested Tween objects into a single Tween object. It would not require traversing all the frames, but would only depend on number of frames specified in the tween.
