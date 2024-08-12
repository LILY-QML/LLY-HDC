
![HDC-removebg-preview](https://github.com/user-attachments/assets/9d16429e-9742-484c-9541-fccd83893cec)
# Introduction

**LLY-DML** is part of the [**LILY Project**](https://www.lilyqml.de) and focuses on optimization parameter-based quantum circuits. It enhances the efficiency of quantum algorithms by fine-tuning parameters of quantum gates. **DML** stands for **Differentiable Machine Learning**, emphasizing the use of gradient-based optimization techniques to improve the performance of quantum circuits.

LLY-DML is available on the [LILY QML platform](https://www.lilyqml.de), making it accessible for researchers and developers.

For inquiries or further information, please contact: [info@lilyqml.de](mailto:info@lilyqml.de).





## Contributors

| Role                     | Name          | Links                                                                                                                |
|--------------------------|---------------|----------------------------------------------------------------------------------------------------------------------|
| Project Lead             | Leon Kaiser   | [ORCID](https://orcid.org/0009-0000-4735-2044), [GitHub](https://github.com/xleonplayz)                              |
| Inquiries and Management | Raul Nieli    | [Email](mailto:raul.nieli@lilyqml.de)                                                                                |
| Supporting Contributors  | Eileen Kühn   | [GitHub](https://github.com/eileen-kuehn), [KIT Profile](https://www-kseta.ttp.kit.edu/fellows/Eileen.Kuehn/)        |
| Supporting Contributors  | Max Kühn      | [GitHub](https://github.com/maxfischer2781)                                                                          |


## Table of contents

1. [Hyperdimensional Properties](#hyperdimensional-properties)
    - [Encoder and Object Recognition](#encoder-and-object-recognition)
        - [Goal of the Encoder](#goal-of-the-encoder)
        - [Functionality of the Encoder](#functionality-of-the-encoder)
    - [HDC Engine Operations](#hdc-engine-operations)
2. [Reflection in Hyperdimensional Computing](#reflection-in-hyperdimensional-computing)
    - [Reflection](#reflection)
        - [Objective of Reflection](#objective-of-reflection)
        - [Functionality of Reflection](#functionality-of-reflection)
3. [Spheres](#spheres)
    - [Tasks of Individual Spheres](#tasks-of-individual-spheres)
    - [Connection Between Spheres](#connection-between-spheres)
    - [Sub-Spheres](#sub-spheres)
4. [Static and Dynamic Vector Regions](#static-and-dynamic-vector-regions)
5. [Global and Local Measurements](#global-and-local-measurements)

---

## Hyperdimensional Properties

### Encoder and Object Recognition

#### Goal of the Encoder

The encoder's goal is to transform an input in the form of words into a high-dimensional vector space, including the relationships that the vectors have with each other. In doing so, the encoder goes through a series of steps, including forming spheres and sub-spheres along the high-dimensional vector. A neural network, optimized through NEAT (NeuroEvolution of Augmenting Topologies), reacts to the input tokens and forms individual regions along the high-dimensional vector.

#### Functionality of the Encoder

1. **Input Processing:**
    - The input in the form of words is passed to the encoder.
    - The transformer tokenizes the input and goes through various transformation layers.
    - The transformer outputs the individual objects of the sentence as tokens and classifies the relationships between these tokens.
2. **Processing by the Neural Network:**
    - The neural network, called Neural HDS (HyperDimensional Space), takes over the data and maps the relationships to the high-dimensional vectors.
3. **Transfer to the HDC Engine:**
    - The data from the neural network is passed to the HDC (HyperDimensional Computing) engine.
    - The HDC engine takes the neural network data and maps it to the high-dimensional space.

### HDC Engine Operations

The neural network passes the data it has processed to the HDC (HyperDimensional Computing) engine, which converts them into high-dimensional vectors. These vectors can then perform the following operations:

- **Addition of Vectors:** Based on their relationships, vectors can be added to create common properties or merge their features. For example, when adding "green" and "apple," the attribute "fresh" is attributed to the apple.
- **Entanglement Between Vectors:** Individual relationships can be represented along the spheres of the high-dimensional vector. For example, the vector area representing the apple's location is entangled with the tree's vector, creating a tendency towards the tree.
- **Bundling of Vectors:** Bundling refers to the individual addition, multiplication, or entanglement of individual vectors. This serves to condense information.
- **Permutation of Vectors:** The individual vector areas are rearranged or loaded with altered values to determine new results.
- **Extending the Vector:** Pattern elements are assigned to the vector to solve complex questions. The data is further permuted until a suitable concept is found, and a desired output is generated.

## Reflection in Hyperdimensional Computing

### Reflection

In reflection, the data extracted from the high-dimensional space is evaluated and processed. The decoder first measures all necessary data and provides it to the transformer. This formulates the data and checks it for consistency and whether it answers the question posed. If not, the transformer passes the data to the reflection neural network, which permutes the vectors and data in the high-dimensional space.

#### Objective of Reflection

The objective of reflection is to validate the data and determine whether the posed question is answered. If not, feedback is sent to adjust the vectors.

#### Functionality of Reflection

After the data from the high-dimensional space is passed to the transformer, it checks whether the data can answer the question posed. If not, the critique is transferred to the Neural Reflector Engine as classifications. This engine permutes and processes the respective places in the vectors to achieve the desired result. This process is repeated until a valid result is generated. If a valid result is generated, the transformer formulates the result and outputs it.

## Spheres

A sphere is a multi-qubit system that can have different purposes and structures. The term "sphere" is derived from representing this multi-qubit system as a Q-sphere. All possible states of the system, represented by the number of qubits, can be depicted on the surface of a sphere. Depending on the input data, these different states are activated, giving the multi-qubit system unique properties. The composition of the sphere can vary, so spheres can be created for different purposes.

### Tasks of Individual Spheres

1. **Perception Sphere:** The task of the perception sphere is to process the data and pass it to the processor.
2. **Classifying Sphere:** The task of the classifying sphere is to measure and categorize the data in a unique form.

### Connection Between Spheres

The spheres are directly connected and entangled, allowing each to influence the other's data.

### Sub-Spheres

The sub-spheres of the individual spheres process tasks specifically and then pass the processed data back to the actual sphere.

## Static and Dynamic Vector Regions

1. **Static Vectors:** Static vectors represent the actual space in which all necessary data is located.
2. **Dynamic Vectors:** Dynamic vectors allow certain regions to shift based on the questions posed. They operate based on specific dynamic protocols that can represent the desired state more accurately.

## Global and Local Measurements

Measurement takes place on several levels:

1. **Local Level:** Spheres and their significance are measured individually.
2. **Contextual Level:** Spheres in their encryption context are measured.
3. **Global Level:** Spheres within the entire system are measured.
