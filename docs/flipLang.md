# The Flip Language

This doc aims to explain the Flip language in detail. It is not mechanical detail (as in a language reference), and for that, it's best to refer to the grammar, available in [fc/flip.lark](../fc/flip.lark).

## Concepts

### Coordinate Axis

The origin is at the lower left with the x coordinate increasing as we go towards the right and y coordinate increasing as we go towards the top.

### Identifiers

Flip only allows using an identifier of an object after we have declared the object itself. This simplifies implementation of the compiler since we'll only require one pass of the AST for symbol resolution but the downside is that the program has to be structured in a specific way, which is the better way in my opinion.

### Size and Position

All the sizes and positions in the programs are specified in terms of squares of the grid. As an example, a size of `4 5` would mean that the object occupies 4 squares horizontally and 5 squares vertically. Similarly, a position `2 3` means that the origin of the object is at the square (2, 3). Currently when we say square (2, 3) we mean the center of the square, but this can be made configurable by allowing anchors to be specified.

## Header

A header is placed before any other object can be declared. There can be potentially many of these, but currently we only have the `grid` header.

### Grid

Syntax: `grid <sizeX> <sizeY>`

This specifies that the grid for this program has a size `sizeX` by `sizeY`. This means that the width of the output is divided into `sizeX` squares and the height is divided into `sizeY` squares.

## Object

### Image

Syntax: `image <imageName> <sizeX> <sizeY> <path>`

This declares an image that will be identified by the name `imageName` which will occupy whatever the maximum it can in `sizeX` by `sizeY` squares in the grid. The image used is present at `path`.

### Tween

A tween represents motion of an object.

Syntax: `tween <tweenName> <objectName> { <frameDescList> }`

This declares a tween that will be identified by the name `tweenName`. The tween is on the object called `objectName` and the actual motion is described by `frameDescList`, which is a comma separated list of frame descriptors.

#### Frame Descriptor

A frame descriptor is specified by `<frameNumber> <posX> <posY>`, which says that at frame number `frameNumber` the object should be at `(posX, posY)`. To generate motion between 2 frame descriptors in a tween, we linearly interpolate between the two positions. Note that other interpolations can be added as a language feature to allow things like easing in.

### Scene

A scene is a collection of objects who are at different places and whose lifetime can also be optionally specified.

Syntax: `scene <sceneName> { <sceneElementList> }`

This declares a scene that will be identified by the name `sceneName`. The different objects present in the scene are described by `sceneElementList` which is a comma separated list (with an optional trailing comma) of Scene Elements

#### Scene Element

A scene element describes where an object is to be placed in the scene and optionally, from when to when does it exist in the scene. It is specified by `[<beginFrame> <endFrame>] objectName <posX> <posY>`. It says that the object called `objectName` is placed at position `(posX, posY)` (in terms of squares of the grid) and optionally, it begins at `beginFrame` and ends at `endFrame`. Otherwise, it will be rendered for all frames of the scene.

## Comments

Flip also allows adding comments with syntax same as C. This means that anything after `//` till the newline character will be ignored and anything between `/*` and /*/` is ignored.
