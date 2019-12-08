# problib
A python library for probabilistic utilities and more

## Philosophy
* Why does this library exist? At its roots, it started as a centralized location for me to build out interesting concepts I've encountered in personal studies and at university. It's slowly become a place for me to generalize old scripts/utilities and make them reusable & modular. 

More recently, I've devoted effort specifically toward completeness of submodules within the library as its evolved into its own project. I've also built other tools on top of it (i.e. probapi, probapp) for visualizing the functionality implemented underneath.

## Approach
This library attempts to provide clean, modular implementations of many topics across computer science, mathematics, and optimization. Generally objected oriented implementations are encouraged, as OOP naturally lends itself to the hierarchical nature of many topics (i.e. common structure across machine learning models). Additionally, all implementations are encouraged to use generators for sequential procedures to ensure efficient use of space and on demand result generation. All code is meant to be as decompartmentalized as possible, as self-sufficient and complete as it can be. This isn't to say some areas won't need or shouldn't use dependencies.

## Current Module Structure
* Combinatorics
  * Counting

* Computer Vision
  * Image gradients
  * Edge detection

* Evolutionary algorithms
  * Candidate (100%)
  * Crossover (100%)
  * Mutation (100%)
  * Selection (100%)

* Machine learning
  * Linear regression (0%)
  * Logistic regression (0%)
  * Support vector machine (0%)
  * Decision tree (0%)
  * Random forest (0%)
  * Neural network (50%)
  * Naive Bayes (0%)
  * Gaussian process (0%)

* Probability (& Statistics)
  * Distributions (50%)
  * Sampling (0%)

* Simulation
  * Markov chain (0%)

* Utils
  * Data loader (0%)
  * Generator (useful extensions) (100%)
  * Timing
