# Contributing to Classroom Distraction Tracker

Thank you for your interest in contributing to this project. This document provides guidelines and instructions for contributing.

## Code of Conduct

This project is released under the same research and educational context as the parent manuscript. All contributors are expected to:

- Use the codebase and datasets strictly for research and non-commercial purposes.
- Respect the ethical framework described in `DATASET_LICENSE.md` and `README.md`.
- Not use the framework for surveillance, profiling, re-identification, or punitive decision-making about individuals.
- Maintain attribution to the original authors and cite the manuscript appropriately.

## How to Contribute

### Reporting Bugs

1. **Search existing issues first** to avoid duplicates.
2. **Open a new issue** with a clear title and description.
3. Include:
   - The exact steps to reproduce the bug
   - Your operating system and hardware configuration
   - Any relevant error messages or logs
   - A minimal, reproducible example if possible

### Suggesting Enhancements

1. Open a GitHub issue to discuss the proposed feature before implementing it.
2. Provide a clear rationale for the enhancement.
3. Describe the expected behavior and any alternative approaches considered.

### Pull Requests

1. **Branch strategy**: Create a feature branch from `main`.
2. **Coding style**: Follow the existing code conventions in the repository.
3. **Documentation**: Update `README.md` or other relevant documentation if your changes affect usage.
4. **Testing**: Verify that the pipeline runs correctly on the provided evaluation data (if access is available).
5. **Commit messages**: Use clear, concise commit messages describing the change.
6. **PR description**: Provide a summary of changes, the motivation, and any breaking changes.

### Areas for Contribution

The following areas are particularly welcome:

- **Portability improvements**: Making the codebase easier to run on different operating systems or hardware platforms (e.g., CPU-only inference, mobile/edge deployment).
- **Documentation enhancements**: Clarifying usage instructions, adding examples, or translating documentation.
- **Benchmarking**: Reproducing results on additional classroom datasets or comparing against new baseline methods.
- **Ethical AI tooling**: Adding privacy-preserving features, fairness audits, or interpretability enhancements that strengthen the ethical foundations of the framework.

### Dataset and Ethical Considerations

- Do **not** add new datasets that involve human subjects without appropriate ethics approval documentation.
- Do **not** modify `DATASET_LICENSE.md` or `DATA_AVAILABILITY.md` without discussing the implications with the core authors.
- Any new visual examples or figures added to the repository must comply with the anonymization guidelines in `DATASET_LICENSE.md`.

## Getting Help

For questions about the codebase or methodology, please open a discussion on GitHub or contact the corresponding author (`jiajunqi@lynu.edu.cn`).

## License

By contributing, you agree that your contributions will be licensed under the MIT License for code and the Research-Only Non-Commercial terms in `DATASET_LICENSE.md` for any data or model files you introduce.
