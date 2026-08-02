# Plain-language course spine shared by the generated pages.

COURSE_TITLE = "The Simple Course Spine"

COURSE_DEK = (
    "A long, plain essay for reading the whole SIGGRAPH 2026 project as one "
    "course: what the field is trying to do, why the first principles matter, "
    "and how the same ideas show up in graphics, topology, design, robotics, "
    "medicine, manufacturing, and other fields."
)

COURSE_SECTIONS = [
    {
        "kicker": "Start Here",
        "title": "The whole subject in one everyday question",
        "body": [
            "Computer graphics is not just the study of pretty pictures. It is the study of how to turn a world into numbers, change those numbers in a controlled way, and turn them back into something a person can see, judge, use, or build. That world may be a face, a cup, a room, a splash of water, a piece of cloth, a tree, a medical scan, a street, a game scene, or an object that does not exist yet.",
            "The first question is always simple: what must the computer remember about the thing? For a shape, it may need points, edges, faces, inside and outside, distance to the surface, or how pieces touch. For light, it may need where rays go and what they hit. For motion, it may need position, speed, force, mass, and time. For a material, it may need how the surface answers light. For a learned model, it may need many examples and a way to copy the pattern without copying one example exactly.",
            "That is why first principles matter. A first principle is the basic reason under the technique. It asks what is being stored, what is being measured, what is being kept fixed, what is allowed to change, and what counts as a better answer. Without that, a paper becomes a pile of names. With it, the field becomes readable."
        ],
    },
    {
        "kicker": "The Main Loop",
        "title": "Describe, change, check, repeat",
        "body": [
            "Most of the course follows one loop. First describe the object in a form the computer can hold. Then change it by a rule. Then check whether the result is better. Then repeat until the object looks right, moves right, or matches the evidence.",
            "A mesh smoother does this with a shape: take rough points, move each point toward its neighbors, check whether the surface became cleaner, and keep enough of the old size so the object does not shrink away. A camera fitting method does this with pictures: guess a camera, project the known points, measure how far the projected points are from the observed ones, then adjust the camera. A material fitting method does this with light: guess surface values, render a picture, compare it to the target, and adjust the values.",
            "The important idea is not the special name of the method. The important idea is the loop. A computer cannot understand beauty, realism, or usefulness directly. It needs a score, a rule for changing the numbers, and a way to stop when small changes no longer help."
        ],
    },
    {
        "kicker": "Shapes",
        "title": "Why shape is harder than it looks",
        "body": [
            "A real object has no built-in grid. It is continuous. You can zoom in and still see more surface. A computer cannot store that whole thing, so it stores a useful substitute. Sometimes the substitute is a skin of small triangles. Sometimes it is a distance rule that answers, for any point in space, how far that point is from the surface. Sometimes it is a cloud of points from a scan. Sometimes it is a learned rule that can produce the shape when asked.",
            "Every choice has a cost. Triangles are direct and easy to draw, but they can tear, fold, or become too heavy. Distance rules are smooth and flexible, but they can hide details and need careful sampling. Point clouds are easy to capture, but they do not automatically say which points form a surface. Learned shape rules can fill gaps, but they may invent a plausible answer that is not the true answer.",
            "This is why geometry processing matters outside graphics too. The same problem appears in medical scans, robot maps, factory inspection, architecture, biology, and 3D printing. In each case, the practical question is the same: can we store the important shape without keeping every raw measurement, and can we change it without breaking what makes it the same object?"
        ],
    },
    {
        "kicker": "Topology",
        "title": "Topology means how pieces stay connected",
        "body": [
            "Topology is often made to sound mysterious. In this course it should mean something very plain: which parts are connected, which parts are separate, where there is a hole, where there is a loop, where a surface has a boundary, and whether changing the shape would cut or glue pieces together.",
            "A coffee mug and a doughnut have the same kind of hole. A bowl and a ball do not. A shirt has openings for the neck, arms, and body. A road map has crossings and routes. A blood vessel tree has branches. A character skeleton has joints connected in a certain order. A mesh for a game object may look fine from one angle but still be broken if two pieces that should be separate were accidentally joined.",
            "Topology matters because many failures are not small visual mistakes. They are wrong relationships. A smoothing method can blur a sharp feature, but a topology mistake can seal a hole, split a surface, connect two separate parts, or make a path impossible. In medicine, that can change whether a vessel appears blocked. In robotics, it can change whether a path exists. In manufacturing, it can change whether an object can be printed or assembled. In animation, it can change whether a body bends like a body. In data analysis, it can change whether a pattern is one cluster, two clusters, a loop, or a branching tree.",
            "The everyday test is this: if you stretch or bend the object without cutting or gluing it, what stays true? Those staying facts are topological facts. They are important because they survive noise, pose, scale, and camera angle. They tell you about the structure of the thing, not just its exact measurements today."
        ],
    },
    {
        "kicker": "Motion",
        "title": "Motion is many small balances over time",
        "body": [
            "To make cloth, water, sand, hair, muscles, or smoke move, the computer does not know the final answer at once. It knows local rules. Gravity pulls down. A spring pulls stretched points back together. Pressure pushes crowded fluid apart. Friction resists sliding. A joint allows some rotations and blocks others. A collision says two solid things cannot occupy the same place.",
            "The hard part is that all these little rules happen together. If one cloth point moves, its neighbors must respond. If water hits sand, the water pushes the sand and the sand pushes back. If a character foot touches the ground, the whole body must adjust. The computer solves this by stepping forward in tiny moments and repeatedly finding a state where the local demands are not fighting each other too badly.",
            "This matters far beyond films and games. The same ideas appear in robot planning, crash testing, surgical simulation, weather, sports science, soft materials, and factory automation. The graphics version is valuable because it cares about both truth and speed: the result must be believable, controllable, and often fast enough to see."
        ],
    },
    {
        "kicker": "Light",
        "title": "A picture is the result of many light paths",
        "body": [
            "A pixel is not just a color chosen from a table. It is the visible result of light traveling through a scene. Light may leave a lamp, bounce off a wall, pass through glass, scatter in fog, hit skin, reflect from metal, and finally reach the camera. The true total is enormous because there are too many possible paths.",
            "Graphics handles this by adding up a limited set of important paths. Sometimes it chooses paths at random and averages them. Sometimes it spends more effort where the image is noisy or where the light changes sharply. Sometimes it uses a learned cleanup step. Sometimes it builds a compact material model so it does not have to simulate every tiny fiber or pore.",
            "The first principle is simple: the color you see is a total effect. The hard part is estimating that total without tracing everything. This same idea appears in medical imaging, remote sensing, acoustics, heat transfer, nuclear transport, and any field where a sensor sees the result of many hidden paths."
        ],
    },
    {
        "kicker": "Capture",
        "title": "A camera gives clues, not the whole truth",
        "body": [
            "A camera sees a flat picture of a three-dimensional world. It loses depth, hides the back side of objects, clips very bright and very dark regions, blurs motion, and mixes the object with the lighting. So many SIGGRAPH papers ask how to recover more of the world from partial evidence.",
            "The first-principles move is to make a guess, render what the guess would look like, compare it with the real picture, and improve the guess. This is why camera fitting, face capture, relighting, image cleanup, and 3D reconstruction all feel related. They are all trying to explain the observed image with hidden causes.",
            "The same idea appears in science and industry whenever measurements are indirect. A scan, sonar return, X-ray, microscope image, or sensor trace is not the thing itself. It is evidence. The work is to find a hidden object or process that would have produced that evidence."
        ],
    },
    {
        "kicker": "Generation",
        "title": "Generation is controlled guessing from examples",
        "body": [
            "Generative models can sound like magic, but the everyday idea is modest: learn from many examples what kinds of shapes, images, motions, or materials are likely, then use that learned sense to make a new one. The model is not simply copying a paper, a chair, or a person. It is learning many repeated patterns and recombining them under a request.",
            "The risk is also plain. A generated result can be plausible but wrong. It can fill a missing part with something that looks normal but does not match the real object. It can obey a text prompt while breaking physics, anatomy, topology, scale, or material behavior. That is why the older first principles still matter. The generated object must still have a sound shape, stable motion, consistent lighting, and useful structure.",
            "This is the 2026 shift: learning is spreading across the whole pipeline, but it does not remove the pipeline. It gives better guesses. The checks still come from geometry, physics, light, time, and topology."
        ],
    },
    {
        "kicker": "Output",
        "title": "The virtual thing has to reach the real world",
        "body": [
            "At the end, the result must be shown, touched, printed, worn, heard, or used. That adds another set of limits. A display has limited brightness, pixels, focus cues, and viewing angle. A headset must match the eyes and head motion. A printer must follow material and machine limits. A knitting machine cannot make every curve. A drawing tool must fit how artists actually work.",
            "So output is not a final export button. It is its own first-principles problem: what can the device really make, and what will a person really perceive? The best methods plan backward from those limits. They do not ask for an impossible perfect output. They ask for the best output that the hardware and human senses can support."
        ],
    },
    {
        "kicker": "Why It Matters",
        "title": "The bigger picture",
        "body": [
            "This is important because the same few questions appear in many fields. How do we store a complicated thing? How do we keep its structure while changing it? How do we infer hidden causes from weak evidence? How do we move a system forward without making it unstable? How do we add up too many small effects? How do we choose a useful answer when many answers are possible?",
            "Computer graphics is an unusually clear place to learn these questions because mistakes are visible. If topology is wrong, the shape tears or seals a hole. If the light estimate is bad, the image has noise or false shadows. If the motion rule is unstable, the cloth explodes. If the learned model guesses without enough structure, the output looks convincing for a second and then fails under inspection.",
            "That visibility is the gift of the field. It teaches general thinking through objects you can see. The course is not just about SIGGRAPH papers. It is about learning how complex systems become understandable when you keep returning to the same plain questions: what is the object, what is measured, what is connected, what is allowed to change, what is the score, and why should this procedure improve the result?"
        ],
    },
]
